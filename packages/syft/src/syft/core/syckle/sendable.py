# stdlib
import ast
import inspect
import re
import sys
from typing import Any
from typing import Callable
from typing import Type
from typing import Union

# third party
from IPython.core.magics.code import extract_symbols
import biwrap


# monkeypatch inspect
def new_getfile(object: object, _old_getfile: Callable = inspect.getfile) -> str:
    if not inspect.isclass(object):
        return _old_getfile(object)

    # Lookup by parent module (as in current inspect)
    if hasattr(object, "__module__"):
        object_ = sys.modules.get(object.__module__)
        filename = getattr(object_, "__file__", None)
        if filename is not None:
            return filename

    # If parent module is __main__, lookup by methods (NEW)
    for _, member in inspect.getmembers(object):
        if (
            inspect.isfunction(member)
            and getattr(object, "__qualname__", "") + "." + member.__name__
            == member.__qualname__
        ):
            return inspect.getfile(member)
    else:
        raise TypeError(f"Source for {object!r} not found")


inspect.getfile = new_getfile


def get_code(obj: object) -> str:
    try:
        return inspect.getsource(obj)  # type: ignore
    except Exception:
        # in case we're looking for a class that was generated within a
        # Jupyter notebook we use the following
        cell_code = "".join(inspect.linecache.getlines(new_getfile(obj)))  # type: ignore
        class_code = extract_symbols(cell_code, getattr(obj, "__name__", ""))[0][0]
        return class_code


class ClassCode:
    def __init__(self, entrypoint: str, return_type: str, code: str) -> None:
        self.code = code
        self.entrypoint = entrypoint
        self.return_type = return_type

    def send(self, client: Any) -> None:
        tree = ast.parse(self.code)
        client.secure_exec(
            entrypoint=self.entrypoint, return_type=self.return_type, ast_tree=tree
        )
        print(self.usage_code())

    def usage_code(self) -> str:
        return (
            "Give this to your DS:\n"
            + "ptr = client.run(\n"
            + f'    entrypoint="{self.entrypoint}",\n'
            + f'    return_type="{self.return_type}"\n'
            + ")"
        )

    def __repr__(self) -> str:
        return self.code


@biwrap.biwrap
def sendable(
    func_or_class: Union[Callable, Type], return_type: str = "syft.lib.python._SyNone"
) -> ClassCode:
    strip_decorator = re.sub(r"@.+sendable.+\n", "", get_code(func_or_class))
    return ClassCode(
        entrypoint=func_or_class.__name__, return_type=return_type, code=strip_decorator
    )
