from common.ICodec import ICodec
import hashlib
from common.constants import MAIN
from common.privateFunctions import _get_calling_module_name


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

    # def __setstate__(self, state):
    #     """
    #     Restore the object state including nested objects.
    #     """
    #     self.function = state.get('function')
    #     self.className = state.get('className')
    #     self.module = state.get('module')
    #     self.args = self._restore(state.get('args', []))
    #     self.kwargs = self._restore(state.get('kwargs', {}))
    #     self.preState = self._restore(state.get('preState'))
    #     self.postState = self._restore(state.get('postState'))
    #     self._sMD5 = state.get('_sMD5')
    #     self.name = state.get('name')
    #     self.path = state.get('path')

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
        return obj

    # def _restore(self, obj):
    #     """
    #     Recursively restore nested objects.
    #     """
    #     if isinstance(obj, dict):
    #         restored = {}
    #         for key, value in obj.items():
    #             if isinstance(value, dict) and 'py/object' in value:
    #                 # Handle nested objects with class metadata
    #                 class_path = value['py/object']
    #                 module_name, class_name = class_path.rsplit('.', 1)
    #                 module = __import__(module_name, fromlist=[class_name])
    #                 cls = getattr(module, class_name)
    #                 restored[key] = cls.__new__(cls)
    #                 restored[key].__setstate__(value)
    #             else:
    #                 restored[key] = self._restore(value)
    #         return restored
    #     elif isinstance(obj, list):
    #         return [self._restore(item) for item in obj]
    #     elif isinstance(obj, tuple):
    #         return tuple(self._restore(item) for item in obj)
    #     return obj


class StateBase:
    def __init__(self):
        self.selfOrClass = None
        self.globals = None

    def __eq__(self, other: "StateBase"):
        ...

    # def __getstate__(self):
    #     """
    #     Serialize the state of the base class including nested objects.
    #     """
    #     # state = {
    #     #     'py/object': f"{self.__class__.__module__}.{self.__class__.__name__}",
    #     #     'selfOrClass': ProgramState._flatten(self.selfOrClass),
    #     #     'globals': ProgramState._flatten(self.globals)
    #     # }
    #     state = self.__dict__.copy()
    #     return state

    # def __setstate__(self, state):
    #     """
    #     Restore the state of the base class including nested objects.
    #     """
    #     self.selfOrClass = ProgramState._restore(state.get('selfOrClass'))
    #     self.globals = ProgramState._restore(state.get('globals'))


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

