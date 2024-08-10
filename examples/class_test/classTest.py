from unitTest.test_runner import JSONTestSuite
from classTestClient import ClassTestee, ClassToBeNested

class ClassTestSuite(JSONTestSuite):
    def __init__(self):
        super().__init__()

