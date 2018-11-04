#!/usr/bin/python

import click
import imp
from tasks import Task, TaskRegistry, Parameter
import scheduler
import graph
import cache
import filesystem as fs
import log
import config
import sys
import plugins
import plugins.environ
import plugins.strings
import loader
import utils
from influence import *
import traceback


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Verbose.")
@click.option("-vv", "--extra-verbose", is_flag=True, help="Verbose.")
@click.option("-c", "--config-file", type=str, help="Configuration file")
def cli(verbose, extra_verbose, config_file):
    if verbose:
        log.set_level(log.VERBOSE)
    if extra_verbose:
        log.set_level(log.HYSTERICAL)
    if config_file:
        config.load(config_file)
        
    # Load configured plugins
    for section in config.sections():
        path = fs.path.dirname(__file__)
        path = fs.path.join(path, "plugins", section + ".py")
        if fs.path.exists(path):
            imp.load_source("plugins." + section, path)

    for cls in loader.JoltLoader().get().load():
        TaskRegistry.get().add_task_class(cls)


@cli.command()
@click.argument("task", type=str, nargs=-1, required=True)
@click.option("-n", "--network", is_flag=True, default=False, help="Build on network.")
@click.option("-i", "--identity", type=str, help="Expected hash identity")
def build(task, network, identity):
    executor = scheduler.ExecutorRegistry.get(network=network)
    acache = cache.ArtifactCache()
    gb = graph.GraphBuilder()
    dag = gb.build(task)
    dag.prune(lambda graph, task: task.is_cached(acache, network))

    if identity:
        root = dag.select(lambda graph, task: task.identity.startswith(identity))
        assert len(root) >= 1, "unknown hash identity, no such task: {}".format(identity)

    queue = scheduler.TaskQueue(executor)
    while dag.nodes:
        leafs = dag.select(lambda graph, task: task.is_ready(graph))
        while leafs:
            task = leafs.pop()
            task.set_in_progress()
            #task.info("Execution requested")
            queue.submit(acache, task)

        task, error = queue.wait()
        assert task, "blocked tasks remain and could not be unblocked, no more tasks in progress"
        if error:
            task.error("Execution failed after {}", task.duration)
            queue.abort()
            raise Exception(error)
        else: 
            task.info("Execution finished after {}", task.duration)

        task.set_completed(dag)

    #queue.shutdown()


@cli.command()
def clean():
    cache_provider = cache.ArtifactCache()
    fs.rmtree(cache_provider.root)


@cli.command()
@click.argument("task")
def display(task):
    gb = graph.GraphBuilder()
    gb.build([task])
    gb.display()


@cli.command()
@click.argument("task", required=False)
@click.option("-a", "--all", is_flag=True, help="Print all tasks recursively")
def list(task=None, reverse=False, all=False):
    result = []

    if not task:
        for task in sorted(TaskRegistry().get().get_task_classes(), key=lambda x: x.name):
            if task.name:
                print(task.name)
        return

    task_registry = TaskRegistry.get()
    dag = graph.GraphBuilder().build(task)
    tasks = dag.select(lambda graph, node: node.name == task)
    successors = set()
    for task in tasks:
        map(successors.add, dag.successors(task))

    for task in sorted(successors):
        print(task.qualified_name)

@cli.command()
@click.argument("task")
@click.option("-i", "--influence", is_flag=True, help="Print task influence.")
def info(task, influence=False):
    task_registry = TaskRegistry.get()
    task = task_registry.get_task(task)

    click.echo()
    click.echo("  {}".format(task.name))
    click.echo()
    if task.__doc__:
        click.echo("  {}".format(task.__doc__.strip()))
        click.echo()
    click.echo("  Parameters")
    has_param = False
    for item, param in task.__dict__.iteritems():
        if isinstance(param, Parameter):
            has_param = True
            click.echo("    {:<15}   {}".format(item, param.__doc__ or ""))
    if not has_param:
        click.echo("    None")

    click.echo()
    click.echo("  Requirements")
    for req in task.requires:
        click.echo("    {}".format(req))
    if not task.requires:
        click.echo("    None")
    click.echo()

    acache = cache.ArtifactCache()
    dag = graph.GraphBuilder().build([task.name])
    tasks = dag.select(lambda graph, node: graph.is_root(node))
    assert len(tasks) == 1, "unexpected graph generated"
    proxy = tasks[0]

    click.echo("  Cache")
    click.echo("    Identity          {}".format(proxy.identity))
    if acache.is_available_locally(proxy):
        click.echo("    Local             {} ({} bytes)".format(True, acache.get_artifact(proxy).size))
    click.echo("    Remote            {}".format(acache.is_available_remotely(proxy)))
    click.echo()

    if influence:
        click.echo("  Influence")
        for string in HashInfluenceRegistry.get().get_strings(task):
            click.echo("    " + string)
        click.echo()

def main():
    try:
        cli()
    except AssertionError as e:
        # traceback.print_exc()
        log.error(str(e))
        sys.exit(1)
    except Exception as e:
        log.error(str(e))
        sys.exit(1)

        
if __name__ == "__main__":
    main()
