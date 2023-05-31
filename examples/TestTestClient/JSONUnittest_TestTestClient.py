from unitTest.test_runner import JSONTestSuite, AutoTestSuite


class Test_JSONTestTestClient(JSONTestSuite):
    def __init__(self):
        #FIXME import as variable
        from TestTestClient import funcTestee
        super().__init__(funcTestee)


class Test_current(AutoTestSuite):
    def __init__(self):
        super().__init__()

