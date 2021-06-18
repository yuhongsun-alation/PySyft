# stdlib
from typing import Any

# third party
from pycolab import things

# syft relative
from ... import deserialize
from ... import serialize
from ...generate_wrapper import GenerateWrapper
from ...proto.lib.pycolab.sprite_pb2 import Sprite as Sprite_PB


class DataSprite(things.Sprite):
    def __init__(self, *args: Any) -> None:
        self._visible = False
        pass

    def update(self, *args: Any) -> None:
        pass


def object2proto(obj: things.Sprite) -> Sprite_PB:
    thing = Sprite_PB()
    thing.obj_type = "pycolab.things.Sprite"

    get_set_map = {
        "visible": "_visible",
        "position": "_position",
        "curtain": "_c_u_r_t_a_i_n",
        "character": "_c_h_a_r_a_c_t_e_r",
        "corner": "_c_o_r_n_e_r",
    }

    character = getattr(obj, get_set_map["character"], None)
    if character is not None:
        thing.character = character

    visible = getattr(obj, get_set_map["visible"], None)
    if visible is not None:
        thing.visible = visible

    curtain = getattr(obj, get_set_map["curtain"], None)
    if curtain is not None:
        thing.curtain.CopyFrom(serialize(curtain))
        thing.has_curtain = True

    position = getattr(obj, get_set_map["position"], None)
    if position is not None:
        thing.position.CopyFrom(serialize(position))
        thing.has_position = True

    corner = getattr(obj, get_set_map["corner"], None)
    if corner is not None:
        thing.corner.CopyFrom(serialize(corner))
        thing.has_corner = True

    return thing


def proto2object(proto: Sprite_PB) -> things.Sprite:
    thing = DataSprite()

    get_set_map = {
        "visible": "_visible",
        "position": "_position",
        "curtain": "_c_u_r_t_a_i_n",
        "character": "_c_h_a_r_a_c_t_e_r",
        "corner": "_c_o_r_n_e_r",
    }

    setattr(thing, get_set_map["character"], proto.character)
    setattr(thing, get_set_map["visible"], proto.visible)

    if proto.has_curtain:
        setattr(thing, get_set_map["curtain"], deserialize(proto.curtain))

    if proto.has_position:
        setattr(thing, get_set_map["position"], deserialize(proto.position))

    if proto.has_corner:
        setattr(thing, get_set_map["corner"], deserialize(proto.corner))

    return thing


GenerateWrapper(
    wrapped_type=things.Sprite,
    import_path="pycolab.things.Sprite",
    protobuf_scheme=Sprite_PB,
    type_object2proto=object2proto,
    type_proto2object=proto2object,
)
