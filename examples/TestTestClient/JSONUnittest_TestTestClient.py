from unitTest.test_runner import JSONTestSuite


class Test_JSONTestTestClient(JSONTestSuite):
    def __init__(self):
        #FIXME import as variable
        from TestTestClient import funcTestee
        super(Test_JSONTestTestClient, self).__init__(funcTestee)

