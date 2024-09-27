from typing import Callable, Union, Any
from functools import reduce
from samuTeszt.src.common.constants import MAIN, ENCODING


class Equatable:
    """
    Class checking two objects are equal by members' value
    """
    def __eq__(self, other: 'Equatable'):
        return self.__hash__() == other.__hash__()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return contentBasedHash(self)

def fnv1a_hash(string):
    FNV_prime = 0x01000193
    hash_value = 0x811c9dc5
    for byte in string.encode(ENCODING):
        hash_value ^= byte
        hash_value *= FNV_prime
        hash_value &= 0xffffffff
    return hash_value

def contentBasedHash(obj: Any, visited=None) -> int:
    """
    Generates a content-based hash value for an object.

    :param obj: The object to hash
    :param visited: Set of already visited objects to prevent circular references
    :return: Hash value
    """
    # if visited is None:
    #     visited = {}
    #
    # if (obj_id := id(obj)) in visited:
    #     return visited[obj_id]

    hash_value = 0

    if hasattr(obj, '__dict__'):
        for key in sorted(obj.__dict__.keys()):
            if not isinstance(obj.__dict__[key], Callable):
                hash_value ^= contentBasedHash(key, visited) ^ contentBasedHash(obj.__dict__[key], visited)
    elif hasattr(obj, '__slots__'):
        for slot in sorted(obj.__slots__):
            # just for uninitalized __slots__ right after __new__
            if hasattr(obj, slot):
                hash_value ^= contentBasedHash(slot, visited) ^ contentBasedHash(getattr(obj, slot), visited)
    elif isinstance(obj, dict):
        for key in sorted(obj.keys()):
            hash_value ^= contentBasedHash(key, visited) ^ contentBasedHash(obj[key], visited)
    elif isinstance(obj, (list, set)):
        for item in obj:
            hash_value ^= contentBasedHash(item, visited)
    elif isinstance(obj, (int, float, bool, tuple, bytes, frozenset)):
        hash_value = hash(obj)
    elif isinstance(obj, str):
        hash_value = fnv1a_hash(obj)
    elif obj is None:
        hash_value = hash(None)
    else:
        hash_value = 0

    # visited[obj_id] = hash_value
    return hash_value

