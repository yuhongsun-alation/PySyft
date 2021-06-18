# third party
from pycolab import things

# syft relative
from ... import deserialize
from ... import serialize
from ...generate_wrapper import GenerateWrapper
from ...proto.lib.pycolab.backdrop_pb2 import Backdrop as Backdrop_PB


def object2proto(obj: things.Backdrop) -> Backdrop_PB:
    return Backdrop_PB(
        curtain=serialize(obj._c_u_r_t_a_i_n), palette=serialize(obj._p_a_l_e_t_t_e)
    )


def proto2object(proto: Backdrop_PB) -> things.Backdrop:
    return things.Backdrop(deserialize(proto.curtain), deserialize(proto.palette))


GenerateWrapper(
    wrapped_type=things.Backdrop,
    import_path="pycolab.things.Backdrop",
    protobuf_scheme=Backdrop_PB,
    type_object2proto=object2proto,
    type_proto2object=proto2object,
)
