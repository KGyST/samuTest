import glob
import unittest
from common.publicFunctions import *
from common.privateFunctions import open_and_create_folders
from common.constants import *
import jsonpickle
from typing import Callable


class JSONStorage:
    ext = ".json"

    class StorageException(Exception):
        pass

    @staticmethod
    def read(path:str)->dict:
        with open(path, "r") as jf:
            try:
                return jsonpickle.loads(jf.read())
            except Exception:
                raise JSONStorage.StorageException()

    @staticmethod
    def dump(path:str, data:dict):
        with open_and_create_folders(path, "w") as fOutput:
            fOutput.write(jsonpickle.dumps(data, indent=4, make_refs=False, include_properties=True))


class FileCollector():
    def __init__(self, path:str, encoder):
        self.sFolderPath = path
        self._index = -1
        self._caseS = []
        if os.path.exists(self.sFolderPath):
            sCaseS = glob.glob('**/*' + encoder.ext, root_dir=self.sFolderPath, recursive=True)
            for _sCase in sCaseS:
                _dCase = encoder.read(os.path.join(self.sFolderPath, _sCase) )
                if NAME not in _dCase:
                    _dCase[NAME] = os.path.splitext(".".join(_sCase.split(os.path.sep)))[0]
                    self._caseS.append(_dCase)

    def __iter__(self)->'FileCollector':
        return self

    def __next__(self)->dict:
        self._index += 1

        if self._index < len(self._caseS):
            return self._caseS[self._index]
        else:
            raise StopIteration


class StorageTestSuite(unittest.TestSuite):
    def __init__(self,
                 path: str=TEST_ITEMS,
                 error_path:str=TEST_ERRORS,
                 collector= FileCollector,
                 encoder = JSONStorage,
                 comparer_function: Callable = default_comparer_func,
                 ):
        """
        :param target_folder:
        """
        # self._tests is an inherited member!
        self._tests = []
        self.cData = encoder
        self.fComparer = comparer_function
        self.sErrorPath = error_path

        for case in collector(path, encoder):
            _item = StorageTestCase(case, self)
            self.addTest(_item)

        super().__init__(self._tests)


class StorageTestCase(unittest.TestCase):
    def __init__(self, data, suite):
        self.testData  = data
        self.suite = suite

        func = self.StorageTestCaseFactory()
        setattr(StorageTestCase, func.__name__, func)
        super().__init__(func.__name__)

    def _dump_data(self, result:dict):
        self.testData.update(result)
        self.suite.cData.dump(self.suite.sErrorPath, self.testData)
        raise

    def StorageTestCaseFactory(self)-> 'Callable':
        def func(object):
            testResult = None

            try:
                import importlib
                module = importlib.import_module(self.testData[MODULE_NAME])

                if CLASS_NAME in self.testData and self.testData[CLASS_NAME]:
                    _class = getattr(module, self.testData[CLASS_NAME])
                    func = getattr(_class, self.testData[FUNC_NAME])
                else:
                    func = getattr(module, self.testData[FUNC_NAME])

                self.suite.fComparer(object, func, self.testData[ARGS], self.testData[KWARGS], self.testData[RESULT])
            except AssertionError:
                self._dump_data({RESULT: testResult,})
            except Exception as e:
                self._dump_data({EXCEPTION: e, })

        func.__name__ = self.testData[NAME]

        return func

