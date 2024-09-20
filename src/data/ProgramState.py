import hashlib

from ..common.ICodec import ICodec
from ..common.constants import MAIN
from ..common.privateFunctions import _get_calling_module_name


class ProgramState:
    nNameHex = None
    codec = None

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
        self.path = None

    def dump(self, *args, **kwargs):
        return self.codec.dump(self.path, self, *args, **kwargs)

    def dumps(self, *args, **kwargs):
        return self.codec.dumps(*args, **kwargs)

    def load(self, *args, **kwargs):
        return self.codec.load(self.path, *args, **kwargs)

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

    @property
    def md5(self):
        if self._sMD5:
            self._sMD5 = hashlib.md5(self.__class__.codec.dumps(self.preState).encode("ansi")).hexdigest()[:self.__class__.nNameHex]
        return self._sMD5

    def __getstate__(self):
        """
        Serialize the object state including nested objects.
        Currently only for json
        """
        state = {
            'py/object': f"{self.__class__.__module__}.{self.__class__.__name__}",
            'function': self.function,
            'className': self.className,
            'module': self.module,
            'args': self._flatten(self.args),
            'kwargs': self._flatten(self.kwargs),
            'preState': self._flatten(self.preState),
            'postState': self._flatten(self.postState),
            'name': self.name,
            'path': self.path,
        }
        return state

    def _isFlattable(self, value: object = None, key: str | None = None) -> bool:
        if callable(value) and not isinstance(value, type):
            return False
        if key and key.startswith('__'):
            return False
        if isinstance(value, property):
            return False
        return True

    def _flatten(self, obj):
        """
        Recursively flatten nested objects.
        """
        if hasattr(obj, "__dict__"):
            if isinstance(obj, type):
                if obj.__module__ == MAIN:
                    obj.__module__ = _get_calling_module_name()
                data = {'py/type': f"{obj.__module__}.{obj.__name__}",}
            else:
                if obj.__class__.__module__ == MAIN:
                    obj.__class__.__module__ = _get_calling_module_name()
                data = {'py/object': f"{obj.__class__.__module__}.{obj.__class__.__name__}",}
            for key, value in obj.__dict__.items():
                if self._isFlattable(value, key):
                    data[key] = self._flatten(value)
            return data
        elif isinstance(obj, dict):
            return {key: self._flatten(val) for key, val in obj.items() if self._isFlattable(val)}
        elif isinstance(obj, list):
            return [self._flatten(item) for item in obj if self._isFlattable(item)]
        elif isinstance(obj, tuple):
            return {'py/tuple': [self._flatten(item) for item in obj if self._isFlattable(item)]}
        elif isinstance(obj, set):
            return {'py/set': [self._flatten(item) for item in obj if self._isFlattable(item)]}
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')
        return obj


class StateBase:
    def __init__(self):
        self.selfOrClass = None
        self.globals = None

    def __eq__(self, other: "StateBase"):
        ...


class PreState(StateBase):
    def __init__(self, pre_self, pre_globals=None):
        self.selfOrClass = pre_self
        self.globals = pre_globals
        super().__init__()


class PostState(StateBase):
    def __init__(self, result, post_self, exception, post_globals=None):
        super().__init__()
        self.result = result
        self.selfOrClass = post_self
        self.exception = exception
        self.globals = post_globals

