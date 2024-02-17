import glob
from common.constants import *


class FileCollector:
    def __init__(self, path:str, encoder):
        self.sFolderPath = path
        self._index = -1
        self._caseS = []
        if os.path.exists(self.sFolderPath):
            sCaseS = glob.glob('**/*' + encoder.ext, root_dir=self.sFolderPath, recursive=True)
            for _sCase in sCaseS:
                _dCase = encoder.read(os.path.join(self.sFolderPath, _sCase) )
                if NAME not in _dCase:
                    _dCase[NAME] = os.path.splitext(".".join(_sCase.split(os.path.sep)))[0]
                    self._caseS.append(_dCase)

    def __iter__(self)->'FileCollector':
        return self

    def __next__(self)->dict:
        self._index += 1

        if self._index < len(self._caseS):
            return self._caseS[self._index]
        else:
            raise StopIteration

