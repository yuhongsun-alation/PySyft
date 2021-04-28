from typing import Callable
from enum import Enum

from syft.core.store.storeable_object import StorableObject

from ...logger import logger
from ..common.uid import UID

logger.level("STORE", no=15, color="<blue>", icon="@")


class StoreOP(Enum):
    GET = 1
    SET = 2
    CLEAR = 3
    DEL = 4


def _wrap_get(func: Callable) -> Callable:
    def get(self, key: UID):
        logger.log("STORE", f"STORE GET OP - ID {key} - STORE STATUS: {self.keys()}")
        result = func(self, key)
        return result
    return get


def _wrap_set(func: Callable) -> Callable:
    def set(self, key: UID, value: StorableObject):
        logger.log("STORE", f"STORE SET OP - ID {key} - VALUE {value} - STORE STATUS: {self.keys()}")
        result = func(self, key, value)
        logger.log("STORE", f"STORE SET RESULT - STORE STATUS: {self.keys()}")
        return result
    return set


def _wrap_del(func: Callable) -> Callable:
    def delete(self, key: UID):
        logger.log("STORE", f"STORE DEL OP - ID {key} - STORE STATUS: {self.keys()}")
        result = func(self, key)
        logger.log("STORE", f"STORE DEL RESULT - STORE STATUS: {self.keys()}")
        return result
    return delete


def _wrap_clear(func: Callable) -> Callable:
    def clear(self, *args, **kwargs):
        logger.log("STORE", "CLEAR OP - ID ???")
        return func(self, *args, **kwargs)

    return clear


def store_logger(op_type: StoreOP) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper():
            if op_type is StoreOP.GET:
                return _wrap_get(func)

            if op_type is StoreOP.SET:
                return _wrap_set(func)

            if op_type is StoreOP.DEL:
                return _wrap_del(func)

            if op_type is StoreOP.CLEAR:
                return _wrap_clear(func)

        return wrapper()

    return decorator
