import sys
import inspect
import cache
import log
import utils
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
import traceback


class TaskQueue(object):
    def __init__(self, execregistry):
        self.futures = {}
        self.execregistry = execregistry
    
    def submit(self, cache, task):
        executor = self.execregistry.create(cache, task)
        assert executor, "no executor can execute the task; "\
            "requesting a network build without proper configuration?"

        future = executor.submit()
        self.futures[future] = task
        return future

    def wait(self):
        for future in as_completed(self.futures):
            task = self.futures[future]
            error = None
            try:
                result = future.result()
            except AssertionError as e:
                log.verbose(traceback.format_exc())
                error = str(e) or ''
            except Exception as e:
                error = traceback.format_exc()
                log.verbose(error)
            del self.futures[future]
            return task, error
        return None, None

    def abort(self):
        for future, task in self.futures.iteritems():
            task.info("Execution cancelled")
            future.cancel()
        log.info("Waiting for tasks to finish")
        self.execregistry.shutdown()

    def in_progress(self, task):
        return task in self.futures.values()


class Executor(object):
    def __init__(self, factory):
        self.factory = factory

    def submit(self):
        return self.factory.submit(self)
        
    def run(self, task):
        pass


class LocalExecutor(Executor):
    def __init__(self, factory, cache, task, force_upload=False):
        super(LocalExecutor, self).__init__(factory)
        self.cache = cache
        self.task = task
        self.force_upload = force_upload

    def run(self):
        try:
            self.task.started()
            self.task.run(self.cache, self.force_upload)
        except:
            self.task.failed()
        else:
            self.task.finished()
        return self.task


class NetworkExecutor(Executor):
    pass


@utils.Singleton
class ExecutorRegistry(object):
    executor_factories = []
    extension_factories = []

    def __init__(self, network=True):
        self._factories = [factory() for factory in self.__class__.executor_factories]
        self._extensions = [factory().create() for factory in self.__class__.extension_factories]
        self._network = network

    def shutdown(self):
        for factory in self._factories:
            factory.shutdown()
        
    def create(self, cache, task):
        for factory in self._factories:
            if not task.is_cacheable() and factory.is_network():
                continue
            if not self._network and factory.is_network():
                continue
            if self._network and not factory.is_network():
                if task.is_cacheable():
                    continue
            if factory.is_eligable(cache, task):
                return factory.create(cache, task)
        return None

    def get_network_parameters(self, task):
        parameters = {}
        for extension in self._extensions:
            parameters.update(extension.get_parameters(task))
        return parameters


class NetworkExecutorExtensionFactory(object):
    @staticmethod
    def Register(cls):
        # assert cls is Factory
        ExecutorRegistry.extension_factories.insert(0, cls)

    def create(self):
        raise NotImplemented()
    

class NetworkExecutorExtension(object):
    def get_parameters(self, task):
        return {}


class ExecutorFactory(object):
    @staticmethod
    def Register(cls):
        # assert cls is Factory
        ExecutorRegistry.executor_factories.insert(0, cls)

    def __init__(self, num_workers=None):
        self.pool = ThreadPoolExecutor(max_workers=num_workers)

    def shutdown(self):
        self.pool.shutdown()
        
    def is_network(self):
        return False
    
    def is_eligable(self, cache, task):
        raise NotImplemented()

    def create(self, cache, task):
        raise NotImplemented()

    def submit(self, executor):
        return self.pool.submit(executor.run)

    
    
class LocalExecutorFactory(ExecutorFactory):
    def __init__(self):
        super(LocalExecutorFactory, self).__init__(num_workers=1)
    
    def is_network(self):
        return False

    def is_eligable(self, cache, task):
        return True

    def create(self, cache, task):
        return LocalExecutor(self, cache, task)

ExecutorFactory.Register(LocalExecutorFactory)


class NetworkExecutorFactory(ExecutorFactory):
    def is_network(self):
        return True

    def is_eligable(self, cache, task):
        return True

