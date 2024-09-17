from common.privateFunctions import open_and_create_folders
import json
from common.constants import MAIN, BUILTINS, MODULE_NAME
import jsonpickle
from .ICodec import ICodec
from data.ProgramState import PostState, PreState, ProgramState


class ProgramStateHandler(jsonpickle.handlers.BaseHandler):
    def _flatten(self, obj):
        if hasattr(obj, "__dict__"):
            data = {}

            for attr, value in obj.__dict__.items():
                if not callable(value) and not attr.startswith('__') or attr.startswith('_'):
                    data[attr] = self._flatten(value)
            data.pop("__iter__", None)
            data.pop("__next__", None)

            return data
        elif isinstance(obj, dict):
            data = {}

            for attr, value in obj.items():
                if not callable(value) and not attr.startswith('__') or attr.startswith('_'):
                    data[attr] = self._flatten(value)
            return data
        elif isinstance(obj, list):
            data = []

            for value in obj:
                if not callable(value):
                    data.append(self._flatten(value))
            return data
        elif isinstance(obj, tuple):
            data = []

            for value in obj:
                if not callable(value):
                    data.append(self._flatten(value))
            return tuple(data)
        return obj


    def flatten(self, obj, data):
        data = {"py/object": f"{obj.__class__.__module__}.{obj.__class__.__name__}"}

        for attr, value in obj.__dict__.items():
            data[attr] = self._flatten(value)
        return data

    def _restore(self, obj, data):
        """
        Helper method to recursively restore attributes from flattened data.
        """
        if isinstance(data, dict):
            for attr, value in data.items():
                if isinstance(value, dict) and attr in obj.__dict__:
                    # Handle nested objects
                    nested_obj = obj.__dict__[attr]
                    self._restore(nested_obj, value)
                else:
                    setattr(obj, attr, value)
        elif isinstance(data, list):
            return [self._restore({}, value) for value in data]
        elif isinstance(data, tuple):
            return tuple(self._restore({}, value) for value in data)
        return data

    def restore(self, data):
        """
        Restore the object using the flattened data.
        """
        if 'className' in data and 'module' in data:
            module = __import__(data['module'])
            class_ = getattr(module, data['className'])
            obj = class_.__new__(class_)

            if 'args' in data:
                args_data = data['args'][0]
                self._restore(obj, args_data)
            if 'postState' in data and 'selfOrClass' in data['postState']:
                self._restore(obj, data['postState']['selfOrClass'])
            return obj
        return super().restore(data)

# jsonpickle.handlers.register(ProgramState, ProgramStateHandler)

class JSONCodec(ICodec):
    sExt = ".json"
    _module = ""

    PY_OBJECT = 'py/object'
    PY_FUNCTION = 'py/function'
    PY_TYPE = 'py/type'

    @staticmethod
    def read(path: str) -> 'ProgramState':
        JSONCodec.find_and_import_classes(path)
        jf = open(path, "r").read()
        try:
            from decorator import Dumper
            Dumper.bDump = False
            return jsonpickle.loads(jf)
        except Exception as e:
            raise JSONCodec.StorageException(e)

    @staticmethod
    def reads(data: str) -> 'ProgramState':
        return jsonpickle.loads(data)

    @staticmethod
    def dumps(data) -> str:
        from decorator import Dumper
        Dumper.bDump = False
        while True:
            try:
                _dumps = jsonpickle.dumps(data, indent=4, include_properties=True)
                break
            except AttributeError as e:
                setattr(e.obj, e.name, None)
        return _dumps
        # return JSONCodec.clean(_dumps)

    @staticmethod
    def dump(path: str, data: dict):
        with open_and_create_folders(path, "w") as fOutput:
            fOutput.write(JSONCodec.dumps(data))

    @staticmethod
    def find_and_import_classes(path: str):
        """
        Import modules that define classes dumped in test cases
        Recursively calls _find_and_import_classes
        FIXME to abstract not to be json-dependent
        :param path: test case data file path
        :return: None
        """
        with open(path, "r") as jf:
            importData = json.loads(jf.read())
            JSONCodec._find_and_import_classes(importData)

    @staticmethod
    def _find_and_import_classes(importData):
        """
        Recursor called by find_and_import_classes
        :param importData:
        :return: None
        """
        import importlib

        if isinstance(importData, dict):
            if JSONCodec.PY_OBJECT in importData:
                class_path = importData[JSONCodec.PY_OBJECT]
                module_name, class_name = class_path.rsplit('.', 1)
                try:
                    module = importlib.import_module(module_name)
                    if module_name != BUILTINS:
                        getattr(module, class_name)  # Ensure the class is loaded
                except (ImportError, AttributeError) as e:
                    print(f"Error importing {class_path}: {e}")
            for key, value in importData.items():
                JSONCodec._find_and_import_classes(value)
        elif isinstance(importData, list):
            for item in importData:
                JSONCodec._find_and_import_classes(item)

    @staticmethod
    def clean(j: str):
        dJson = json.loads(j)
        JSONCodec._module = dJson[MODULE_NAME]
        dJson = JSONCodec._clean(dJson)
        return json.dumps(dJson, indent=4)

    @staticmethod
    def _clean(element):
        if isinstance(element, dict):
            _dElement = {}
            for k, item in element.items():
                if not JSONCodec._isBuiltin(item):
                    if k == JSONCodec.PY_OBJECT or k == JSONCodec.PY_FUNCTION or k == JSONCodec.PY_TYPE:
                        if item.startswith(MAIN):
                            item = str.replace(item, MAIN, JSONCodec._module)
                    item = JSONCodec._clean(item)
                    _dElement[k] = item
            element = _dElement
        elif isinstance(element, list) or isinstance(element, tuple):
            _lElement = []
            for item in element:
                if not JSONCodec._isBuiltin(item):
                    item = JSONCodec._clean(item)
                    _lElement.append(item)
            element = _lElement
            if isinstance(element, tuple):
                element = tuple(element)
        return element

    @staticmethod
    def _isBuiltin(item):
        if isinstance(item, dict):
            if JSONCodec.PY_OBJECT in item:
                if item[JSONCodec.PY_OBJECT].startswith(BUILTINS):
                    return True
        return False

