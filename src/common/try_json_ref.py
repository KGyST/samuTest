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
            _dict = None
            if hasattr(obj, "__dict__"):
                _dict = obj.__dict__
            elif hasattr(obj, "__slots__"):
                _dict = {k: getattr(obj, k) for k in obj.__slots__}
            elif isinstance(obj, dict):
                _dict = obj
            _hash = contentBasedHash(obj)
            if _hash in _sHash:
                return {HASH: _hash}

            if _dict:
                for k, v in _dict.items():
                    _dict[k] = _setHash(v)
                _dict[HASH] = _hash
            elif isinstance(obj, list):
                obj = list(map(_setHash, obj))
            _sHash.add(_hash)
            return obj

        _result = {}
        try:
            for key, value in self.__dict__.items():
                _result[key] = _setHash(value)
        except Exception as e:
            print(e)
            raise
        return _result

    def __setstate__(self, state):
        _dHash = {}

        def _getHash(obj):
            if isinstance(obj, list):
                return list(map(_getHash, obj))

            if hasattr(obj, "__dict__"):
                _dict = obj.__dict__
            elif hasattr(obj, "__slots__"):
                _dict = {k: getattr(obj, k) for k in obj.__slots__}
            elif isinstance(obj, dict):
                _dict = obj
            else:
                return obj

            if not HASH in _dict:
                return obj
            else:
                _hash = _dict[HASH]
                _dict.pop(HASH)

            for key, value in _dict.items():
                _dict[key] = _getHash(value)
            if _hash in _dHash:
                return _dHash[_hash]
            else:
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
            "nestedObject1":         
            {
                "py/object": "__main__.ClassToBeNested",
                "nestedInstanceVariable": 10
            }
        }, 
        "nestedInstance2": 
        {
            "py/object": "__main__.ClassToBeNested",
            "nestedObject2":         
            {
                "py/object": "__main__.ClassToBeNested",
                "nestedObject21":         
                {
                    "py/object": "__main__.ClassToBeNested",
                    "nestedInstanceVariable": 10
                },
                "nestedObject22":         
                {
                    "py/object": "__main__.ClassToBeNested",
                    "nestedInstanceVariable": 10
                },
                "nestedObjectS":   
                [      
                    {
                        "py/object": "__main__.ClassToBeNested",
                        "nestedInstanceVariable": 10
                    } ,
                    {
                        "py/object": "__main__.ClassToBeNested",
                        "nestedInstanceVariable": 10
                    },      
                    {
                        "py/object": "__main__.ClassToBeNested",
                        "nestedInstanceVariable": 10
                    }
                ]
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
# print(vars(restored_obj))

