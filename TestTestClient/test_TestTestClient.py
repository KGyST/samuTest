# from unittest import TestCase
from test_runner import JSONTestSuite
import os
from parameters import TestParameters


class test_TestTestClient(JSONTestSuite, TestParameters):
    testOnly    = os.environ['TEST_ONLY']  if "TEST_ONLY"  in os.environ else ""            # Delimiter: ; without space, filenames without ext
    targetDir   ="..\\tests\\testTest"
    isActive    =False

    def __init__(self):
        from TestTestClient import funcTestee
        super(test_TestTestClient, self).__init__(function=funcTestee, folder=test_TestTestClient.targetDir, case_only=test_TestTestClient.testOnly)

