import os
import sys
import unittest
import json
from common.publicFunctions import *
from common.privateFunctions import generateFolder, caseFileCollector
from common.constants import ERROR_STR
import jsonpickle
from typing import Callable
import importlib


class JSONTestSuite(unittest.TestSuite):
    def __init__(self,
                 func: Callable,
                 target_folder: str=".",
                 cases_only: str="",
                 filename_filter_func: Callable=filename_filter_func,
                 case_filter_func: Callable=case_filter_func,
                 comparer_func: Callable=default_comparer_func,
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
                with open(os.path.join(self._folder, sFile), "r") as jf:
                    testData = jsonpickle.loads(jf.read())
                testCase = JSONTestCase(func, testData, self._folder, sFile, comparer_func)
                testCase.maxDiff = None
                self.addTest(testCase)
            except json.decoder.JSONDecodeError:
                print(f"JSONDecodeError - Filename: {sFile}")
                continue
        super().__init__(self._tests)

    def __contains__(self, p_Name: str):
        for test in self._tests:
            if test._testMethodName == p_Name:
                return True
        return False


class JSONTestCase(unittest.TestCase):
    def __init__(self, p_function: Callable, p_TestData, p_Dir: str, p_FileName: str, p_comparer: Callable):
        self.sDir = p_Dir
        self.sFile = p_FileName
        func = self.JSONTestCaseFactory(p_function, p_TestData, p_Dir, p_FileName, p_comparer)
        setattr(JSONTestCase, func.__name__, func)
        super(JSONTestCase, self).__init__(func.__name__)

    @staticmethod
    def JSONTestCaseFactory(p_function: Callable, p_TestData, p_Dir: str, p_FileName: str, p_comparer: Callable=default_comparer_func):
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

class AutoTestSuite(unittest.TestSuite):
    def __init__(self,
                 target_folder: str ='test_folder',
                 comparer_func: Callable = default_comparer_func,
                 ):
        self._tests = []

        try:
            with open(os.path.join(os.getcwd(), target_folder, "current.json"), "r") as jf:

                testData = jsonpickle.loads(jf.read())
            sys.path.append(testData["module_path"])
            module = importlib.import_module(testData["module"])
            func = getattr(module, testData["function"])

            testCase = JSONTestCase(func, testData, target_folder, "current.json", comparer_func)
            testCase.maxDiff = None
            self.addTest(testCase)
        except json.decoder.JSONDecodeError:
            print(f"JSONDecodeError - Filename: current.json")
        super().__init__(self._tests)

