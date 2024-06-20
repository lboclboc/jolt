# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from jolt.plugins.remote_execution import administration_pb2 as jolt_dot_plugins_dot_remote__execution_dot_administration__pb2
from jolt.plugins.remote_execution import scheduler_pb2 as jolt_dot_plugins_dot_remote__execution_dot_scheduler__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in jolt/plugins/remote_execution/administration_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class AdministrationStub(object):
    """This service is not yet implemented.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CancelBuild = channel.unary_unary(
                '/Administration/CancelBuild',
                request_serializer=jolt_dot_plugins_dot_remote__execution_dot_scheduler__pb2.CancelBuildRequest.SerializeToString,
                response_deserializer=jolt_dot_plugins_dot_remote__execution_dot_scheduler__pb2.CancelBuildResponse.FromString,
                _registered_method=True)
        self.ListBuilds = channel.unary_unary(
                '/Administration/ListBuilds',
                request_serializer=jolt_dot_plugins_dot_remote__execution_dot_administration__pb2.ListBuildsRequest.SerializeToString,
                response_deserializer=jolt_dot_plugins_dot_remote__execution_dot_administration__pb2.ListBuildsResponse.FromString,
                _registered_method=True)
        self.ListWorkers = channel.unary_unary(
                '/Administration/ListWorkers',
                request_serializer=jolt_dot_plugins_dot_remote__execution_dot_administration__pb2.ListWorkersRequest.SerializeToString,
                response_deserializer=jolt_dot_plugins_dot_remote__execution_dot_administration__pb2.ListWorkersResponse.FromString,
                _registered_method=True)
        self.Reschedule = channel.unary_unary(
                '/Administration/Reschedule',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)


class AdministrationServicer(object):
    """This service is not yet implemented.
    """

    def CancelBuild(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListBuilds(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListWorkers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Reschedule(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AdministrationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CancelBuild': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelBuild,
                    request_deserializer=jolt_dot_plugins_dot_remote__execution_dot_scheduler__pb2.CancelBuildRequest.FromString,
                    response_serializer=jolt_dot_plugins_dot_remote__execution_dot_scheduler__pb2.CancelBuildResponse.SerializeToString,
            ),
            'ListBuilds': grpc.unary_unary_rpc_method_handler(
                    servicer.ListBuilds,
                    request_deserializer=jolt_dot_plugins_dot_remote__execution_dot_administration__pb2.ListBuildsRequest.FromString,
                    response_serializer=jolt_dot_plugins_dot_remote__execution_dot_administration__pb2.ListBuildsResponse.SerializeToString,
            ),
            'ListWorkers': grpc.unary_unary_rpc_method_handler(
                    servicer.ListWorkers,
                    request_deserializer=jolt_dot_plugins_dot_remote__execution_dot_administration__pb2.ListWorkersRequest.FromString,
                    response_serializer=jolt_dot_plugins_dot_remote__execution_dot_administration__pb2.ListWorkersResponse.SerializeToString,
            ),
            'Reschedule': grpc.unary_unary_rpc_method_handler(
                    servicer.Reschedule,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Administration', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('Administration', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Administration(object):
    """This service is not yet implemented.
    """

    @staticmethod
    def CancelBuild(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Administration/CancelBuild',
            jolt_dot_plugins_dot_remote__execution_dot_scheduler__pb2.CancelBuildRequest.SerializeToString,
            jolt_dot_plugins_dot_remote__execution_dot_scheduler__pb2.CancelBuildResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ListBuilds(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Administration/ListBuilds',
            jolt_dot_plugins_dot_remote__execution_dot_administration__pb2.ListBuildsRequest.SerializeToString,
            jolt_dot_plugins_dot_remote__execution_dot_administration__pb2.ListBuildsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ListWorkers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Administration/ListWorkers',
            jolt_dot_plugins_dot_remote__execution_dot_administration__pb2.ListWorkersRequest.SerializeToString,
            jolt_dot_plugins_dot_remote__execution_dot_administration__pb2.ListWorkersResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Reschedule(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Administration/Reschedule',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
