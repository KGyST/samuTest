import unittest
import os
import shutil
import json

def case_filter_func(p_cases_to_be_tested:str, p_fileName:str) -> bool:
    cases_to_be_tested = case_only.split(";")
    return p_cases_to_be_tested \
           and p_fileName[:-5] not in cases_to_be_tested \
           and p_fileName not in cases_to_be_tested

def filename_filter_func(p_fileName:str, p_ext:str) -> bool:
    return not p_fileName.startswith('_') \
           and os.path.splitext(p_fileName)[1] == p_ext

def default_comparer_func(p_Obj:object, p_function:function, p_TestData:dict, *args, **kwargs):
    testResult = p_function(*p_TestData["args"], **p_TestData["kwargs"])
    p_TestData.update({"result": testResult})
    p_Obj.assertEqual(p_TestData["result"], testResult)

def resultFileGenerator(p_folder:str, p_testFile:str) -> str:
    sResultFolder = p_folder + "_errors"
    try:
        shutil.rmtree(sResultFolder)
    except OSError:
        pass
    try:
        os.mkdir(sResultFolder)
    except PermissionError:
        #FIXME handling
        pass
    return os.path.join(sResultFolder, p_testFile)


class JSONTestSuite(unittest.TestSuite):
    def __init__(self,
                 folder,
                 case_only,
                 function=None,
                 filename_filter_func=filename_filter_func,
                 case_filter_func=case_filter_func,
                 comparer_func=default_comparer_func,
                 first_run=False):
        self._tests = []
        #FIXME check if folder doesn't exist:
        self._fileList = sorted([f for f in os.listdir(folder)])
        self._folder = folder
        self._folderHandler(first_run)
        for fileName in self._fileList:
            if case_filter_func(case_only, fileName):
                continue
            if filename_filter_func(fileName, ".json"):
                try:
                    testData = json.load(open(os.path.join(folder, fileName), "r"))

                    testCase = JSONTestCase(function, testData, folder, fileName, comparer_func)
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

    def _folderHandler(self, p_firstRun):
        #FIXME add first_run
        #FIXME WinMerge file generation

        try:
            shutil.rmtree(self._folder + "_errors")
        except OSError:
            pass

        try:
            os.mkdir(self._folder + "_errors")
        except PermissionError:
            #FIXME handling
            pass


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

