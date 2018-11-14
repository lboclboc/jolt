from tasks import *
from plugins import directory
from cache import *
from graph import *
from scheduler import *


log.verbose("SelfDeploy loaded")


_path = fs.path.dirname(__file__)
_path = fs.path.dirname(_path)


@directory.influence(_path, pattern="*.py")
class Jolt(Task):
    name = "jolt"

    def info(self, fmt, *args, **kwargs):
        log.verbose(fmt, *args, **kwargs)

    def publish(self, artifact, tools):
        with tools.cwd(_path):
            artifact.collect('README.rst')
            artifact.collect('*.py')
            artifact.collect('*/*.py')
            artifact.collect('*/*.job')
            artifact.collect('*/*/*.py')


class SelfDeployExtension(NetworkExecutorExtension):
    @utils.cached.instance
    def get_parameters(self, task):
        registry = TaskRegistry()
        registry.add_task_class(Jolt)
        acache = ArtifactCache()
        gb = GraphBuilder(registry)
        dag = gb.build(["jolt"])
        task = dag.select(lambda graph, task: True)
        assert len(task) == 1, "too many selfdeploy tasks found"
        task = task[0]
        if not acache.is_available_remotely(task):
            duration = utils.duration()
            factory = LocalExecutorFactory()
            executor = LocalExecutor(factory, acache, task, force_upload=True)
            executor.run()
        jolt_url = acache.location(task)
        assert jolt_url, "failed to selfdeploy jolt to remote cache"
        return { "jolt_url":  jolt_url}


@NetworkExecutorExtensionFactory.Register
class SelfDeployExtensionFactory(NetworkExecutorExtensionFactory):
    def create(self):
        return SelfDeployExtension()
