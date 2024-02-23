import unittest
from common.publicFunctions import *
from typing import Callable
from common.Collector import *
from common.Codec import *


class StorageTestSuite(unittest.TestSuite):
    def __init__(self,
                 path: str=TEST_ITEMS,
                 error_path:str=TEST_ERRORS,
                 collector= FileCollector,
                 codec = JSONCodec,
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
        self.testData  = data
        self.suite = suite

        func = self.StorageTestFunctionFactory()
        setattr(StorageTestCase, func.__name__, func)
        super().__init__(func.__name__)

    def _dump_data(self, result:dict):
        self.testData.update(result)
        self.suite.cData.dump(self.suite.sErrorPath, self.testData)
        raise

    def StorageTestFunctionFactory(self)-> 'Callable':
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

