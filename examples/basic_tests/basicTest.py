import os.path
from common.Storage import StorageTestSuite


class BasicStorageTestClient(StorageTestSuite):
    def __init__(self):
        super().__init__(path="tests", error_path=os.path.join("..", "errors"))

