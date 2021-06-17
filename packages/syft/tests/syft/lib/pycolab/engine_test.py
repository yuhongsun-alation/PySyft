# third party
import pytest

# syft absolute
import syft as sy
from syft import deserialize
from syft import serialize


@pytest.mark.vendor(lib="pycolab")
def test_engine_serde() -> None:
    # third party
    from pycolab import engine

    game = engine.Engine(rows=10, cols=10, occlusion_in_layers=True)

    game_ser = serialize(game)


# crap game
# from pycolab import ascii_art
# from pycolab import things

# ART = ["1@"]

# def make_game():
#     """Builds and returns a Hello World game."""
#     return ascii_art.ascii_art_to_game(
#         ART,
#         what_lies_beneath=" ",
#         sprites={
#             "1": ascii_art.Partial(SlidingSprite, 0),
#         },
#         drapes={"@": RollingDrape},
#         z_order="1@",
#     )


# class RollingDrape(things.Drape):
#     def update(self, *args):
#         pass


# class SlidingSprite(things.Sprite):
#     def __init__(self, *args):
#         self._visible = False
#         pass

#     def update(self, *args):
#         pass


# game = make_game()
# a = game.its_showtime()
# print(a)
# b = game.play("0")
# print(b)
# print(game.game_over)
