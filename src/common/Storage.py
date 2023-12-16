import os
from typing import Callable
import glob
import unittest


class Case(unittest.TestCase):
    def __init__(self):
        super().__init__()


class FileStorage:
    def __init__(self,
          folder: str,
          cases_only: str,
          case_filter_func: Callable,
          ext: str):
        """
        :param folder:
        :param cases_only: filenames with or without extension divided by;
        :param case_filter_func:
        :param ext:
        """
        self.sFolderPath = folder
        self.sCases = cases_only
        self.fFilter = case_filter_func
        self.sExt = ext
        self.sCaseS = self._caseFileCollector()

    def _caseFileCollector(self):
        if os.path.exists(self.sFolderPath):
            _sCaseS = glob.glob('**/*' + self.sExt, root_dir=self.sFolderPath, recursive=True)
            if self.fFilter:
                def _caseFilter(file_name: str):
                    return self.fFilter(file_name, self.sExt, cases_to_be_tested=self.sCases)
                _sCaseS = list(filter(_caseFilter, _sCaseS))
            return _sCaseS


class JSONStorage(FileStorage):
    pass