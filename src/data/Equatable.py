class Equatable:
    """
    Class checking two objects are equal by members' value
    """
    def __eq__(self, other):
        return self.__class__._eq(self, other)

    @classmethod
    def _eq(cls, first, second):
        if first is second:
            return True
        if type(first) is not type(second):
            return False
        if hasattr(first, '__dict__'):
            if first.__dict__.keys() ^ second.__dict__.keys():
                return False
            for k in first.__dict__.keys():
                if not cls._eq(first.__dict__[k], second.__dict__[k]):
                    return False
        elif hasattr(first, '__slots__') and hasattr(second, '__slots__'):
            for slot in first.__slots__:
                if not cls._eq(getattr(first, slot), getattr(second, slot)):
                    return False
        elif isinstance(first, dict):
            if first.keys() ^ second.keys():
                return False
            for k in first.keys():
                if not cls._eq(first[k], second[k]):
                    return False
        elif isinstance(first, set) or isinstance(first, frozenset):
            return first == second
        elif isinstance(first, (list, tuple)):
            if len(first) != len(second):
                return False
            for value1, value2 in zip(first, second):
                if not cls._eq(value1, value2):
                    return False
        elif isinstance(first, (bytes, bytearray, memoryview, int, float, complex, str)):
            return first == second
        else:
            return first is second
        return True

    def __ne__(self, other):
        return not self == other

