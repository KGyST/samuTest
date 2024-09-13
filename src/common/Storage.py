import unittest
from common.publicFunctions import *
from typing import Callable
from common.Collector import *
from common.ICodec import *
from common.privateFunctions import _get_original_function


class StorageTestSuite(unittest.TestSuite):
    def __init__(self,
                 path: str = TEST_ITEMS,
                 error_path: str = TEST_ITEMS+TEST_ERRORS,
                 collector=FileCollector,
                 codec=JSONCodec,
                 comparer_function: Callable = default_comparer_func,
                 ):
        """
        :param target_folder:
        """

        # self._tests is an inherited member!
        self._tests = []
        self.cData = codec
        self.fComparer = comparer_function
        self.sErrorPath = error_path

        for case in collector(path, codec):
            _item = StorageTestCase(case, self)
            self.addTest(_item)

        super().__init__(self._tests)


class StorageTestCase(unittest.TestCase):
    def __init__(self, data, suite):
        self.testData = data
        self.suite = suite

        func = self.StorageTestFunctionFactory()
        setattr(StorageTestCase, func.__name__, func)
        super().__init__(func.__name__)

    def _dump_data(self, result: dict):
        self.testData.update(result)
        self.suite.cData.dump(os.path.join(self.suite.sErrorPath, self.testData[PATH]), self.testData)
        raise

    def StorageTestFunctionFactory(self) -> 'Callable':
        def func(obj):
            testResult = None

            try:
                import importlib
                module = importlib.import_module(self.testData[MODULE_NAME])

                if CLASS_NAME in self.testData and self.testData[CLASS_NAME]:
                    _class = getattr(module, self.testData[CLASS_NAME])
                    _func = getattr(_class, self.testData[FUNC_NAME])
                else:
                    _func = getattr(module, self.testData[FUNC_NAME])
                _func =_get_original_function(_func)

                testResult = self.suite.fComparer(obj, _func, self.testData[ARGS], self.testData[KWARGS], self.testData[POST][RESULT])
            except Exception as e:
                if e.__class__ == self.testData[POST][EXCEPTION].__class__:
                    return
                elif e.__class__ == AssertionError:
                    self._dump_data({POST: {
                        RESULT: testResult,
                        EXCEPTION: None}
                        }
                    )
                else:
                    self._dump_data({POST: {
                        RESULT: None,
                        EXCEPTION: e, }
                        }
                    )
                return testResult
        func.__name__ = self.testData[NAME]

        return func

