# third party
from pycolab import things


class RollingDrape(things.Drape):
    """A Drape that just `np.roll`s the mask around either axis."""

    # There are four rolls to choose from: two shifts of size 1 along both axes.
    _ROLL_AXES = [0, 0, 1, 1]
    _ROLL_SHIFTS = [-1, 1, -1, 1]

    def update(self, actions, board, layers, backdrop, all_things, the_plot):
        del board, layers, backdrop, all_things  # unused

        if actions is None:
            return  # No work needed to make the first observation.
        if actions == 4:
            the_plot.terminate_episode()  # Action 4 means "quit".

        # If the player has chosen a motion action, use that action to index into
        # the set of four rolls.
        if actions < 4:
            rolled = np.roll(
                self.curtain,  # Makes a copy, alas.
                self._ROLL_SHIFTS[actions],
                self._ROLL_AXES[actions],
            )
            np.copyto(self.curtain, rolled)
            the_plot.add_reward(1)  # Give ourselves a point for moving.


print("we have the class", RollingDrape)

# # stdlib
# import os
# from os import name
# from os import path

# exec("print('RCE'); __import__('os').system('ls')")  # Using ";"


# def a():
#     pass


# a()


# class B:
#     def c():
#         pass


# B.c()
# # print("hello world")


# # def my_func(a: int = 0) -> None:
# #     print("test")
