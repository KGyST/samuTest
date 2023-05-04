import unittest
import os
import shutil
import json
from common.publicFunctions import *
from common.privateFunctions import generateFolder, caseFileCollector
from common.constants import ERROR_STR


class JSONTestSuite(unittest.TestSuite):
    def __init__(self,
                 func,
                 target_folder:str=".",
                 cases_only:str="",
                 filename_filter_func=filename_filter_func,
                 case_filter_func=case_filter_func,
                 comparer_func=default_comparer_func,
                 ):
        # self._tests is an inherited member!
        self._tests = []
        self._folder = os.path.join(target_folder, func.__name__, )
        generateFolder(self._folder + ERROR_STR)
        for sFile in caseFileCollector(self._folder,
                                          case_filter_func,
                                          cases_only,
                                          filename_filter_func,
                                          ".json"):
            try:
                testData = json.load(open(os.path.join(self._folder, sFile), "r"))
                testCase = JSONTestCase(func, testData, self._folder, sFile, comparer_func)
                testCase.maxDiff = None
                self.addTest(testCase)
            except json.decoder.JSONDecodeError:
                print(f"JSONDecodeError - Filename: {sFile}")
                continue
        super(JSONTestSuite, self).__init__(self._tests)

    def __contains__(self, p_Name):
        for test in self._tests:
            if test._testMethodName == p_Name:
                return True
        return False


class JSONTestCase(unittest.TestCase):
    def __init__(self, p_function, p_TestData, p_Dir, p_FileName, p_comparer):
        self.sDir = p_Dir
        self.sFile = p_FileName
        func = self.JSONTestCaseFactory(p_function, p_TestData, p_Dir, p_FileName, p_comparer)
        setattr(JSONTestCase, func.__name__, func)
        super(JSONTestCase, self).__init__(func.__name__)

    @staticmethod
    def JSONTestCaseFactory(p_function, p_TestData, p_Dir, p_FileName, p_comparer=default_comparer_func):
        def func(p_Obj):
            sOutFile = os.path.join(p_Dir + ERROR_STR, p_FileName)
            testResult = None

            try:
                p_comparer(p_Obj, p_function, p_TestData, file_name=p_FileName)
            except AssertionError:
                with open(sOutFile, "w") as fOutput:
                    p_TestData.update({"result": testResult})
                    json.dump(p_TestData, fOutput, indent=4)
                raise

        if "name" in p_TestData:
            func.__name__ = p_TestData["name"]
        else:
            func.__name__ = "test_" + p_FileName[:-5]
        return func

