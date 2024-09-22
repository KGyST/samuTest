from typing import Callable


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


def contentBasedHash(obj):
    """
    :param obj:
    :return:
    """
    hash_value = 0

    if hasattr(obj, '__dict__'):
        for key in sorted(obj.__dict__.keys()):
            if not isinstance(obj.__dict__[key], Callable):
                hash_value ^= contentBasedHash(key) ^ contentBasedHash(obj.__dict__[key])
    elif hasattr(obj, '__slots__'):
        for slot in sorted(obj.__slots__):
            if not isinstance(slot, Callable):
                hash_value ^= contentBasedHash(slot) ^ contentBasedHash(getattr(obj, slot))
    elif isinstance(obj, dict):
        for key in sorted(obj.keys()):
            hash_value ^= contentBasedHash(key) ^ contentBasedHash(obj[key])
    elif isinstance(obj, (list, set, )):
        for key in sorted(obj):
            hash_value ^= contentBasedHash(key)
    elif isinstance(obj, (int, float, str, bool, tuple, bytes, frozenset)):
        hash_value = hash(obj)
    else:
        hash_value = 0
    return hash_value

