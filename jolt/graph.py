from contextlib import contextmanager, ExitStack
import copy
import hashlib
from os import getenv
from threading import RLock
from collections import OrderedDict
import uuid

from jolt.tasks import Alias, Resource, WorkspaceResource, Task
from jolt.influence import HashInfluenceRegistry, TaskRequirementInfluence
from jolt import log
from jolt import utils
from jolt import colors
from jolt import hooks
from jolt import filesystem as fs
from jolt.error import raise_error_if
from jolt.error import raise_task_error_if
from jolt.options import JoltOptions


class TaskProxy(object):
    def __init__(self, task, graph, cache, options):
        self.task = task
        self.graph = graph
        self.cache = cache
        self.options = options

        self.children = []
        self.ancestors = set()
        self.descendants = set()
        self.neighbors = []
        self.extensions = []
        self.duration_queued = None
        self.duration_running = None
        self.requirement_aliases = {}

        self._extended_task = None
        self._in_progress = False
        self._completed = False
        self._goal = False
        self._download = True
        self._local = False
        self._network = False
        self._artifacts = []

        hooks.task_created(self)

    def __hash__(self):
        return id(self)

    @property
    def artifacts(self):
        return self._artifacts

    @property
    def tools(self):
        return self.task.tools

    @property
    def name(self):
        return self.task.name

    @property
    def canonical_name(self):
        return self.task.canonical_name

    @property
    def qualified_name(self):
        return self.task.qualified_name

    @property
    def short_qualified_name(self):
        return self.task.short_qualified_name

    @property
    def log_name(self):
        return "({0} {1})".format(self.short_qualified_name, self.identity[:8])

    @property
    def identity(self):
        if self.task.identity is not None:
            return self.task.identity

        # Acquire workspace resources before calculating the identity
        for c in self.children:
            if c.is_workspace_resource():
                c.task.acquire_ws()

        sha = hashlib.sha1()
        HashInfluenceRegistry.get().apply_all(self.task, sha)
        self.task.identity = sha.hexdigest()

        return str(self.task.identity)

    @identity.setter
    def identity(self, value):
        self.task.identity = value

    @property
    def instance(self):
        return self.task._instance.value

    @property
    def is_unstable(self):
        return self.task.unstable

    @property
    def weight(self):
        return self.task.weight

    @weight.setter
    def weight(self, weight):
        self.task.weight = weight

    def __str__(self):
        return "{0}{1}".format(self.short_qualified_name, "*" if self.is_extension() else '')

    def info(self, fmt, *args, **kwargs):
        self.task.info(fmt + " " + self.log_name, *args, **kwargs)

    def verbose(self, fmt, *args, **kwargs):
        log.verbose(fmt + " " + self.log_name, *args, **kwargs)

    def warning(self, fmt, *args, **kwargs):
        self.task.warning(fmt + " " + self.log_name, *args, **kwargs)

    def error(self, fmt, *args, **kwargs):
        self.task.error(fmt + " " + self.log_name, *args, **kwargs)

    def has_children(self):
        return len(self.children) > 0

    def has_ancestors(self):
        return len(self.ancestors) > 0

    def has_artifact(self):
        return self.is_cacheable() and not self.is_resource() and not self.is_alias()

    def has_extensions(self):
        return len(self.extensions) > 0

    def add_extension(self, task):
        if self.is_extension():
            self.get_extended_task().add_extension(task)
        self.extensions.append(task)

    def set_extended_task(self, task):
        self._extended_task = task

    def get_extended_task(self):
        if self.is_extension():
            return self._extended_task.get_extended_task()
        return self

    def deps_available_locally(self):
        for c in self.children:
            if c.is_resource() or c.is_alias():
                continue
            if not c.is_available_locally():
                return False
        return True

    def is_alias(self):
        return isinstance(self.task, Alias)

    def is_available_locally(self, extensions=True, skip_session=False):
        dep_artifacts = []
        if extensions:
            for dep in self.extensions:
                dep_artifacts += dep.artifacts
        artifacts = filter(lambda a: not a.is_session(), self._artifacts + dep_artifacts)
        return all(map(self.cache.is_available_locally, artifacts))

    def is_available_remotely(self, extensions=True):
        dep_artifacts = []
        if extensions:
            for dep in self.extensions:
                dep_artifacts += dep.artifacts
        artifacts = filter(lambda a: not a.is_session(), self._artifacts + dep_artifacts)
        return all(map(self.cache.is_available_remotely, artifacts))

    def is_cacheable(self):
        return self.task.is_cacheable()

    def is_completed(self):
        return self._completed

    def is_downloadable(self):
        return self._download

    def is_extension(self):
        return self._extended_task is not None

    def is_fast(self):
        tasks = [self.task] + [e.task for e in self.extensions]
        return all([task.fast for task in tasks])

    def is_identified(self):
        return self.task.identity is not None

    def is_goal(self, with_extensions=True):
        return self._goal or (with_extensions and any([e.is_goal() for e in self.extensions]))

    def in_progress(self):
        return self._in_progress

    def is_ready(self):
        if self.in_progress():
            return False

        if self.is_extension():
            return False

        return self.graph.is_leaf(self)

    def is_locally_executed(self):
        return self._local

    def is_remotely_executed(self):
        return self._network

    def is_resource(self):
        return isinstance(self.task, Resource)

    def is_unpackable(self):
        return self.task.unpack.__func__ is not Task.unpack

    def is_unpacked(self):
        tasks = [self] + self.extensions
        artifacts = []
        for task in tasks:
            artifacts.extend(task._artifacts)
        return any(map(lambda artifact: artifact.is_unpacked(), artifacts))

    def is_uploadable(self, artifacts=None):
        tasks = [self] + self.extensions
        if not artifacts:
            artifacts = []
            for task in tasks:
                artifacts.extend(task._artifacts)
        return all(map(lambda artifact: artifact.is_uploadable(), artifacts))

    def is_workspace_resource(self):
        return isinstance(self.task, WorkspaceResource)

    @contextmanager
    def lock_artifacts(self, discard=False):
        artifacts = []
        stack = ExitStack()
        for artifact in self.artifacts:
            lock = self.cache.lock_artifact(artifact, discard=discard)
            artifacts.append(stack.enter_context(lock))
        try:
            self._artifacts = artifacts
            yield artifacts
        finally:
            stack.close()

    def disable_download(self):
        self._download = False

    def download(self, force=False, session_only=False, persistent_only=False):
        if not self.is_downloadable():
            return True
        artifacts = self._artifacts
        if session_only:
            artifacts = list(filter(lambda a: a.is_session(), self._artifacts))
        if persistent_only:
            artifacts = list(filter(lambda a: not a.is_session(), self._artifacts))
        if not artifacts:
            return True
        return all([self.cache.download(artifact, force=force) for artifact in artifacts])

    def upload(self, force=False, locked=False, session_only=False, persistent_only=False):
        artifacts = self._artifacts
        if session_only:
            artifacts = list(filter(lambda a: a.is_session(), self._artifacts))
        if persistent_only:
            artifacts = list(filter(lambda a: not a.is_session(), self._artifacts))
        if not artifacts:
            return True
        if not self.is_uploadable(artifacts):
            return False
        return all([self.cache.upload(artifact, force=force, locked=locked) for artifact in artifacts])

    def resolve_requirement_alias(self, name):
        return self.requirement_aliases.get(name)

    def set_in_progress(self):
        self._in_progress = True

    def set_locally_executed(self):
        self._local = True

    def set_remotely_executed(self):
        self._network = True

    def set_goal(self):
        self._goal = True

    def finalize(self, dag, manifest):
        log.debug("Finalizing: " + self.short_qualified_name)
        self.manifest = manifest

        # Find all direct and transitive dependencies
        self.ancestors = set()
        self.descendants = set()

        self.neighbors = copy.copy(self.children)
        self.neighbors = sorted(self.neighbors, key=lambda n: n.qualified_name)

        for n in self.neighbors:
            self.descendants.add(n)
            self.descendants = self.descendants.union(n.descendants)
            if not n.task.selfsustained:
                self.children.extend(n.children)
            n.ancestors.add(self)

        # Exclude transitive alias and resources dependencies
        self.children = list(
            filter(lambda n: not n.is_alias() and (not n.is_resource() or dag.are_neighbors(self, n)),
                   utils.unique_list(self.children)))

        self.descendants = list(self.descendants)

        self.task.influence += [TaskRequirementInfluence(n) for n in self.neighbors]
        self.identity
        self._artifacts = self.task._artifacts(self.cache, self)

        return self.identity

    def taint(self, salt=None):
        self.task.taint = salt or uuid.uuid4()
        if salt is None:
            # Only recalculate identity when build is forced, not when salted
            self.identity = None
            self.identity

    def started(self, what="Execution"):
        self.task.info(colors.blue(what + " started " + self.log_name))
        self.duration_queued = utils.duration()
        self.duration_running = utils.duration()
        hooks.task_started(self)

    def running(self, when=None):
        self.duration_running = utils.duration() if not when else when

    def failed(self, what="Execution"):
        self.error("{0} failed after {1} {2}", what,
                   self.duration_running,
                   self.duration_queued.diff(self.duration_running))
        if self.is_unstable:
            try:
                self.graph.remove_node(self)
            except KeyError:
                self.warning("Pruned task was executed")
            self.graph.add_unstable(self)
            hooks.task_unstable(self)
        else:
            self.graph.add_failed(self)
            hooks.task_failed(self)

    def passed(self, what="Execution"):
        hooks.task_passed(self)

    def finished(self, what="Execution"):
        raise_task_error_if(
            self.is_completed() and not self.is_extension(),
            self, "task has already been completed")
        self._completed = True
        try:
            self.graph.remove_node(self)
        except KeyError:
            self.warning("Pruned task was executed")
        self.task.info(colors.green(what + " finished after {0} {1}" + self.log_name),
                       self.duration_running,
                       self.duration_queued.diff(self.duration_running))
        hooks.task_finished(self)

    def skipped(self):
        self._completed = True
        try:
            self.graph.remove_node(self)
        except KeyError:
            pass
        hooks.task_skipped(self)

    def pruned(self):
        self._completed = True
        try:
            self.graph.remove_node(self)
        except KeyError:
            self.warning("Pruned task was already pruned")
        hooks.task_pruned(self)

    def clean(self, cache, if_expired, onerror=None):
        with self.tools:
            self.task.clean(self.tools)
            for artifact in self.artifacts:
                discarded = cache.discard(artifact, if_expired, onerror=fs.onerror_warning)
                if discarded:
                    log.debug("Discarded: {} ({})", self.short_qualified_name, artifact.identity)
                else:
                    log.debug(" Retained: {} ({})", self.short_qualified_name, artifact.identity)

    def run(self, cache, force_upload=False, force_build=False):
        with self.tools:
            available_locally = available_remotely = False

            for child in self.children:
                if not child.has_artifact():
                    continue
                raise_task_error_if(
                    not child.is_completed() and child.is_unstable,
                    self, "Task depends on failed task '{}'", child.short_qualified_name)
                if not child.is_available_locally(extensions=False):
                    raise_task_error_if(
                        not child.download(),
                        child, "Failed to download task artifact")

            if not force_build:
                available_locally = self.is_available_locally()
                if available_locally and not force_upload:
                    return
                available_remotely = cache.download_enabled() and self.is_available_remotely()
                if not available_locally and available_remotely:
                    available_locally = self.download()

            if force_build or not available_locally:
                with log.threadsink() as buildlog:
                    if self.task.is_runnable():
                        log.verbose("Host: {0}", getenv("HOSTNAME", "localhost"))

                    with self.lock_artifacts(discard=force_build) as artifacts:
                        if not self.is_available_locally() or self.has_extensions():
                            with cache.get_context(self) as context:
                                self.running()
                                with self.tools.cwd(self.task.joltdir):
                                    hooks.task_prerun(self, context, self.tools)
                                    if self.is_goal() and self.options.debug:
                                        log.info("Entering debug shell")
                                        self.task.debugshell(context, self.tools)
                                    try:
                                        self.task.run(context, self.tools)
                                    finally:
                                        hooks.task_postrun(self, context, self.tools)
                                        # Publish session artifacts
                                        with self.tools.cwd(self.task.joltdir):
                                            for artifact in filter(lambda a: a.is_session(), artifacts):
                                                self.publish(context, artifact)
                                        raise_task_error_if(
                                            not self.upload(force=force_upload, locked=False, session_only=True) and cache.upload_enabled(),
                                            self, "Failed to upload session artifact")

                                if not self.is_available_locally(extensions=False):
                                    # Publish persistent artifacts
                                    with self.tools.cwd(self.task.joltdir):
                                        with self.tools.cwd(self.task.joltdir):
                                            for artifact in filter(lambda a: not a.is_session(), artifacts):
                                                self.publish(context, artifact, buildlog)
                                else:
                                    self.info("Publication skipped, already in local cache")
                        else:
                            self.info("Execution skipped, already in local cache")

                        # Must upload the artifact while still holding its lock, otherwise the
                        # artifact may become unpack():ed before we have a chance to.
                        if force_upload or force_build or not available_remotely:
                            raise_task_error_if(
                                not self.upload(force=force_upload, locked=False, persistent_only=True) and cache.upload_enabled(),
                                self, "Failed to upload task artifact")
            elif force_upload or not available_remotely:
                raise_task_error_if(
                    not self.upload(force=force_upload, persistent_only=True) and cache.upload_enabled(),
                    self, "Failed to upload task artifact")

            for extension in self.extensions:
                try:
                    extension.started()
                    with hooks.task_run(extension):
                        extension.run(cache, force_upload, force_build)
                except Exception as e:
                    extension.failed()
                    raise e
                else:
                    extension.finished()

    def publish(self, context, artifact, buildlog=None):
        hooks.task_prepublish(self, artifact, self.tools)
        publish = self.task.publish if artifact.is_main() else \
            getattr(self.task, "publish_" + artifact.name)
        publish(artifact, self.tools)
        self.task._verify_influence(context, artifact, self.tools)
        if artifact.is_main() and buildlog:
            with open(fs.path.join(artifact.path, ".build.log"), "w") as f:
                f.write(buildlog.getvalue())
        hooks.task_postpublish(self, artifact, self.tools)
        artifact.get_cache().commit(artifact)

    def report(self):
        return self.task.report()


class Graph(object):
    def __init__(self):
        self._mutex = RLock()
        self._failed = []
        self._unstable = []
        self._children = OrderedDict()
        self._parents = OrderedDict()

    def add_node(self, node):
        with self._mutex:
            self._children[node] = OrderedDict()
            self._parents[node] = OrderedDict()

    def remove_node(self, node):
        with self._mutex:
            parents = self._parents[node].keys()
            for child in self._children[node]:
                del self._parents[child][node]
            for parent in parents:
                del self._children[parent][node]
            del self._children[node]
            del self._parents[node]

    def add_edges_from(self, edges):
        with self._mutex:
            for src, dst in edges:
                self._children[src][dst] = None
                self._parents[dst][src] = None

    def successors(self, node):
        return self._children[node].keys()

    def predecessors(self, node):
        return self._parents[node].keys()

    @property
    def topological_nodes(self):
        with self._mutex:
            G = self.clone()
            S = G.roots
            L = []
            while S:
                for n in S:
                    L.append(n)
                    G.remove_node(n)
                S = G.roots
            if len(G.nodes) > 0:
                log.debug("[GRAPH] Graph has cycles between these nodes:")
                for node in G.nodes:
                    log.debug("[GRAPH]   " + node.short_qualified_name)
                raise_error_if(len(G.nodes) > 0, "graph has cycles")
            return L

    def clone(self):
        g = Graph()
        g._children = OrderedDict()
        g._parents = OrderedDict()
        for k, v in self._children.items():
            g._children[k] = copy.copy(v)
        for k, v in self._parents.items():
            g._parents[k] = copy.copy(v)
        return g

    @property
    def nodes(self):
        with self._mutex:
            return self._children.keys()

    def number_of_tasks(self, filterfn=None):
        return len(list(filter(filterfn, self.nodes)) if filterfn else self.nodes)

    @property
    def failed(self):
        return self._failed

    def add_failed(self, task):
        self._failed.append(task)

    @property
    def unstable(self):
        return self._unstable

    def add_unstable(self, task):
        self._unstable.append(task)

    @property
    def tasks(self):
        with self._mutex:
            return [n for n in self.nodes]

    @property
    def roots(self):
        with self._mutex:
            return [n for n in self.nodes if self.is_root(n)]

    def has_tasks(self):
        with self._mutex:
            return len(self.nodes) > 0

    def get_task(self, qualified_name):
        with self._mutex:
            return self._nodes_by_name.get(qualified_name)

    def select(self, func):
        with self._mutex:
            return [n for n in self.nodes if func(self, n)]

    def debug(self):
        with self._mutex:
            log.debug("[GRAPH] Listing all nodes")
            for node in self.topological_nodes:
                log.debug("[GRAPH]   " + node.qualified_name + " ({})", len(self._children[node].keys()))

    def is_leaf(self, node):
        with self._mutex:
            return len(self._children[node].keys()) == 0

    def is_root(self, node):
        with self._mutex:
            return len(self._parents[node].keys()) == 0

    def is_orphan(self, node):
        with self._mutex:
            return self.is_root(node) and self.is_leaf(node)

    def are_neighbors(self, n1, n2):
        with self._mutex:
            return n2 in self._children[n1]


class GraphBuilder(object):
    def __init__(self, registry, cache, manifest, options=None, progress=False):
        self.cache = cache
        self.graph = Graph()
        self.nodes = {}
        self.registry = registry
        self.manifest = manifest
        self.progress = progress
        self.options = options or JoltOptions()

    def _get_node(self, progress, name):
        name = utils.stable_task_name(name)
        node = self.nodes.get(name)
        if not node:
            task = self.registry.get_task(name, manifest=self.manifest)
            node = self.nodes.get(task.qualified_name, None)
            if node is not None:
                return node
            node = TaskProxy(task, self.graph, self.cache, self.options)
            self.nodes[node.short_qualified_name] = node
            self.nodes[node.qualified_name] = node
            if self.options.salt:
                node.taint(self.options.salt)
            self._build_node(progress, node)
            progress.update(1)
        return node

    def _build_node(self, progress, node):
        self.graph.add_node(node)

        if node.task.extends:
            extended_node = self._get_node(progress, node.task.extends)
            self.graph.add_edges_from([(node, extended_node)])
            node.set_extended_task(extended_node)
            extended_node.add_extension(node)
            node.children.append(extended_node)
            parent = extended_node.get_extended_task()
        else:
            parent = node

        for requirement in node.task.requires:
            alias, artifact, task, name = utils.parse_aliased_task_name(requirement)
            child = self._get_node(progress, utils.format_task_name(task, name))
            # Create direct edges from alias parents to alias children
            if child.is_alias():
                for child_child in child.children:
                    self.graph.add_edges_from([(parent, child_child)])
                    node.children.append(child_child)
            self.graph.add_edges_from([(parent, child)])
            node.children.append(child)
            if alias:
                node.requirement_aliases[alias] = requirement

        node.children = utils.unique_list(node.children)

        return node

    @contextmanager
    def _progress(self, *args, **kwargs):
        if self.progress:
            with log.progress(*args, **kwargs) as p:
                yield p
        else:
            with log.progress_log(*args, **kwargs) as p:
                yield p

    def build(self, task_list, influence=True):
        with self._progress("Building graph", len(self.graph.tasks), "tasks") as progress:
            goals = [self._get_node(progress, task) for task in task_list]
            self.graph._nodes_by_name = self.nodes

        if influence:
            topological_nodes = self.graph.topological_nodes
            with self._progress("Collecting task influence", len(self.graph.tasks), "tasks") as p:
                for node in reversed(topological_nodes):
                    node.finalize(self.graph, self.manifest)
                    p.update(1)

            max_time = 0
            min_time = 0
            for node in topological_nodes:
                max_time += node.task.weight
                node.task.weight += max([a.weight for a in node.ancestors] + [0])
                min_time = max(node.task.weight, min_time)

            log.verbose("Time estimate: {}- {}",
                        utils.duration_diff(min_time),
                        utils.duration_diff(max_time))

        self.graph.requested_goals = goals
        self.graph.goals = []
        for goal in goals:
            goal.set_goal()
            self.graph.goals.append(goal)
            if goal.is_alias():
                for goal_alias in goal.neighbors:
                    goal_alias.set_goal()
                    self.graph.goals.append(goal_alias)

        self.graph.all_nodes = [n for n in self.graph.nodes]

        return self.graph


class PruneStrategy(object):
    def should_prune_requirements(self, task):
        raise NotImplementedError()


class GraphPruner(object):
    def __init__(self, strategy):
        self.strategy = strategy
        self.retained = set()
        self.visited = set()

    def _check_node(self, node):
        if node in self.visited:
            return
        self._progress.update(1)
        self.visited.add(node)
        self.retained.add(node)

        prune = self.strategy.should_prune_requirements(node)
        if not node.task.selfsustained or not prune or node.is_extension():
            utils.map_concurrent(self._check_node, node.neighbors)

    def prune(self, graph):
        with log.progress("Checking availability", 0, " tasks") as p:
            self._progress = p
            for root in graph.roots:
                self._check_node(root)

        for node in graph.goals:
            self.retained.add(node)

        pruned = []
        for node in graph.nodes:
            if node not in self.retained:
                pruned.append(node)
            else:
                log.debug("Retained: {}", node.log_name)
                node.children = [c for c in node.children if c in self.retained]

        for node in pruned:
            log.debug("Excluded: {}", node.log_name)
            node.pruned()

        return graph
