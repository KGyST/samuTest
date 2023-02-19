import unittest
import os
import shutil
import json

FOLDER      = "test_BigBang"
TEST_ONLY   = os.environ['TEST_ONLY']  if "TEST_ONLY"  in os.environ else ""            # Delimiter: ; without space, filenames without ext

class TestSuite_BigBang(unittest.TestSuite):
    def __init__(self):
        try:
            shutil.rmtree(FOLDER + "_errors")
            os.mkdir(FOLDER + "_errors")
        except PermissionError:
            pass
        except OSError:
            pass

        self._tests = []
        self._fileList = sorted([f for f in os.listdir(FOLDER + "_suites")])
        for fileName in self._fileList:
            split = TEST_ONLY.split(";")
            if TEST_ONLY != "" and fileName [:-5] not in split:
                continue
            if not fileName.startswith('_') and os.path.splitext(fileName)[1] == '.json':
                try:
                    testData = json.load(open(os.path.join(FOLDER + "_suites", fileName), "r"))

                    test_case = TestCase_BigBang(testData, FOLDER, fileName)
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
    def BigBangTestCaseFactory(inTestData, inDir, inFileName):
        def func(inObj):
            outFileName = os.path.join(inDir + "_errors", inFileName)


            try:
                inObj.assertEqual(inTestData["result"], responseJSON)
            except AssertionError:
                print(inTestData["description"])
                print(f"Filename: {inFileName[:-5]}")
                with open(outFileName, "w") as outputFile:
                    inTestData.update({"result": responseJSON})
                    json.dump(inTestData, outputFile, indent=4)
                raise

            #FIXME cleanup
        if "description" in inTestData:
            func.__name__ = inTestData["description"]
        else:
            func.__name__ = "test_" + inFileName[:-5]
        return func