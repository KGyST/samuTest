from unitTest.test_runner import XMLTestSuite
import os

class test_XMLTestTestClient(XMLTestSuite):
    testOnly    = os.environ['TEST_ONLY'] if "TEST_ONLY" in os.environ else ""            # Delimiter: ; without space, filenames without ext
    targetDir   = "testXMLTest"
    isActive    = False

    def __init__(self):
        #FIXME import as variable
        from TestTestClient import funcTestee
        super(test_XMLTestTestClient, self).__init__(function=funcTestee, folder=self.targetDir, case_only=self.testOnly)

