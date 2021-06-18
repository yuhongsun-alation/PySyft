# third party
from pycolab import plot

# syft relative
from ... import deserialize
from ... import serialize
from ...generate_wrapper import GenerateWrapper
from ...lib.python import List
from ...proto.lib.pycolab.enginedirectives_pb2 import (
    EngineDirectives as EngineDirectives_PB,
)


def object2proto(obj: plot.Plot) -> EngineDirectives_PB:
    return EngineDirectives_PB(
        z_updates=serialize(List(obj.z_updates)),
        summed_reward=obj.summed_reward,
        game_over=obj.game_over,
        discount=obj.discount,
    )


def proto2object(proto: EngineDirectives_PB) -> plot.Plot:
    ed = plot.Plot._EngineDirectives()
    ed.z_updates = deserialize(proto.z_updates).upcast()
    ed.summed_reward = proto.summed_reward
    ed.game_over = proto.game_over
    ed.discount = proto.discount
    return ed


GenerateWrapper(
    wrapped_type=plot.Plot._EngineDirectives,
    import_path="pycolab.plot.Plot._EngineDirectives",
    protobuf_scheme=EngineDirectives_PB,
    type_object2proto=object2proto,
    type_proto2object=proto2object,
)
