# third party
from pycolab import engine

# syft relative
from ... import deserialize
from ... import serialize
from ...generate_wrapper import GenerateWrapper
from ...lib.python import Set
from ...proto.lib.pycolab.palette_pb2 import Palette as Palette_PB


def object2proto(obj: engine.Palette) -> Palette_PB:
    return Palette_PB(legal_characters=serialize(Set(obj._legal_characters)))


def proto2object(proto: Palette_PB) -> engine.Palette:
    return engine.Palette(deserialize(proto.legal_characters).upcast())


GenerateWrapper(
    wrapped_type=engine.Palette,
    import_path="pycolab.engine.Palette",
    protobuf_scheme=Palette_PB,
    type_object2proto=object2proto,
    type_proto2object=proto2object,
)
