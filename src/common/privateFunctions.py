import glob
import os.path
import shutil
from typing import Callable


def caseFileCollector(folder:str,
                      case_filter_func: Callable,
                      cases_only: str,
                      filename_filter_func: Callable,
                      ext:str) -> list[str]:
    resultCaseS = []
    if not os.path.exists(folder):
        return resultCaseS
    resultCaseS = glob.glob('**/*' + ext, root_dir=folder, recursive=True)
    def _onlyFilter(file_name:str)->bool:
        if not cases_only:
            return True
        _cases_only = cases_only.split(";")
        return any((case in file_name) for case in _cases_only)
    resultCaseS = list(filter(_onlyFilter, resultCaseS))
    def _nameFilter(file_name:str):
        return filename_filter_func(file_name, ext)
    resultCaseS = list(filter(_nameFilter, resultCaseS))
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
        os.mkdir(folder_path)
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
    # elif hasattr(func, '__closure__'):
    #     return func.__closure__[0].cell_contents
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
        module_name = os.path.splitext(os.path.basename(__file__))[0]

    return module_name, class_name, func_name

