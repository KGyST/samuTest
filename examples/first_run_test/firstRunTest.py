from unitTest.test_runner import JSONTestSuite


class firstRunTestSuite(JSONTestSuite):
    def __init__(self):
        #FIXME import module name as passed variable:
        from firstRunTestClient import funcTestee
        #FIXME devise actual function name, to remove first param
        super(firstRunTestSuite, self).__init__("funcTestee", funcTestee, first_run=True, target_folder="test_folder")

