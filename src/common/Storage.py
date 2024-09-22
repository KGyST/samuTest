import unittest

from .Collector import *
from .JSONCodec import *
from .privateFunctions import _get_original_function
from .constants import *
from .publicFunctions import *
from samuTeszt.src.data.FileState import FileState


class FileTestSuite(unittest.TestSuite):
    def __init__(self,
                 path: str = TEST_ITEMS,
                 error_path: str = TEST_ITEMS+TEST_ERRORS,
                 collector=FileCollector,
                 codec: 'ICodec' = JSONCodec,
                 comparer_function: Callable = default_comparer_func,
                 ):
        """
        """
        # self._tests is an inherited member!
        self._tests = []
        self.codec = codec
        self.fComparer = comparer_function
        self.sErrorPath = error_path

        for case in collector(path, codec):
            _fileData = FileState(case, path, error_path)
            _item = FileTestCase(_fileData, self)
            self.addTest(_item)
        super().__init__(self._tests)


class FileTestCase(unittest.TestCase):
    def __init__(self, data: 'FileState', suite: 'FileTestSuite'):
        self.fileData = data
        self.testData = data.functionState
        self.suite = suite

        func = self.StorageTestFunctionFactory()
        setattr(FileTestCase, func.__name__, func)
        super().__init__(func.__name__)

    def StorageTestFunctionFactory(self) -> 'Callable':
        def func(obj):
            testResult = None

            try:
                import importlib
                module = importlib.import_module(self.testData.module)

                if self.testData.className:
                    _class = getattr(module, self.testData.className)
                    _func = getattr(_class, self.testData.function)
                else:
                    _func = getattr(module, self.testData.function)
                _func = _get_original_function(_func)

                testResult = self.suite.fComparer(obj, _func, self.testData.args, self.testData.kwargs, self.testData.postState.result)
            except Exception as e:
                _sPath = os.path.join(self.suite.sErrorPath)
                if e.__class__ == self.testData.postState.exception.__class__:
                    return
                elif e.__class__ == AssertionError:
                    self.testData.result = testResult
                    self.testData.exception = e
                    self.suite.codec.dump(self.fileData.sFullErrorPath, self.testData)
                    raise
                else:
                    self.testData.exception = e
                    self.suite.codec.dump(self.fileData.sFullErrorPath, self.testData)
                    raise
            return testResult
        func.__name__ = self.testData.getFullyQualifiedTestName()

        return func

