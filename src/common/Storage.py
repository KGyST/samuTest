import os
import glob
import unittest
import json
from common.publicFunctions import *
from common.privateFunctions import generateFolder, caseFileCollector, open_and_create_folders
from common.constants import *
import jsonpickle
from typing import Callable


class JSONStorage:
    class StorageException(Exception):
        pass

    @staticmethod
    def read(path):
        with open(path, "r") as jf:
            try:
                return jsonpickle.loads(jf.read())
            except Exception:
                raise JSONStorage.StorageException()

    @staticmethod
    def dump(path):
        pass


class StorageTestSuite(unittest.TestSuite):
    def __init__(self,
                 base_folder: str=TEST_ITEMS,
                 sub_folder: str = '',
                 file_name: str = '',
                 data_class = JSONStorage,
                 ):
        """
        :param target_folder:
        """
        # self._tests is an inherited member!
        self._tests = []
        self.cData = data_class
        sSubFolder = os.path.join(sub_folder, file_name)

        from os import listdir, path
        for _file in listdir(os.path.join(base_folder, sSubFolder)):
            if path.isdir(os.path.join(base_folder, sSubFolder, _file)):
                _item = StorageTestSuite(base_folder, sSubFolder, _file, self.cData)
                _item.__name__ = file_name
                self.addTest(_item)
            else:
                try:
                    _item = StorageTestCase(base_folder, sSubFolder, _file, self.cData)
                    _item.__name__ = file_name
                    self.addTest(_item)
                except JSONStorage.StorageException:
                    continue
                # if file_name:

        super().__init__(self._tests)


class StorageTestCase(unittest.TestCase):
    def __init__(self, base_folder: str, sub_path, file_name, data_class):
        self.sFile = file_name
        self.sItemsPath = os.path.join(base_folder, sub_path, file_name)
        self.sErrorsPath = os.path.join(base_folder + TEST_ERRORS, sub_path, file_name)
        self.testData  = data_class.read(self.sItemsPath)
        func = self.JSONTestCaseFactory(self.testData)
        setattr(StorageTestCase, func.__name__, func)
        super().__init__(func.__name__)

    def JSONTestCaseFactory(self, test_data:dict, comparer_function: Callable=default_comparer_func)->'Callable':
        def func(object):
            testResult = None

            try:
                import importlib
                module = importlib.import_module(test_data[MODULE_NAME])
                if CLASS_NAME in test_data and test_data[CLASS_NAME]:
                    _class = getattr(module, test_data[CLASS_NAME])
                    func = getattr(_class, test_data[FUNC_NAME])
                else:
                    func = getattr(module, test_data[FUNC_NAME])

                comparer_function(object, func, test_data[ARGS], test_data[KWARGS], test_data[RESULT])
            except AssertionError:
                test_data.update({RESULT: testResult,})

                # try:
                with open_and_create_folders(self.sErrorsPath, "w") as fOutput:
                    json.dump(test_data, fOutput, indent=4)
                raise
            except Exception as e:
                raise
        if NAME in test_data:
            func.__name__ = test_data[NAME]
        else:
            func.__name__ = "test_" + self.sFile[:-5]
        return func


#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------

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


