# stdlib
import ast
import json
import os

# third party
from astpp import pdp


# from pprint import pprint
def pprint(args):
    attrs = dir(args)
    map = {}
    for i in attrs:
        if not i.startswith("__"):
            map[i] = type(getattr(args, i)).__name__
    print("*****************************")
    print("Type: ", type(args), "\n")
    print("Attrs:")
    print(json.dumps(map, indent=4, sort_keys=True))
    print("*****************************")


class FuncLister(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print(node.name)
        self.generic_visit(node)


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
denylist = [ast.Import, ast.ImportFrom]

# exec
# eval


def parse_all_nodes(tree):
    nodes = []
    for node in ast.walk(tree):
        print("node", node, type(node))
        if isinstance(node, ast.Call):
            print("call node", dir(node))
            pdp(node)
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
                pdp(node)
                raise ("Found a different Call type")
        if isinstance(node, ast.FunctionDef):
            print(node.name)
        if isinstance(node, ast.Import):
            imports = ",".join([name.name for name in node.names])
            nodes.append((node, f"import {imports}"))
        if isinstance(node, ast.ImportFrom):
            imports = ", ".join([name.name for name in node.names])
            nodes.append((node, f"from {node.module} import {imports}"))
    return nodes


code_path = os.path.abspath("code.py")


def validate_nodes(nodes):
    valid = True
    for (node, desc) in nodes:
        if isinstance(node, (ast.ImportFrom, ast.Import)):
            valid = False
            print(
                f"WARNING: `{desc}` not allowed {code_path}:{node.lineno}:{node.col_offset}"
            )
        if isinstance(node, (ast.Call)):
            if desc.startswith("__builtins__") and node.func.id in bad_ops:
                print(
                    f"WARNING: `{desc}()` not allowed {code_path}:{node.lineno}:{node.col_offset}"
                )
    return valid


code_str = ""
with open(code_path) as f:
    code_str = f.read()

print("RAW CODE")
print("=============================")
print(code_str)
print("=============================")
print("\n\n")

tree = ast.parse(code_str)
print("AST TREE")
print("=============================")
print(tree)
# FuncLister().visit(tree)
nodes = parse_all_nodes(tree)
validate_nodes(nodes)


print("=============================")
print("\n\n")


# print("CODE EXECUTION")
# print("=============================")
# exec(compile(tree, filename="<ast>", mode="exec"))
# print("=============================")


# class Call(func, args, keywords, starargs, kwargs)


# stdlib
import pickle

favorite_color = {"lion": "yellow", "kitty": "red"}

bt = pickle.dumps(tree)
# print(bt)

obj = pickle.loads(bt)
print(obj, type(obj), obj.__class__, obj.__module__)

# third party
import _ast

obj2 = _ast.Module()
obj2.body = obj
pdp(obj2)
assert obj2 == obj

exec(compile(obj, filename="<ast>", mode="exec"), {}, {})
