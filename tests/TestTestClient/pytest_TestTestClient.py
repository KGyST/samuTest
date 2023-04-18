from pyTest.pyTestFramework import getTests, Test_Dummy, defaultComparer
import os
import pytest


class Test_JSONpytestClient(Test_Dummy):
    testOnly    = os.environ['TEST_ONLY'] if "TEST_ONLY" in os.environ else ""            # Delimiter: ; without space, filenames without ext
    targetDir   = "testJSONTest"
    isActive    = False

    def __init__(self):
        super(Dummy, self).__init__()

    @pytest.mark.parametrize(
        'p_testCase', getTests("testJSONTest")
    )
    def test_file(self, p_testCase):
        from TestTestClient import funcTestee

        defaultComparer(funcTestee, p_testCase)

        print(p_testCase)

