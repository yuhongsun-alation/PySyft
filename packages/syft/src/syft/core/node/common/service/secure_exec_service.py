# future
from __future__ import annotations

# stdlib
import ast
import sys
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple

# third party
import _ast
from google.protobuf.reflection import GeneratedProtocolMessageType
from nacl.signing import VerifyKey

# syft relative
from ..... import serialize
from .....generate_wrapper import GenerateWrapper
from .....lib import bind_ast
from .....logger import debug
from .....logger import traceback
from .....proto.core.ast.module_pb2 import AstModule as AstModule_PB
from .....proto.core.node.common.service.secure_exec_service_pb2 import (
    SecureExecMessage as SecureExecMessage_PB,
)
from .....util import get_fully_qualified_name
from ....common.message import ImmediateSyftMessageWithoutReply
from ....common.serde.deserialize import _deserialize
from ....common.serde.serializable import bind_protobuf
from ....common.uid import UID
from ....io.address import Address
from ...abstract.node import AbstractNode
from .auth import service_auth
from .node_service import ImmediateNodeServiceWithoutReply

# TODO: Ugly TEMP CODE PLAYGROUND


def object2proto(obj: _ast.Module) -> AstModule_PB:
    # temporary workaround
    import pickle  # nosec # isort:skip

    data = pickle.dumps(obj)
    try:
        del sys.modules["pickle"]
    except Exception as e:
        pass
    try:
        del pickle
    except Exception as e:
        pass

    # continue
    return AstModule_PB(obj_type=get_fully_qualified_name(obj=obj), data=data)


def proto2object(proto: AstModule_PB) -> _ast.Module:
    # temporary workaround
    import pickle  # nosec # isort:skip

    ast_tree = pickle.loads(proto.data)
    try:
        del sys.modules["pickle"]
    except Exception as e:
        pass
    try:
        del pickle
    except Exception as e:
        pass

    # continue
    return ast_tree


GenerateWrapper(
    wrapped_type=_ast.Module,
    import_path="_ast.Module",
    protobuf_scheme=AstModule_PB,
    type_object2proto=object2proto,
    type_proto2object=proto2object,
)


builtins = [
    "__import__",
    "abs",
    "all",
    "any",
    "ascii",
    "bin",
    "bool",
    "breakpoint",
    "bytearray",
    "bytes",
    "callable",
    "chr",
    "classmethod",
    "compile",
    "complex",
    "delattr",
    "dict",
    "dir",
    "divmod",
    "enumerate",
    "eval",
    "exec",
    "filter",
    "float",
    "format",
    "frozenset",
    "getattr",
    "globals",
    "hasattr",
    "hash",
    "help",
    "hex",
    "id",
    "input",
    "int",
    "isinstance",
    "issubclass",
    "iter",
    "len",
    "list",
    "locals",
    "map",
    "max",
    "memoryview",
    "min",
    "next",
    "object",
    "oct",
    "open",
    "ord",
    "pow",
    "print",
    "property",
    "range",
    "repr",
    "reversed",
    "round",
    "set",
    "setattr",
    "slice",
    "sorted",
    "staticmethod",
    "str",
    "sum",
    "super",
    "tuple",
    "type",
    "vars",
    "zip",
]

# TODO: from@Trask: remove any use of bad_ops or denylist. Should be able to rely only on allowlist
bad_ops = [
    "exec",
    "eval",
    "open",
    "compile",
    "memoryview",
    "input",
    "globals",
    "breakpoint",
]

# TODO: from@Trask: remove because it doesn't get used?
denylist = [ast.Import, ast.ImportFrom]


def parse_all_nodes(tree):
    nodes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            call_path = ""
            if isinstance(node.func, (ast.Name)):
                if node.func.id in builtins:
                    module = "__builtins__"
                else:
                    module = "__file__"
                call_path = f"{module}.{node.func.id}"
                nodes.append((node, call_path))
            elif isinstance(node.func, (ast.Attribute)):
                module = "__file__"
                call_path = f"{module}.{node.func.value.id}.{node.func.attr}"
                nodes.append((node, call_path))
            else:
                raise ("Found a different Call type")
        if isinstance(node, ast.Import):
            imports = ",".join([name.name for name in node.names])
            nodes.append((node, f"import {imports}"))
        if isinstance(node, ast.ImportFrom):
            imports = ", ".join([name.name for name in node.names])
            nodes.append((node, f"from {node.module} import {imports}"))
    return nodes


def validate_nodes(nodes):
    valid = True
    for (node, desc) in nodes:
        if isinstance(node, (ast.ImportFrom, ast.Import)):
            valid = False
            print(f"WARNING: `{desc}` not allowed {node.lineno}:{node.col_offset}")
        if isinstance(node, (ast.Call)):
            if desc.startswith("__builtins__") and node.func.id in bad_ops:
                valid = False
                print(
                    f"WARNING: `{desc}()` not allowed {node.lineno}:{node.col_offset}"
                )
    # return valid
    return True


def bind_to_global_ast():
    # stdlib
    import sys

    sandbox = sys.modules["syft"].sandbox
    mylib = sandbox.mylib
    modules: List[Tuple[str, Any]] = [
        ("syft.sandbox", sandbox),
        ("syft.sandbox.mylib", mylib),
    ]

    classes: List[Tuple[str, str, Any]] = [
        ("syft.sandbox.mylib.Test", "syft.sandbox.mylib.Test", mylib.Test),
    ]

    methods: List[Tuple[str, str]] = [
        ("syft.sandbox.mylib.Test.hello", "syft.lib.python.String"),
    ]

    try:
        bind_ast("mylib", modules, classes, methods)
    except Exception as e:
        print("failed to bind ast", e)


# TODO: Ugly TEMP CODE PLAYGROUND


@bind_protobuf
class SecureExecMessage(ImmediateSyftMessageWithoutReply):
    def __init__(
        self,
        ast_tree: _ast.Module,
        address: Address,
        msg_id: Optional[UID] = None,
    ):
        super().__init__(address=address, msg_id=msg_id)
        self.ast_tree = ast_tree

    def _object2proto(self) -> SecureExecMessage_PB:
        return SecureExecMessage_PB(
            ast_tree=serialize(self.ast_tree),
            address=serialize(self.address),
            msg_id=serialize(self.id),
        )

    @staticmethod
    def _proto2object(proto: SecureExecMessage_PB) -> SecureExecMessage:
        return SecureExecMessage(
            ast_tree=_deserialize(blob=proto.ast_tree),
            address=_deserialize(blob=proto.address),
            msg_id=_deserialize(blob=proto.msg_id),
        )

    @staticmethod
    def get_protobuf_schema() -> GeneratedProtocolMessageType:
        return SecureExecMessage_PB


class SecureExecService(ImmediateNodeServiceWithoutReply):
    @staticmethod
    @service_auth(root_only=True)
    def process(
        node: AbstractNode, msg: SecureExecMessage, verify_key: VerifyKey
    ) -> None:
        debug(f"> Executing {type(msg)} {msg.pprint} on {node.pprint}")

        # try:
        print("=============================")
        print("Remote Secure Exec")
        print("=============================")
        nodes = parse_all_nodes(msg.ast_tree)
        if validate_nodes(nodes):
            print("Compiling...")
            exec(compile(msg.ast_tree, filename="<ast>", mode="exec"))  # nosec
            print("... compiled!")
            bind_to_global_ast()
            print("Accepting, code executed successfully!")
        else:
            print("Rejecting, code is insecure!")

        print("=============================")

        # except Exception as e:
        #     traceback(e)

    @staticmethod
    def message_handler_types() -> List[type]:
        return [SecureExecMessage]
