import glob
from samuTeszt.src.common.constants import *
from samuTeszt.src.common.Logger import Logger


class FileCollector:
    def __init__(self, path: str, codec):
        self.sFolderPath = path
        self._index = -1
        self._caseS = []
        if os.path.exists(self.sFolderPath):
            sCaseS = glob.glob('**/*' + codec.sExt, root_dir=self.sFolderPath, recursive=True)
            for _sCase in sCaseS:
                try:
                    dCase = codec.read(_path := os.path.join(self.sFolderPath, _sCase))
                    dCase.codec = codec
                    if not dCase.name:
                        # Test has NO given name, so let it be the filename
                        dCase.setFullyQualifiedTestName(os.path.splitext(_sCase)[0], os.path.sep)
                    elif not "." in dCase.name:
                        # Test has a given name, but path is to be inferred from folder path
                        dCase.setFullyQualifiedTestName(os.path.splitext(_sCase)[0], os.path.sep)
                    self._caseS.append(dCase)
                except Exception as e:
                    Logger().error(f"File load failed: {e} {_path}")


    def __iter__(self) -> 'FileCollector':
        return self

    def __next__(self):
        self._index += 1

        if self._index < len(self._caseS):
            return self._caseS[self._index]
        else:
            raise StopIteration


class DBCollector:
    ...

