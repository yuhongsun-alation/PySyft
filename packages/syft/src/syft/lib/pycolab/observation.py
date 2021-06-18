# third party
from pycolab import rendering

# syft relative
from ... import deserialize
from ... import serialize
from ...generate_wrapper import GenerateWrapper
from ...lib.python import Dict
from ...proto.lib.pycolab.observation_pb2 import Observation as Observation_PB


def object2proto(obj: rendering.Observation) -> Observation_PB:
    return Observation_PB(
        board=serialize(obj.board), layers=serialize(Dict(obj.layers))
    )


def proto2object(proto: Observation_PB) -> rendering.Observation:
    return rendering.Observation(
        board=deserialize(proto.board), layers=deserialize(proto.layers).upcast()
    )


GenerateWrapper(
    wrapped_type=rendering.Observation,
    import_path="pycolab.rendering.Observation",
    protobuf_scheme=Observation_PB,
    type_object2proto=object2proto,
    type_proto2object=proto2object,
)
