import os.path
import shutil

def folderHandler(p_sFolder):
    sErrorFolder = p_sFolder + "_errors"
    if os.path.exists(sErrorFolder):
        shutil.rmtree(sErrorFolder)
    os.mkdir(sErrorFolder)

def caseFileCollector(p_sFolder:str,
                      p_case_filter_func,
                      p_cases_only,
                      p_filename_filter_func,
                      p_ext) -> list:
    resultCaseS = []
    if not os.path.exists(p_sFolder):
        return resultCaseS
    resultCaseS = sorted([f for f in os.listdir(p_sFolder)])
    def _onlyFilter(p_sFile):
        return p_sFile in p_cases_only
    filter(_onlyFilter, resultCaseS)
    def _nameFilter(p_sFile):
        return filename_filter_func(p_sFile, p_ext)
    filter(_nameFilter, resultCaseS)
    return resultCaseS

