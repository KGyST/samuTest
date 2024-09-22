import os.path
from common.Storage import FileTestSuite


class BasicFileTestClient(FileTestSuite):
    def __init__(self):
        super().__init__(path="tests", error_path=os.path.join("..", "errors"))

