import unittest
import os
import shutil
import json


def case_filter(p_sOnly, p_sFileName, p_split):
    return p_sOnly != "" and p_sFileName[:-5] not in p_split

def filename_filter(p_sFileName):
    return not p_sFileName.startswith('_') and os.path.splitext(p_sFileName)[1] == '.json'


class JSONTestSuite(unittest.TestSuite):
    def __init__(self, function, folder, case_only,
                 filename_filter=filename_filter,
                 case_filter=case_filter):
        try:
            shutil.rmtree(folder + "_errors")
            os.mkdir(folder + "_errors")
        except PermissionError:
            pass
        except OSError:
            pass

        self._tests = []
        self._fileList = sorted([f for f in os.listdir(folder + "_suites")])
        for fileName in self._fileList:
            split = case_only.split(";")
            if case_filter(case_only, fileName, split):
                continue
            if filename_filter(fileName):
                try:
                    testData = json.load(open(os.path.join(folder + "_suites", fileName), "r"))

                    test_case = JSONTestCase(function, testData, folder, fileName)
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
    def __init__(self, function, inTestData, inDir, inFileName):
        func = self.BigBangTestCaseFactory(function, inTestData, inDir, inFileName)
        setattr(JSONTestCase, func.__name__, func)
        super(JSONTestCase, self).__init__(func.__name__)

    @staticmethod
    def BigBangTestCaseFactory(p_function, p_TestData, inDir, inFileName):
        def func(p_Obj):
            outFileName = os.path.join(inDir + "_errors", inFileName)
            testResult = None

            try:
                testResult = p_function(*p_TestData["args"], **p_TestData["kwargs"])
                p_Obj.assertEqual(p_TestData["result"], testResult)
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
            func.__name__ = "test_" + inFileName[:-5]
        return func