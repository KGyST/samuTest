from unitTest.test_runner import JSONTestSuite


class multiResultTestSuite(JSONTestSuite):
    def __init__(self):
        #FIXME import module name as passed variable:
        from multiResultTestClient import funcTestee
        super(multiResultTestSuite, self).__init__(funcTestee, target_folder="test_folder")

