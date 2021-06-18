# third party
from pycolab import plot

# syft relative
from ... import deserialize
from ... import serialize
from ...generate_wrapper import GenerateWrapper
from ...lib.python import Dict
from ...proto.lib.pycolab.plot_pb2 import Plot as Plot_PB


def object2proto(obj: plot.Plot) -> Plot_PB:
    return Plot_PB(dict=serialize(Dict(obj.__dict__)))


def proto2object(proto: Plot_PB) -> plot.Plot:
    the_plot = plot.Plot()
    the_plot.__dict__ = deserialize(proto.dict).upcast()
    return the_plot


GenerateWrapper(
    wrapped_type=plot.Plot,
    import_path="pycolab.plot.Plot",
    protobuf_scheme=Plot_PB,
    type_object2proto=object2proto,
    type_proto2object=proto2object,
)
