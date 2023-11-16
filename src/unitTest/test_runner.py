import unittest
import json
from common.publicFunctions import *
from common.privateFunctions import generateFolder, caseFileCollector, open_and_create_folders
from common.constants import *
import jsonpickle
from typing import Callable
from decorator.decorators import FunctionDumper


class JSONTestSuite(unittest.TestSuite):
    def __init__(self,
                 target_folder: str=TEST_ITEMS,
                 cases_only: str="",
                 filename_filter_func: Callable=filename_filter_func,
                 case_filter_func: Callable=case_filter_func,
                 comparer_func: Callable=default_comparer_func,
                 ):
        # self._tests is an inherited member!
        self._tests = []
        self._folder = os.path.join(target_folder, )
        FunctionDumper.doesDump = False
        generateFolder(TEST_ERRORS)

        for sFilePath in caseFileCollector(self._folder,
                                           case_filter_func,
                                           cases_only,
                                           filename_filter_func,
                                           ".json"):
            try:
                with open(os.path.join(self._folder, sFilePath), "r") as jf:
                    testData = jsonpickle.loads(jf.read())
                testCase = JSONTestCase(testData, self._folder, sFilePath, comparer_func)
                testCase.maxDiff = None
                self.addTest(testCase)
            except json.decoder.JSONDecodeError:
                print(f"JSONDecodeError - Filename: {sFilePath}")
                continue
        super().__init__(self._tests)

    def __contains__(self, p_Name: str):
        for test in self._tests:
            if test._testMethodName == p_Name:
                return True
        return False


class JSONTestCase(unittest.TestCase):
    def __init__(self, p_TestData, p_Dir: str, p_FileName: str, p_comparer: Callable):
        self.sDir = p_Dir
        self.sFile = p_FileName
        func = self.JSONTestCaseFactory(p_TestData, p_Dir, p_FileName, p_comparer)
        setattr(JSONTestCase, func.__name__, func)
        super().__init__(func.__name__)


    @staticmethod
    def JSONTestCaseFactory(test_data, p_Dir: str, p_FileName: str, p_comparer: Callable=default_comparer_func):
        def func(p_Obj):
            sOutFile = os.path.join(TEST_ERRORS, p_FileName)
            testResult = None

            try:
                import importlib
                module = importlib.import_module(test_data[MODULE_NAME])
                if CLASS_NAME in test_data and test_data[CLASS_NAME]:
                    _class = getattr(module, test_data[CLASS_NAME])
                    func = getattr(_class, test_data[FUNC_NAME])
                else:
                    func = getattr(module, test_data[FUNC_NAME])

                expectedResult = test_data[RESULT]

                p_comparer(p_Obj, func, test_data[ARGS], test_data[KWARGS], expectedResult)
            except Exception as e:
                # FIXME exception to json TypeError: Object of type ZeroDivisionError is not JSON serializable
                # "exception": JSONSeriazable(e)
                test_data.update({RESULT: testResult,})

                # try:
                with open_and_create_folders(sOutFile, "w") as fOutput:
                    json.dump(test_data, fOutput, indent=4)
                raise
        if NAME in test_data:
            func.__name__ = test_data[NAME]
        else:
            func.__name__ = "test_" + p_FileName[:-5]
        return func

