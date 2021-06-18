# stdlib
import functools
from typing import Any as TypeAny
from typing import List as TypeList
from typing import Tuple as TypeTuple

# third party
import pycolab
from pycolab import ascii_art
from pycolab import engine
from pycolab import plot
from pycolab import prefab_parts
from pycolab import rendering
from pycolab import things
from pycolab.prefab_parts import drapes
from pycolab.prefab_parts import sprites

# syft relative
from . import backdrop  # noqa: 401
from . import drape  # noqa: 401
from . import enginedirectives  # noqa: 401
from . import observation  # noqa: 401
from . import palette  # noqa: 401
from . import position  # noqa: 401
from . import sprite  # noqa: 401
from . import the_plot  # noqa: 401
from ...ast import add_classes
from ...ast import add_methods
from ...ast import add_modules
from ...ast.globals import Globals
from ..util import generic_update_ast

LIB_NAME = "pycolab"
PACKAGE_SUPPORT = {"lib": LIB_NAME}


def create_ast(client: TypeAny = None) -> Globals:
    ast = Globals(client)
    # pycolab.rendering.Observation
    modules: TypeList[TypeTuple[str, TypeAny]] = [
        ("pycolab", pycolab),
        ("pycolab.engine", engine),
        ("pycolab.ascii_art", ascii_art),
        ("pycolab.things", things),
        ("pycolab.prefab_parts", prefab_parts),
        ("pycolab.prefab_parts.drapes", drapes),
        ("pycolab.prefab_parts.sprites", sprites),
        ("pycolab.rendering", rendering),
        ("pycolab.plot", plot),
    ]

    classes: TypeList[TypeTuple[str, str, TypeAny]] = [
        ("pycolab.plot.Plot", "pycolab.plot.Plot", plot.Plot),
        ("pycolab.engine.Engine", "pycolab.engine.Engine", engine.Engine),
        ("pycolab.engine.Palette", "pycolab.engine.Palette", engine.Palette),
        ("pycolab.ascii_art.Partial", "pycolab.ascii_art.Partial", ascii_art.Partial),
        ("pycolab.things.Backdrop", "pycolab.things.Backdrop", things.Backdrop),
        ("pycolab.things.Drape", "pycolab.things.Drape", things.Drape),
        ("pycolab.things.Sprite", "pycolab.things.Sprite", things.Sprite),
        # (
        #     "pycolab.things.Sprite.Position",
        #     "pycolab.things.Sprite.Position",
        #     things.Sprite.Position,
        # ),
        (
            "pycolab.prefab_parts.drapes.Scrolly",
            "pycolab.prefab_parts.drapes.Scrolly",
            drapes.Scrolly,
        ),
        (
            "pycolab.prefab_parts.sprites.MazeWalker",
            "pycolab.prefab_parts.sprites.MazeWalker",
            sprites.MazeWalker,
        ),
        (
            "pycolab.rendering.Observation",
            "pycolab.rendering.Observation",
            rendering.Observation,
        ),
    ]

    methods: TypeList[TypeTuple[str, str]] = [
        ("pycolab.ascii_art.ascii_art_to_game", "pycolab.engine.Engine"),
        ("pycolab.things.Drape.update", "syft.lib.python._SyNone"),
        ("pycolab.things.Sprite.update", "syft.lib.python._SyNone"),
        ("pycolab.engine.Engine.its_showtime", "syft.lib.python.Tuple"),
        ("pycolab.engine.Engine.play", "syft.lib.python.Tuple"),
        ("pycolab.engine.Engine.game_over", "syft.lib.python.Bool"),
        ("pycolab.engine.Engine.things", "syft.lib.python.Dict"),
        ("pycolab.engine.Engine.rows", "syft.lib.python.Int"),
        ("pycolab.engine.Engine.cols", "syft.lib.python.Int"),
        ("pycolab.engine.Engine.backdrop", "pycolab.things.Backdrop"),
        ("pycolab.engine.Engine.the_plot", "pycolab.plot.Plot"),
        ("pycolab.things.Backdrop.palette", "pycolab.engine.Palette"),
    ]

    add_modules(ast, modules)
    add_classes(ast, classes)
    add_methods(ast, methods)

    for klass in ast.classes:
        klass.create_pointer_class()
        klass.create_send_method()
        klass.create_storable_object_attr_convenience_methods()

    return ast


update_ast = functools.partial(generic_update_ast, LIB_NAME, create_ast)
