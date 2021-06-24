# stdlib
import asyncio
import curses
from typing import Any

# third party
import pycolab

# syft absolute
import syft as sy

import syft_ui as human_ui  # isort:skip


# helper functions for pointer resolution
def _resolve(tuple_ptr, size=1):
    resolved = []
    for i in range(size):
        resolved.append(tuple_ptr[i].resolve_pointer_type())
    return tuple(resolved)


def resolve(tuple_ptr):
    return _resolve(tuple_ptr, 3)


# These colours are only for humans to see in the CursesUi.
COLOUR_FG = {
    " ": (0, 0, 0),  # Inky blackness of SPAAAACE
    ".": (949, 929, 999),  # These stars are full of lithium
    "@": (999, 862, 110),  # Shimmering golden coins
    "#": (764, 0, 999),  # Walls of the SPACE MAZE
    "P": (0, 999, 999),  # This is you, the player
    "a": (999, 0, 780),  # Patroller A
    "b": (145, 987, 341),  # Patroller B
    "c": (987, 623, 145),
}  # Patroller C

COLOUR_BG = {".": (0, 0, 0), "@": (0, 0, 0)}  # Around the stars, inky blackness etc.

ui = human_ui.CursesUi(
    keys_to_actions={
        curses.KEY_UP: 0,
        curses.KEY_DOWN: 1,
        curses.KEY_LEFT: 2,
        curses.KEY_RIGHT: 3,
        -1: 4,
        "q": 5,
        "Q": 5,
    },
    delay=100,
    colour_fg=COLOUR_FG,
    colour_bg=COLOUR_BG,
)


class ProxyEngine:
    def __init__(self, engine: Any) -> None:
        self.engine_ptr = engine

    def __getattribute__(self, key: str) -> Any:
        if key == "engine_ptr":
            return super().__getattribute__(key)
        else:
            attr = self.engine_ptr.__getattribute__(key)
            if "Pointer" in type(attr).__name__:
                return attr.get()
            return attr


duet = sy.join_duet(loopback=True)

# wait for the game to be setup on the DM side
loop = asyncio.get_event_loop()
task = loop.create_task(asyncio.sleep(2))
loop.run_until_complete(task)

int_ptr = duet.python.Int(0)  # gives us permission as creator of the game
int_ptr.gc_enabled = False
game_ptr = duet.run(
    entrypoint="make_game", return_type="pycolab.engine.Engine", args=int_ptr
)
game_ptr.gc_enabled = False
proxy_game = ProxyEngine(game_ptr)
ui.play(proxy_game)
