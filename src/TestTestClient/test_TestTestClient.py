from unittest import TestCase
from test_runner import JSONTestSuite
import os
from TestTestClient import funcTestee


class test_TestTestClient(JSONTestSuite):
    FOLDER      = "..\\..\\tests\\testTest"
    TEST_ONLY   = os.environ['TEST_ONLY']  if "TEST_ONLY"  in os.environ else ""            # Delimiter: ; without space, filenames without ext

    def __init__(self):
        super(test_TestTestClient, self).__init__(function=funcTestee, folder=test_TestTestClient.FOLDER, case_only=test_TestTestClient.TEST_ONLY)

