# stdlib
import pickle
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

# syft absolute
import syft as sy
from syft import deserialize
from syft import serialize
from syft.lib.util import full_name_with_name
from syft.proto.message_pb2 import DataMessage as DataMessageProto

rust = sy.libsyft
run_class_method_message = rust.message.run_class_method_message


def _make_message(obj: object, capability: str) -> DataMessageProto:
    bytes = sy.serialize(obj, to_bytes=True)
    request = DataMessageProto()
    request.obj_type = full_name_with_name(klass=type(obj))
    request.content = bytes
    request.capability = capability
    return request


def _read_message(request_bytes: bytes) -> Optional[DataMessageProto]:
    try:
        request = DataMessageProto()
        request.ParseFromString(bytes(request_bytes))
        return request
    except Exception as e:
        print(f"Python failed to decode request {repr(request_bytes)}, error: {e}")
        return None


def create_handler(handler: Callable[[object], object]) -> Callable[[bytes], bytes]:
    def wrapped_handler(request_bytes: bytes) -> bytes:
        try:
            message = _read_message(request_bytes)
            if message is not None:
                data = deserialize(message.content, from_bytes=True)
                result = handler(data)
                response = _make_message(result, "message_without_reply")

                # serialize protobuf to bytes
                response_bytes = response.SerializeToString()
                return response_bytes
            else:
                return b""
        except Exception as e:
            print(f"Python failed to handle request {repr(request_bytes)}, error: {e}")
            return b""

    return wrapped_handler


def execute_capability(remote_addr: str, capability: str, data: object) -> object:
    try:
        request = _make_message(data, capability)
        request_bytes = request.SerializeToString()
        response_bytes = run_class_method_message(remote_addr, request_bytes)
        response_bytes = bytes(response_bytes)  # its a list
        try:
            response = _read_message(response_bytes)
            if response is not None:
                data = deserialize(response.content, from_bytes=True)
                return data
            else:
                print(f"Python failed to decode response: {repr(response_bytes)}")
        except Exception as e:
            print(f"Python failed to decode response: {e} {response_bytes}")
    except Exception as e:
        print(
            f"Python failed to execute request: {e} {remote_addr} {capability} {data}"
        )
    return None
