import jsonpickle
from samuTeszt.src.data.Equatable import contentBasedHash
from pprint import pprint


HASH = "py/hash"


class ClassToBeNested:
    pass

class ClassTestee:
    def __getstate__(self):
        _sHash = set()

        def _setHash(obj):
            _hash = contentBasedHash(obj)
            if _hash in _sHash:
                return {HASH: _hash}
            _sHash.add(_hash)
            # try:
            #     for k, v in obj.__dict__.items():
            #         _sHash.add(contentBasedHash(k))
            # except AttributeError:
            #     pass
            return obj

        # _result = {}
        # for key, value in self.__dict__.items():
        #     _result[key] = _setHash(value)
        # return _result
        return {key: _setHash(value) for key, value in self.__dict__.items()}

    def __setstate__(self, state):
        _dHash = {}

        def _getHash(obj):
            try:
                if HASH in obj:
                    _hash = obj[HASH]
                    return _dHash[_hash]
            except TypeError:
                _hash = contentBasedHash(obj)
                _dHash[_hash] = obj
                return obj

        for key, value in state.items():
            state[key] = _getHash(value)
        self.__dict__ = state


original_json = '''
{
    "py/object": "__main__.ClassTestee", 
    "py/state": 
    {
        "instance_variable": 2, 
        "nestedInstance": 
        {
            "py/object": "__main__.ClassToBeNested",
            "nestedInstanceVariable":         
            {
                "py/object": "__main__.ClassToBeNested",
                "nestedInstanceVariable": 10
            }
        }, 
        "nestedInstance2": 
        {
            "py/object": "__main__.ClassToBeNested",
            "nestedInstanceVariable":         
            {
                "py/object": "__main__.ClassToBeNested",
                "nestedInstanceVariable": 10
            }
        }, 
        "_someProperty": 3, 
        "_somePrivateMember": 4
    }
}
'''

original_obj = jsonpickle.decode(original_json)

encode_ = jsonpickle.encode(original_obj)
pprint(encode_)

restored_obj = jsonpickle.decode(encode_)

print("Restored Object:")
print(vars(restored_obj))

