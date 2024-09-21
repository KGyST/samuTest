import os
from .FunctionState import FunctionState


class FileState:
    """
    Defines a FunctionState object's place in the file system
    """
    def __init__(self, function_state: 'FunctionState', root_dir: str, root_error_dir: str = ""):
        self.functionState = function_state
        self.sRootDir = root_dir
        self.sRootErrorDir = root_error_dir

    @property
    def sRelativeDir(self) -> str:
        return self.functionState.getFullyQualifiedTestName(os.path.sep)

    @sRelativeDir.setter
    def sRelativeDir(self, value: str):
        pass

    @property
    def sFullDir(self) -> str:
        return os.path.join(self.sRootDir, self.sRelativeDir)

    @property
    def sFullPath(self) -> str:
        return os.path.join(self.sFullDir, self.name + self.functionState.codec.sExt)

    @property
    def sFullErrorDir(self) -> str:
        return os.path.join(self.sRootErrorDir, self.sRelativeDir)

    @property
    def sFullErrorPath(self) -> str:
        return os.path.join(self.sFullErrorDir, self.name + self.functionState.codec.sExt)

    @property
    def md5(self) -> str:
        return self.functionState.md5

    @property
    def name(self) -> str:
        """
        Filename of the actual test (without extension)
        :return:
        """
        if _name := self.functionState.name:
            return _name
        elif not os.path.exists(os.path.join(self.sFullDir, (_sLastDirName := self.sFullDir.split(os.path.sep)[-1]) + self.functionState.codec.sExt)
                and os.getenv('PYCHARM_HOSTED') != '1'):
            return _sLastDirName
        else:
            return self.md5

