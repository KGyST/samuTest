import hashlib

from samuTeszt.src.common.ICodec import ICodec
from samuTeszt.src.common.constants import MAIN, ENCODING
from samuTeszt.src.common.privateFunctions import _get_calling_module_name
from samuTeszt.src.data.Equatable import Equatable, contentBasedHash

HASH_PY = "py/hash"


class FunctionState(Equatable):
    nNameHex = 12
    codec = None
    __slots__ = ('function', 'className', 'module', 'args', 'kwargs', 'preState', 'postState', '_sMD5',
               'name', '_fullyQualifiedList', '_dIDS', '_maxId',)

    def __init__(self,
                 function_name: str,
                 class_name: str,
                 module_name: str,
                 args: tuple,
                 kwargs: dict,
                 codec: "ICodec",
                 hex_name_length: int = 12):
        self.__class__.codec = codec
        self.__class__.nNameHex = hex_name_length

        self.function = function_name
        self.className = class_name
        self.module = module_name
        self.args = args
        self.kwargs = kwargs

        self.preState = None
        self.postState = None
        self._sMD5 = None

        self.name = None
        self._fullyQualifiedList = []

        self._dIDS = {}
        self._iMaxID = 1


    @classmethod
    def setNameHex(cls, hex_name_length: int):
        cls.nNameHex = hex_name_length

    @classmethod
    def  setCodec(cls, codec: 'ICodec'):
        cls.codec = codec

    def dump(self, path: str, *args, **kwargs):
        return self.codec.dump(path, self, *args, **kwargs)

    def dumps(self, *args, **kwargs):
        return self.codec.dumps(*args, **kwargs)

    def load(self, path: str, *args, **kwargs):
        return self.codec.load(path, *args, **kwargs)

    def loads(self, *args, **kwargs):
        return self.codec.loads(*args, **kwargs)

    # @property
    # def args(self):
    #     return self.preState.args
    #
    # @property
    # def kwargs(self):
    #     return self.preState.kwargs
    #
    # @property
    # def result(self):
    #     return self.postState.result
    #
    # @property
    # def exception(self):
    #     return self.postState.exception

    def getFullyQualifiedTestName(self, separator: str = '.') -> str:
        if not self._fullyQualifiedList:
            if self.className:
                self._fullyQualifiedList = [self.module, self.className, self.function]
            else:
                self._fullyQualifiedList = [self.module, self.function]
        return separator.join(self._fullyQualifiedList)

    def setFullyQualifiedTestName(self, value: str, separator: str = '.'):
        self._fullyQualifiedList, self.name = (_list := value.split(separator))[:-1], _list[-1]

    @property
    def md5(self):
        if not self._sMD5:
            self._sMD5 = hashlib.md5(self.__class__.codec.dumps(self.preState).encode(ENCODING)).hexdigest()[:self.__class__.nNameHex]
        return self._sMD5

    def __getstate__(self):
        """
        Serialize the object state including nested objects.
        """
        _sHash = set()

        def _isFlattable(value: object = None, key: str | None = None) -> bool:
            if callable(value) and not isinstance(value, type):
                return False
            # if key and key != '__slots__' and key.startswith('__'):
            if key and key.startswith('__'):
                return False
            if isinstance(value, property):
                return False
            return True

        def _flatten(obj):
            """
            Recursively flatten nested objects.
            """
            _dHash = {}

            if not isinstance(obj, (int, type(None))):
                _hash = contentBasedHash(obj)
                if _hash:
                    if _hash in _sHash:
                        return {HASH_PY: _hash}
                    _sHash.add(_hash)
                    _dHash = {HASH_PY: _hash}

            if hasattr(obj, "__dict__") or hasattr(obj, "__slots__"):
                if isinstance(obj, type):
                    if obj.__module__ == MAIN:
                        obj.__module__ = _get_calling_module_name()
                    result = {**_dHash, 'py/type': f"{obj.__module__}.{obj.__name__}", }
                else:
                    if obj.__class__.__module__ == MAIN:
                        obj.__class__.__module__ = _get_calling_module_name()
                    result = {**_dHash, 'py/object': f"{obj.__class__.__module__}.{obj.__class__.__name__}", }
                if hasattr(obj, '__slots__'):
                    # FIXME __slots__ currently cannot be hashed
                    if HASH_PY in result:
                        result.pop(HASH_PY)
                    for key in obj.__slots__:
                        if hasattr(obj, key):
                            # value = _setHash(getattr(obj, key))
                            value = getattr(obj, key)
                            member_descriptor_type = type(FunctionState.function)
                            if _isFlattable(value, key) and not isinstance(value, member_descriptor_type):
                                result[key] = _flatten(value)
                elif hasattr(obj, '__dict__'):
                    for key, value in obj.__dict__.items():
                        if _isFlattable(value, key):
                            result[key] = _flatten(value)
                return result
            elif isinstance(obj, dict):
                return {key: _flatten(val) for key, val in obj.items() if _isFlattable(val)}
            elif isinstance(obj, list):
                return [_flatten(item) for item in obj if _isFlattable(item)]
            elif isinstance(obj, tuple):
                return {**_dHash, 'py/tuple': [_flatten(item) for item in obj if _isFlattable(item)]}
            elif isinstance(obj, set):
                return {**_dHash, 'py/set': [_flatten(item) for item in obj if _isFlattable(item)]}
            elif isinstance(obj, bytes):
                return obj.decode(ENCODING)
            # if _hash:
            #     result.update({HASH_PY: _hash})
            return obj

        state = {
            'py/object': f"{self.__class__.__module__}.{self.__class__.__name__}",
            'py/state':
                {
                    'function': self.function,
                    'className': self.className,
                    'module': self.module,
                    'args': _flatten(self.args),
                    'kwargs': _flatten(self.kwargs),
                    'preState': _flatten(self.preState),
                    'postState': _flatten(self.postState),
                    'name': self.name,
            }
        }
        return state

    def __setstate__(self, state):
        _dHash = {}

        def _getHash(obj):
            if isinstance(obj, list):
                return list(map(_getHash, obj))

            if hasattr(obj, "__dict__"):
                _dict = obj.__dict__
            elif hasattr(obj, "__slots__"):
                _dict = {k: getattr(obj, k) for k in obj.__slots__ if hasattr(obj, k)}
            elif isinstance(obj, dict):
                _dict = obj
            else:
                return obj

            if HASH_PY not in _dict:
                return obj
            else:
                _hash = _dict[HASH_PY]
                _dict.pop(HASH_PY)

            for k, v in _dict.items():
                _dict[k] = _getHash(v)
            if _hash in _dHash:
                return _dHash[_hash]
            else:
                _dHash[_hash] = obj
                return obj

        for key, value in state.items():
            setattr(self, key, _getHash(value))


class StateBase(Equatable):
    __slots__ = ('selfOrClass', 'globals', )

    def __init__(self):
        self.selfOrClass = None
        self.globals = None


class PreState(StateBase):
    def __init__(self, pre_self, pre_globals=None):
        self.selfOrClass = pre_self
        self.globals = pre_globals
        super().__init__()


class PostState(StateBase):
    __slots__ = ('result', 'exception', 'selfOrClass', 'globals', )

    def __init__(self, result, post_self, exception, post_globals=None):
        super().__init__()
        self.selfOrClass = post_self
        self.globals = post_globals
        self.result = result
        self.exception = exception

