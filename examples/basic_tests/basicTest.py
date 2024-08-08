from unitTest.test_runner import JSONTestSuite


class Test_JSONTestTestClient(JSONTestSuite):
    def __init__(self):
        super().__init__(target_folder="tests")


class Test_current(JSONTestSuite):
    def __init__(self):
        super().__init__(cases_only='current')


from common.Storage import StorageTestSuite
class StorageTestClient(StorageTestSuite):
    def __init__(self):
        super().__init__(path="tests", error_path="..\\errors" )

