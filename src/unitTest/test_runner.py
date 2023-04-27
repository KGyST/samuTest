import unittest
import os
import shutil
import json
from common.commonFunctions import *
from common.private import folderHandler, caseFileCollector

class JSONTestSuite(unittest.TestSuite):
    def __init__(self,
                 cases_folder:str,
                 function,
                 cases_only:str="",
                 filename_filter_func=filename_filter_func,
                 case_filter_func=case_filter_func,
                 comparer_func=default_comparer_func,
                 first_run:bool=False):
        self._tests = []
        #FIXME check if folder doesn't exist:
        self._folder = cases_folder
        folderHandler(self._folder)
        for fileName in caseFileCollector(self._folder,
                                          case_filter_func,
                                          cases_only,
                                          filename_filter_func,
                                          ".json"):
            try:
                testData = json.load(open(os.path.join(self._folder, fileName), "r"))
                testCase = JSONTestCase(function, testData, self._folder, fileName, comparer_func)
                testCase.maxDiff = None
                self.addTest(testCase)
            except json.decoder.JSONDecodeError:
                print(f"JSONDecodeError - Filename: {fileName}")

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
            outFileName = os.path.join(p_Dir + "_errors", p_FileName)
            testResult = None

            try:
                p_comparer(p_Obj, p_function, p_TestData, file_name=p_FileName)
            except AssertionError:
                with open(outFileName, "w") as outputFile:
                    p_TestData.update({"result": testResult})
                    json.dump(p_TestData, outputFile, indent=4)
                raise

            #FIXME cleanup
        if "description" in p_TestData:
            func.__name__ = p_TestData["description"]
        else:
            func.__name__ = "test_" + p_FileName[:-5]
        return func

