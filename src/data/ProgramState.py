from common.ICodec import ICodec
import hashlib


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

    @property
    def md5(self):
        if self._sMD5:
            self._sMD5 = hashlib.md5(self.__class__.codec.dumps(self.preState).encode("ansi")).hexdigest()[:self.__class__.nNameHex]
        return self._sMD5

    def __getstate__(self):
        """
        Serialize the object state including nested objects.
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
            '_sMD5': self._sMD5
        }
        return state

    def __setstate__(self, state):
        """
        Restore the object state including nested objects.
        """
        self.function = state.get('function')
        self.className = state.get('className')
        self.module = state.get('module')
        self.args = self._restore(state.get('args', []))
        self.kwargs = self._restore(state.get('kwargs', {}))
        self.preState = self._restore(state.get('preState'))
        self.postState = self._restore(state.get('postState'))
        self._sMD5 = state.get('_sMD5')

    def _flatten(self, obj):
        """
        Recursively flatten nested objects.
        """
        if hasattr(obj, "__dict__"):
            data = {}
            for attr, value in obj.__dict__.items():
                if not callable(value) and not attr.startswith('__'):
                    data[attr] = self._flatten(value)
            return data
        elif isinstance(obj, dict):
            return {key: self._flatten(val) for key, val in obj.items()}
        elif isinstance(obj, list):
            return [self._flatten(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self._flatten(item) for item in obj)
        return obj

    def _restore(self, obj):
        """
        Recursively restore nested objects.
        """
        if isinstance(obj, dict):
            restored = {}
            for key, value in obj.items():
                if isinstance(value, dict) and 'py/object' in value:
                    # Handle nested objects with class metadata
                    class_path = value['py/object']
                    module_name, class_name = class_path.rsplit('.', 1)
                    module = __import__(module_name, fromlist=[class_name])
                    cls = getattr(module, class_name)
                    restored[key] = cls.__new__(cls)
                    restored[key].__setstate__(value)
                else:
                    restored[key] = self._restore(value)
            return restored
        elif isinstance(obj, list):
            return [self._restore(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self._restore(item) for item in obj)
        return obj


class StateBase:
    def __init__(self):
        self.selfOrClass = None
        self.globals = None

    def __eq__(self, other: "StateBase"):
        ...

    def __getstate__(self):
        """
        Serialize the state of the base class including nested objects.
        """
        state = {
            'py/object': f"{self.__class__.__module__}.{self.__class__.__name__}",
            'selfOrClass': ProgramState._flatten(self.selfOrClass),
            'globals': ProgramState._flatten(self.globals)
        }
        return state

    def __setstate__(self, state):
        """
        Restore the state of the base class including nested objects.
        """
        self.selfOrClass = ProgramState._restore(state.get('selfOrClass'))
        self.globals = ProgramState._restore(state.get('globals'))


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

