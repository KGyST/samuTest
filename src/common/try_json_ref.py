import jsonpickle
from samuTeszt.src.data.Equatable import contentBasedHash
from pprint import pprint


HASH = "py/hash"


class ClassToBeNested:
    pass

class ClassTestee:
    _dHash = {}

    def _getHash(self, obj):
        try:
            if HASH in obj:
                _hash = obj[HASH]
                hash_ = self.__class__._dHash[_hash]
                return hash_
        except Exception:
            _hash = contentBasedHash(obj)
            self.__class__._dHash[_hash] = obj
            return obj

    def __setstate__(self, state):
        for key, value in state.items():
            state[key] = self._getHash(value)
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__


modified_json = jsonpickle.encode(ClassTestee())

modified_json = '''
{
    "py/object": "__main__.ClassTestee", 
    "py/state": 
    {
    "instance_variable": 2, 
    "nestedInstance": 
        {
        "py/object": "__main__.ClassToBeNested",
        "nestedInstanceVariable": 10
        }, 
    "nestedInstance2": 
        {
        "py/hash": -3185606141063167895
        }, 
    "_someProperty": 3, 
    "_somePrivateMember": 4
    }
}
'''

# from pprint import pprint
# pprint(modified_json)

restored_obj = jsonpickle.decode(modified_json)

# print("Restored Object:")
# print(vars(restored_obj))

pprint(jsonpickle.encode(restored_obj))

