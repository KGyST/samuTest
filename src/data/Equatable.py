from types import NoneType
from typing import Callable, Union, Any
from functools import reduce
from samuTeszt.src.common.constants import MAIN, ENCODING


class Equatable:
    """
    Class checking two objects are equal by members' value
    """
    def __eq__(self, other: 'Equatable'):
        if id(self) == id(other):
            return True
        return self.__hash__() == other.__hash__()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return contentBasedHash(self)


def contentBasedHash(obj: Any) -> int:
    """
    Generates a content-based hash value for an object.

    :param obj: The object to hash
    :return: Hash value
    """
    visited: [int, object] = {}

    FNV_PRIME = 0x01000193
    HASH_OF_NONE = 0x811c9dc5
    MASK = 0xffffffff

    def fnv1a_hash(value, key=None):
        assert isinstance(key, (str, NoneType))
        hash_value = HASH_OF_NONE
        hash_value ^= _contentBasedHash(value)
        hash_value *= FNV_PRIME
        if key:
            for byte in key.encode(ENCODING):
                hash_value ^= byte
                hash_value *= FNV_PRIME
        hash_value &= MASK
        return hash_value

    def _contentBasedHash(obj: Any):
        hash_value = HASH_OF_NONE

        if (obj_id := id(obj)) in visited:
            return visited[obj_id]

        if hasattr(obj, '__dict__'):
            for key in sorted(obj.__dict__.keys()):
                if not isinstance(obj.__dict__[key], Callable):
                    hash_value ^= fnv1a_hash(obj.__dict__[key], key)
        elif hasattr(obj, '__slots__'):
            for slot in sorted(obj.__slots__):
                # just for uninitalized __slots__ right after __new__
                if hasattr(obj, slot):
                    hash_value ^= fnv1a_hash(getattr(obj, slot), slot)
        elif isinstance(obj, dict):
            for key in sorted(obj.keys()):
                hash_value ^= fnv1a_hash(obj[key], key)
        elif isinstance(obj, (list, tuple, set)):
            for item in obj:
                hash_value ^= fnv1a_hash(item)
        elif isinstance(obj, (int, float, bool, bytes, frozenset)):
            hash_value = hash(obj)
        # elif isinstance(obj, str):
        #     hash_value = fnv1a_hash(None, obj)
        elif obj is None:
            hash_value = hash(None)
        else:
            hash_value = HASH_OF_NONE

        visited[obj_id] = hash_value
        return hash_value

    _result = _contentBasedHash(obj)
    if _result == HASH_OF_NONE:
        return None
    else:
        return _result
