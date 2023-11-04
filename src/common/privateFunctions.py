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



