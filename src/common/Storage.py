import os
import glob
import unittest
from common.publicFunctions import *
from common.privateFunctions import generateFolder, caseFileCollector, open_and_create_folders
from common.constants import *
import jsonpickle
from typing import Callable





# class StorageTestSuite(unittest.TestSuite):
#     def __init__(self,
#                  base_folder: str=TEST_ITEMS,
#                  sub_folder: str = '',
#                  file_name: str = '',
#                  data_class = JSONStorage,
#                  ):
#         """
#         :param target_folder:
#         """
#         # self._tests is an inherited member!
#         self._tests = []
#         self.cData = data_class
#         sSubFolder = os.path.join(sub_folder, file_name)
#
#         from os import listdir, path
#         for _file in listdir(os.path.join(base_folder, sSubFolder)):
#             if path.isdir(os.path.join(base_folder, sSubFolder, _file)):
#                 _item = StorageTestSuite(base_folder, sSubFolder, _file, self.cData)
#                 _item.__name__ = file_name
#                 self.addTest(_item)
#             else:
#                 try:
#                     _item = StorageTestCase(base_folder, sSubFolder, _file, self.cData)
#                     _item.__name__ = file_name
#                     self.addTest(_item)
#                 except JSONStorage.StorageException:
#                     continue
#                 # if file_name:
#         super().__init__(self._tests)


class StorageTestCase(unittest.TestCase):
    def __init__(self, base_folder: str, sub_path, file_name, data_class):
        self.sFile = file_name
        self.sItemsPath = os.path.join(base_folder, sub_path, file_name)
        self.sErrorsPath = os.path.join("..", base_folder + TEST_ERRORS, sub_path, file_name)
        self.testData  = data_class.read(self.sItemsPath)
        func = self.JSONTestCaseFactory()
        setattr(StorageTestCase, func.__name__, func)
        super().__init__(func.__name__)

    def _dump_data(self, p_dResult:dict):
        self.testData.update(p_dResult)
        with open_and_create_folders(self.sErrorsPath, "w") as fOutput:
            fOutput.write(jsonpickle.dumps(self.testData, indent=4, make_refs=False, include_properties=True))
        raise

    def JSONTestCaseFactory(self, comparer_function: Callable=default_comparer_func)->'Callable':
        def func(object):
            testResult = None

            try:
                import importlib
                module = importlib.import_module(self.testData[MODULE_NAME])

                if CLASS_NAME in self.testData and self.testData[CLASS_NAME]:
                    _class = getattr(module, self.testData[CLASS_NAME])
                    func = getattr(_class, self.testData[FUNC_NAME])
                else:
                    func = getattr(module, self.testData[FUNC_NAME])

                comparer_function(object, func, self.testData[ARGS], self.testData[KWARGS], self.testData[RESULT])
            except AssertionError:
                self._dump_data({RESULT: testResult,})
            except Exception as e:
                self._dump_data({EXCEPTION: e, })

        if NAME in self.testData:
            func.__name__ = self.testData[NAME]
        else:
            #FIXME
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



#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------

class JSONStorage:
    class StorageException(Exception):
        pass

    def __init__(self):
        self.ext = ".json"

    @staticmethod
    def read(path):
        with open(path, "r") as jf:
            try:
                return jsonpickle.loads(jf.read())
            except Exception:
                raise JSONStorage.StorageException()

    @staticmethod
    def dump(path):
        #TODO
        pass

class FileCollector():
    def __init__(self, path, encoder, ext='.json'):
        self.sFolderPath = path
        self.sExt = ext
        self._index = -1
        if os.path.exists(self.sFolderPath):
            self._caseS = []
            _sCaseS = glob.glob('**/*' + self.sExt, root_dir=self.sFolderPath, recursive=True)
            for _sCase in _sCaseS:
                _t = encoder.read(os.path.join(self.sFolderPath, _sCase) )
                if NAME not in _t:
                    _t[NAME], _ =  os.path.splitext(os.path.basename(_sCase))
                    self._caseS.append(_t)

    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1

        if self._index < len(self._caseS):
            # return os.path.join(self.sFolderPath, self._caseS[self._index])
            return self._caseS[self._index]
        else:
            raise StopIteration

class SamuTestSuite(unittest.TestSuite):
    def __init__(self,
                 path: str=TEST_ITEMS,
                 error_path:str=TEST_ERRORS,
                 collector= FileCollector,
                 encoder = JSONStorage,
                 comparer_function: Callable = default_comparer_func,
                 ):
        """
        :param target_folder:
        """
        # self._tests is an inherited member!
        self._tests = []
        self.cData = encoder
        self.fComparer = comparer_function
        self.sErrorPath = error_path

        for t in collector(path, encoder):
            _item = SamuTestCase(t, self)
            self.addTest(_item)

        super().__init__(self._tests)


class SamuTestCase(unittest.TestCase):
    def __init__(self, data, suite):
        self.testData  = data
        self.suite = suite

        func = self.JSONTestCaseFactory()
        setattr(SamuTestCase, func.__name__, func)
        super().__init__(func.__name__)

    def _dump_data(self, p_dResult:dict):
        self.testData.update(p_dResult)
        with open_and_create_folders(self.suite.sErrorPath, "w") as fOutput:
            fOutput.write(jsonpickle.dumps(self.testData, indent=4, make_refs=False, include_properties=True))
        raise

    def JSONTestCaseFactory(self)->'Callable':
        def func(object):
            testResult = None

            try:
                import importlib
                module = importlib.import_module(self.testData[MODULE_NAME])

                if CLASS_NAME in self.testData and self.testData[CLASS_NAME]:
                    _class = getattr(module, self.testData[CLASS_NAME])
                    func = getattr(_class, self.testData[FUNC_NAME])
                else:
                    func = getattr(module, self.testData[FUNC_NAME])

                self.suite.fComparer(object, func, self.testData[ARGS], self.testData[KWARGS], self.testData[RESULT])
            except AssertionError:
                self._dump_data({RESULT: testResult,})
            except Exception as e:
                self._dump_data({EXCEPTION: e, })

        func.__name__ = self.testData[NAME]

        return func

