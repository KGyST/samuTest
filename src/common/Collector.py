import glob
from common.constants import *
from data.ProgramState import PostState, PreState, ProgramState


class FileCollector:
    def __init__(self, path: str, codec):
        self.sFolderPath = path
        self._index = -1
        self._caseS = []
        if os.path.exists(self.sFolderPath):
            sCaseS = glob.glob('**/*' + codec.sExt, root_dir=self.sFolderPath, recursive=True)
            for _sCase in sCaseS:
                _dCase = codec.read(os.path.join(self.sFolderPath, _sCase))
                _dCase.path = _sCase
                if not _dCase.name:
                    # Test has NO given name, so let it be the filename
                    _dCase.name = os.path.splitext(".".join(_sCase.split(os.path.sep)))[0]
                elif not "." in _dCase.name:
                    # Test has a given name, but path is to be inferred from folder path
                    _dCase.name = ".".join([*_sCase.split(os.path.sep)[:-1], _dCase.name])
                self._caseS.append(_dCase)

    def __iter__(self) -> 'FileCollector':
        return self

    def __next__(self) -> dict:
        self._index += 1

        if self._index < len(self._caseS):
            return self._caseS[self._index]
        else:
            raise StopIteration


class DBCollector:
    ...

