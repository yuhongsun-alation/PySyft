# stdlib
import functools
import inspect
from types import FunctionType

# syft relative
from . import sandboxed_proxy
from ... import lib_ast


@functools.singledispatch
def sendable(obj: object):
    raise TypeError("Object has to be either a function or a class.")


@sendable.register
def _(obj: type):
    pass


def validate_func(obj: FunctionType):
    signature = inspect.signature(obj)
    input_output_types = []

    for parameter_annotation in signature.parameters.values():
        annotation = parameter_annotation.annotation
        if annotation is parameter_annotation.empty:
            raise ValueError("Please annotate all parameters")

        input_output_types.append(annotation)

    if signature.return_annotation is signature.empty:
        raise ValueError("Please annotate the return type")

    input_output_types.append(signature.return_annotation)

    for elem in input_output_types:
        path = elem.__module__ + "." + elem.__name__
        lib_ast.query(path)


@sendable.register
def _(obj: FunctionType):
    validate_func(obj)
    return_annotation = inspect.signature(obj).return_annotation
    sandboxed_proxy.REGISTERED_FUNCTIONS[obj] = (
        return_annotation.__module__ + "." + return_annotation.__name__
    )
    setattr(sandboxed_proxy, obj.__name__, obj)
    return obj
