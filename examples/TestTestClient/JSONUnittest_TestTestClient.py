from unitTest.test_runner import JSONTestSuite
import os
import pytest


class Test_JSONTestTestClient(JSONTestSuite):
    testOnly    = os.environ['TEST_ONLY'] if "TEST_ONLY" in os.environ else ""            # Delimiter: ; without space, filenames without ext
    targetDir   = "testJSONTest"
    isActive    = False

    def __init__(self):
        #FIXME import as variable
        from TestTestClient import funcTestee
        super(Test_JSONTestTestClient, self).__init__(function=funcTestee, folder=self.targetDir, case_only=self.testOnly)




