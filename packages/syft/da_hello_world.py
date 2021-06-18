# stdlib
import asyncio
import curses
from typing import Any

# third party
import pycolab

# syft absolute
import syft as sy

import syft_ui  # isort:skip


# helper functions for pointer resolution
def _resolve(tuple_ptr, size=1):
    resolved = []
    for i in range(size):
        resolved.append(tuple_ptr[i].resolve_pointer_type())
    return tuple(resolved)


def resolve(tuple_ptr):
    return _resolve(tuple_ptr, 3)


HELLO_COLOURS = {
    " ": (123, 123, 123),  # Only used in this program by
    "#": (595, 791, 928),  # the CursesUi.
    "@": (54, 501, 772),
    "1": (999, 222, 222),
    "2": (222, 999, 222),
    "3": (999, 999, 111),
    "4": (222, 222, 999),
}

ui = syft_ui.CursesUi(
    keys_to_actions={
        curses.KEY_UP: 0,
        curses.KEY_DOWN: 1,
        curses.KEY_LEFT: 2,
        curses.KEY_RIGHT: 3,
        "q": 4,
        "Q": 4,
        -1: 5,
    },
    delay=50,
    colour_fg=HELLO_COLOURS,
)


class ProxyEngine:
    def __init__(self, engine: Any) -> None:
        self.engine_ptr = engine

    def __getattribute__(self, key: str) -> Any:
        # print("trying to get ", key)
        if key == "engine_ptr":
            return super().__getattribute__(key)
        else:
            attr = self.engine_ptr.__getattribute__(key)
            # print("what", attr, type(attr))
            if "Pointer" in type(attr).__name__:
                return attr.get(request_block=True)
            return attr


duet = sy.join_duet(loopback=True)

# wait for the game to be setup on the DM side
loop = asyncio.get_event_loop()
task = loop.create_task(asyncio.sleep(2))
loop.run_until_complete(task)

game_ptr = duet.run(entrypoint="make_game", return_type="pycolab.engine.Engine")
game_ptr.gc_enabled = False
proxy_game = ProxyEngine(game_ptr)
ui.play(proxy_game)
