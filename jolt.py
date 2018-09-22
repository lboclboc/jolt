#!/usr/bin/python

#import jenkins
import click
import imp
from tasks import Task, TaskRegistry
import scheduler
import graph
import cache
import filesystem as fs
import log
import config
import sys
import pdb
import plugins
import plugins.environ
import plugins.strings
import loader


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
            with open(path) as fd:
                imp.load_module("plugins." + section, fd, path, ('.py', 'r', imp.PY_SOURCE))

    for cls in loader.JoltLoader().get().load_directory():
        TaskRegistry.get().add_task_class(cls)


@cli.command()
@click.argument("task")
@click.option("--local", is_flag=True, default=False, help="Build local.")
def build(task, local):
    executor = scheduler.ExecutorRegistry(network=not local)
    acache = cache.ArtifactCache()

    tasks = [TaskRegistry.get().get_task(task)]
    dag = graph.GraphBuilder.build(tasks)
    dag.prune(lambda graph, task: acache.is_available_locally(task))

    leafs = dag.select(lambda graph, task: graph.is_leaf(task))
    while leafs:
        while leafs:
            task = leafs.pop()
            dag.remove_node(task)
        
            worker = executor.create(acache, task)
            worker.run(task)
        leafs = dag.select(lambda graph, task: graph.is_leaf(task))


@cli.command()
def clean():
    cache_provider = cache.ArtifactCache()
    fs.rmtree(cache_provider.root)
    

@cli.command()
@click.argument("task", required=False)
@click.option("-a", "--all", is_flag=True, help="Print all tasks recursively")
def list(task=None, reverse=False, all=False):
    result = []

    if not task:
        for task in sorted(Task.instances.values(), key=lambda x: x.name):
            print(task.name)
        return

    task_registry = TaskRegistry.get()

    tasks = [task_registry.get_task(task)]
    dag = graph.GraphBuilder.build(tasks, task_registry)
    tasks = dag.select(lambda graph, node: node.name == task)
    successors = set()
    for task in tasks:
        map(successors.add, dag.successors(task))

    for task in sorted(successors):
        print(task.name)


def main():
    try:
        cli()
    except AssertionError as e:
        log.error(str(e))
        sys.exit(1)

        
if __name__ == "__main__":
    main()
