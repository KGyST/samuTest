import json
import jsonpickle

from samuTeszt.src.data.FunctionState import FunctionState
from samuTeszt.src.common.privateFunctions import open_and_create_folders
from samuTeszt.src.common.constants import MAIN, BUILTINS, MODULE_NAME
from samuTeszt.src.common.ICodec import ICodec

class JSONCodec(ICodec):
    sExt = ".json"
    _module = ""

    PY_OBJECT = 'py/object'
    PY_FUNCTION = 'py/function'
    PY_TYPE = 'py/type'

    @staticmethod
    def read(path: str) -> 'FunctionState':
        JSONCodec.find_and_import_classes(path)
        jf = open(path, "r").read()
        try:
            from samuTeszt.src.decorator import Dumper
            Dumper.bDump = False
            assert isinstance(_result := jsonpickle.loads(jf), FunctionState)
            return _result
        except Exception as e:
            # pass
            raise JSONCodec.StorageException(e)

    @staticmethod
    def reads(data: str) -> 'FunctionState':
        assert isinstance((_result := jsonpickle.loads(data)), FunctionState)
        return _result

    @staticmethod
    def dumps(data: 'FunctionState') -> str:
        from samuTeszt import Dumper
        Dumper.bDump = False
        _dumps = json.dumps(data.__getstate__(), indent=4)
        return _dumps

    @staticmethod
    def dump(path: str, data: 'FunctionState'):
        with open_and_create_folders(path, "w") as fOutput:
            fOutput.write(JSONCodec.dumps(data))

    @staticmethod
    def find_and_import_classes(path: str):
        """
        Import modules that define classes dumped in test cases
        Recursively calls _find_and_import_classes
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

