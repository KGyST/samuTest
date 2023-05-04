from unitTest.test_runner import JSONTestSuite


class firstRunTestSuite(JSONTestSuite):
    def __init__(self):
        #FIXME import module name as passed variable:
        from firstRunTestClient import funcTestee
        super(firstRunTestSuite, self).__init__(funcTestee, target_folder="test_folder")

