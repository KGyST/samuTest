from unitTest.test_runner import JSONTestSuite


class ClassTestSuite(JSONTestSuite):
    def __init__(self):
        # FIXME import module name as passed variable:
        from classTestClient import ClassTestee
        super().__init__(ClassTestee, target_folder="test_folder")

