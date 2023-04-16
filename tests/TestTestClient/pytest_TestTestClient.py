from pyTest.pyTestFramework import getTests
import os
import pytest

def defaultComparer(p_function, p_TestData):
    testResult = p_function(*p_TestData["args"], **p_TestData["kwargs"])
    p_TestData.update({"result": testResult})
    assert p_TestData["result"] == testResult


class Test_JSONpytestClient():
    testOnly    = os.environ['TEST_ONLY'] if "TEST_ONLY" in os.environ else ""            # Delimiter: ; without space, filenames without ext
    targetDir   = "testJSONTest"
    isActive    = False

    @pytest.mark.parametrize(
        'p_testCase', getTests("testJSONTest")
    )
    def test_file(self, p_testCase):
        from TestTestClient import funcTestee

        defaultComparer(funcTestee, p_testCase)

        print(p_testCase)
