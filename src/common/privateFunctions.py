import glob
import os.path
import shutil
from typing import Callable
from common.constants import MD5, TEST_ITEMS
from common.publicFunctions import *

def md5Collector( folder:str=TEST_ITEMS,
                  cases_only: str = "",
                  case_filter_func: Callable=case_filter_func,
                  filename_filter_func: Callable=filename_filter_func,
                  ext:str = ".json") -> dict[str, str]:
    dResult = {}
    for sFilePath in caseFileCollector(folder, "", None, filename_filter_func, ".json"):
        import jsonpickle
        with open(os.path.join(folder, sFilePath), "r") as jf:
            _dCase = jsonpickle.loads(jf.read())
            if MD5 in _dCase:
                _sMD5 = _dCase[MD5]
                dResult[_sMD5] = sFilePath
    return dResult

def caseFileCollector(folder:str,
                      cases_only: str,
                      case_filter_func: Callable,
                      filename_filter_func: Callable,
                      ext:str) -> list[str]:
    resultCaseS = []
    if not os.path.exists(folder):
        return resultCaseS
    resultCaseS = glob.glob('**/*' + ext, root_dir=folder, recursive=True)
    def _onlyFilter(file_name:str)->bool:
        if not cases_only:
            return True
        _onlyCaseS = cases_only.split(";")
        return any((case in file_name) for case in _onlyCaseS)
    resultCaseS = list(filter(_onlyFilter, resultCaseS))
    if filename_filter_func:
        def _nameFilter(file_name:str):
            return filename_filter_func(file_name, ext)
    if case_filter_func:
        def _caseFilter(file_name:str):
            return case_filter_func(_caseFilter, ext)
    resultCaseS = list(filter(_caseFilter, resultCaseS))
    return resultCaseS


def generateFolder(folder_path:str, force_delete:bool=False):
    if os.path.exists(folder_path):
        if force_delete:
            try:
                shutil.rmtree(folder_path)
            except OSError:
                #FIXME maybe removing all the files from the folder
                pass
        else:
            #Common case
            return
    try:
        os.makedirs(folder_path)
    except PermissionError:
        #FIXME handling
        pass


def open_and_create_folders(file:str, mode:str):
    try:
        return open(file, mode)
    except FileNotFoundError:
        folder_path = os.path.dirname(file)
        os.makedirs(folder_path, exist_ok=True)

        return open(file, mode)


def _get_original_function(func: 'Callable') -> 'Callable':
    if hasattr(func, '__closure__') and func.__closure__:
        return _get_original_function(func.__closure__[0].cell_contents)
    else:
        return func


def get_original_function_name(func: 'Callable'):
    """
    Get the real function name considering module names, class names, decorators, etc.
    """
    module_name, class_name, func_name = None, None, func.__name__

    # Extract the original function from the closure attribute of the wrapper
    original_func = _get_original_function(func)
    if original_func:
        module_name = original_func.__module__
        class_name = original_func.__qualname__.split('.')[0] if '.' in original_func.__qualname__ else None
        func_name = original_func.__name__

    # When the script is run directly, use __file__ to get the module name
    if module_name == '__main__':
        module_name = _get_calling_module_name()
    return module_name, class_name, func_name


def _get_calling_module_name():
    import inspect
    frame = inspect.currentframe().f_back
    while frame:
        if frame.f_globals['__name__'] == '__main__':
            _f = frame.f_globals['__file__']
            return os.path.splitext(os.path.basename(_f))[0]
        frame = frame.f_back
    return frame.f_globals['__name__']

