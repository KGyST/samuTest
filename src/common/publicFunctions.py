from common.constants import ERROR_STR
import os
import jsonpickle
import importlib
import sys


class DefaultResult:
    def __init__(self, p_result):
        if hasattr(p_result, "__dict__"):
            self.__dict__ = p_result.__dict__
        else:
            self.__value = p_result
        self.__class = p_result.__class__

    def __eq__(self, other):
        if isinstance(other, self.__class) or isinstance(other, DefaultResult) and self.__class == other.__class:
            if hasattr(self, "__dict__"):
                return self.__dict__ == other.__dict__
            else:
                return self.__value == other
        return False


def case_filter_func(cases_to_be_tested:str, file_name:str) -> bool:
    lCaseS = cases_to_be_tested.split(";")
    return lCaseS \
           and file_name[:-5] not in lCaseS \
           and file_name not in lCaseS

def filename_filter_func(file_name:str, extension:str) -> bool:
    return not file_name.startswith('_') \
           and os.path.splitext(file_name)[1] == extension

def default_comparer_func(obj:object, test_data:dict, *args, **kwargs):
    module = importlib.import_module(test_data["module"])
    func = getattr(module, test_data["function"])
    testResult = func(*test_data["args"], **test_data["kwargs"])
    expectedResult = test_data["result"]

    # test_data.update({"result": testResult})
    #FIXME to modify into something like this:
    # test_data.update({"result": ResultClass(testResult)})
    # __eq__ etc being defined in ResultClass
    obj.assertEqual(DefaultResult(expectedResult), DefaultResult(testResult))

