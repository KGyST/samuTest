from unittest import TestCase
from test_runner import TestSuite_BigBang
import os

FOLDER      = "..\\..\\tests\\testTest"
TEST_ONLY   = os.environ['TEST_ONLY']  if "TEST_ONLY"  in os.environ else ""            # Delimiter: ; without space, filenames without ext

class test_TestTestClient(TestSuite_BigBang):
    def __init__(self):
        super(test_TestTestClient, self).__init__(p_folder=FOLDER, p_test_only=TEST_ONLY)


class Test(TestCase):
    def test_func_testee(self):
        self.fail()
