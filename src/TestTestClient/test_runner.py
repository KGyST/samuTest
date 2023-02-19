import unittest
import os
import shutil
import json
from TestTestClient import funcTestee

FOLDER      = "..\\..\\tests\\testTest"
TEST_ONLY   = os.environ['TEST_ONLY']  if "TEST_ONLY"  in os.environ else ""            # Delimiter: ; without space, filenames without ext

class TestSuite_BigBang(unittest.TestSuite):
    def __init__(self, p_folder = FOLDER, p_test_only=TEST_ONLY):
        try:
            shutil.rmtree(p_folder + "_errors")
            os.mkdir(p_folder + "_errors")
        except PermissionError:
            pass
        except OSError:
            pass

        self._tests = []
        self._fileList = sorted([f for f in os.listdir(p_folder + "_suites")])
        for fileName in self._fileList:
            split = p_test_only.split(";")
            if p_test_only != "" and fileName [:-5] not in split:
                continue
            if not fileName.startswith('_') and os.path.splitext(fileName)[1] == '.json':
                try:
                    testData = json.load(open(os.path.join(p_folder + "_suites", fileName), "r"))

                    test_case = TestCase_BigBang(testData, p_folder, fileName)
                    test_case.maxDiff = None
                    self.addTest(test_case)
                except json.decoder.JSONDecodeError:
                    print(f"JSONDecodeError - Filename: {fileName}")

        super(TestSuite_BigBang, self).__init__(self._tests)

    def __contains__(self, inName):
        for test in self._tests:
            if test._testMethodName == inName:
                return True
        return False


class TestCase_BigBang(unittest.TestCase):
    def __init__(self, inTestData, inDir, inFileName):
        func = self.BigBangTestCaseFactory(inTestData, inDir, inFileName)
        setattr(TestCase_BigBang, func.__name__, func)
        super(TestCase_BigBang, self).__init__(func.__name__)

    @staticmethod
    def BigBangTestCaseFactory(p_TestData, inDir, inFileName):
        def func(p_Obj):
            outFileName = os.path.join(inDir + "_errors", inFileName)

            try:
                testResult = funcTestee(*p_TestData["args"], **p_TestData["kwargs"])
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