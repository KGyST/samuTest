import unittest
import os
import shutil
import json
#FIXME WinMerge file generation

def case_filter(p_sOnly, p_sFileName, p_split):
    return p_sOnly != "" and p_sFileName[:-5] not in p_split and p_sFileName not in p_split

def filename_filter(p_sFileName, p_ext):
    return not p_sFileName.startswith('_') and os.path.splitext(p_sFileName)[1] == p_ext

def defaultComparer(p_Obj, p_function, p_TestData):
    testResult = p_function(*p_TestData["args"], **p_TestData["kwargs"])
    p_Obj.assertEqual(p_TestData["result"], testResult)


class JSONTestSuite(unittest.TestSuite):
    def __init__(self,
                 folder, case_only,
                 function=None,
                 filename_filter=filename_filter,
                 case_filter=case_filter,
                 comparer=defaultComparer):
        try:
            shutil.rmtree(folder + "_errors")
        except OSError:
            pass
        try:
            os.mkdir(folder + "_errors")
        except PermissionError:
            #FIXME handling
            pass

        self._tests = []
        self._fileList = sorted([f for f in os.listdir(folder)])
        for fileName in self._fileList:
            split = case_only.split(";")
            if case_filter(case_only, fileName, split):
                continue
            if filename_filter(fileName, ".json"):
                try:
                    testData = json.load(open(os.path.join(folder, fileName), "r"))

                    test_case = JSONTestCase(function, testData, folder, fileName, comparer)
                    test_case.maxDiff = None
                    self.addTest(test_case)
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
    def JSONTestCaseFactory(p_function, p_TestData, p_Dir, p_FileName, p_comparer=defaultComparer):
        def func(p_Obj):
            outFileName = os.path.join(p_Dir + "_errors", p_FileName)
            testResult = None

            try:
                # testResult = p_function(*p_TestData["args"], **p_TestData["kwargs"], working_directory = p_Dir)
                # p_Obj.assertEqual(p_TestData["result"], testResult)
                p_comparer(p_Obj, p_function, p_TestData)
            except AssertionError:
                # print(p_TestData["description"])
                # print(f"Filename: {inFileName[:-5]}")
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


