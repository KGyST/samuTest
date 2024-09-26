from typing import Callable, Union, Any
from functools import reduce

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

def contentBasedHash(obj: Any, visited=None) -> int:
    """
    Generates a content-based hash value for an object.

    :param obj: The object to hash
    :param visited: Set of already visited objects to prevent circular references
    :return: Hash value
    """
    if visited is None:
        visited = set()

    if (obj_id := id(obj)) in visited:
        return 0
    visited.add(obj_id)

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
        hash_value = reduce(lambda acc, b: hash((acc, b)), obj.encode('utf-8'), 0)
    elif obj is None:
        hash_value = hash(None)
    else:
        hash_value = 0

    return hash_value

