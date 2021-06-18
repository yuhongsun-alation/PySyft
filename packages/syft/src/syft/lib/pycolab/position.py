# third party
from pycolab import things

# syft relative
from ... import deserialize
from ... import serialize
from ...generate_wrapper import GenerateWrapper
from ...lib.python import Dict
from ...proto.lib.pycolab.position_pb2 import Position as Position_PB


def object2proto(obj: things.Sprite.Position) -> Position_PB:
    return Position_PB(position=serialize(Dict(obj._asdict())))


def proto2object(proto: Position_PB) -> things.Sprite.Position:
    return things.Sprite.Position(**deserialize(proto.position).upcast())


GenerateWrapper(
    wrapped_type=things.Sprite.Position,
    import_path="pycolab.things.Sprite",
    protobuf_scheme=Position_PB,
    type_object2proto=object2proto,
    type_proto2object=proto2object,
)
