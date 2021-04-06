# stdlib

# third party
from fhir2dataset import Query

# syft relative
from ...generate_wrapper import GenerateWrapper
from ...proto.lib.fhir2dataset.query_pb2 import FHIRQuery as FHIRQuery_PB


def object2proto(obj: Query) -> FHIRQuery_PB:
    proto = FHIRQuery_PB(fhir_api_url=obj.fhir_api_url, token=obj.token)
    return proto


def proto2object(proto: FHIRQuery_PB) -> Query:
    query = Query(fhir_api_url=proto.fhir_api_url, token=proto.token)
    return query


GenerateWrapper(
    wrapped_type=Query,
    import_path="fhir2dataset.Query",
    protobuf_scheme=FHIRQuery_PB,
    type_object2proto=object2proto,
    type_proto2object=proto2object,
)
