import os.path
import shutil
from typing import Callable


def caseFileCollector(folder:str,
                      p_case_filter_func: Callable,
                      cases_only: str,
                      filename_filter_func: Callable,
                      ext:str) -> list[str]:
    resultCaseS = []
    if not os.path.exists(folder):
        return resultCaseS
    resultCaseS = sorted([f for f in os.listdir(folder)])
    def _onlyFilter(file_name:str)->bool:
        return file_name in cases_only
    resultCaseS = list(filter(_onlyFilter, resultCaseS))
    def _nameFilter(file_name:str):
        return filename_filter_func(file_name, ext)
    resultCaseS = list(filter(_nameFilter, resultCaseS))
    return resultCaseS

def generateFolder(p_sFolderPath:str, p_bForceDelete:bool=False):
    if os.path.exists(p_sFolderPath):
        if p_bForceDelete:
            try:
                shutil.rmtree(p_sFolderPath)
            except OSError:
                #FIXME maybe removing all the files from the folder
                pass
        else:
            #Common case
            return
    try:
        os.mkdir(p_sFolderPath)
    except PermissionError:
        #FIXME handling
        pass

