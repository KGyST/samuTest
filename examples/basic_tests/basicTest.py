from unitTest.test_runner import JSONTestSuite


class Test_JSONTestTestClient(JSONTestSuite):
    def __init__(self):
        super().__init__()


class Test_current(JSONTestSuite):
    def __init__(self):
        super().__init__(cases_only='current')

