import os
from typing import Callable


class DefaultResult:
    #FIXME __repr__ or __str__
    def __init__(self, result):
        if hasattr(result, "__dict__"):
            self.__dict__ = result.__dict__
        else:
            self.__value = result
        self.__class = result.__class__

    def __eq__(self, other):
        if isinstance(other, self.__class) or isinstance(other, DefaultResult) and self.__class == other.__class:
            if hasattr(self, "__dict__"):
                return self.__dict__ == other.__dict__
            else:
                return self.__value == other
        return False

    def __repr__(self):
        from pprint import pformat
        _dict = {k: v for k, v in self.__dict__.items() if k not in self.__class__.__dict__ }
        return pformat(_dict)


def case_filter_func(file_name:str, extension:str, filter_char:str=".",  cases_to_be_tested:str="" , delimiter:str=";") -> bool:
    """
    Allows to run against only a list of cases, including or excluding extension, like .json
    :param file_name:
    :param extension: expected extension
    :param filter_char: if filename starts with this character, it is filtered out
    :param cases_to_be_tested: a string of filenames and delimiters
    :param delimiter: of cases_to_be_tested
    :return: True if the case is to be tested, False if to be filtered out
    """
    lCaseS = cases_to_be_tested.split(delimiter) if delimiter in cases_to_be_tested else []
    return  (   len(lCaseS) == 0
                or os.path.splitext(file_name)[0] in lCaseS
                or file_name in lCaseS) \
            and os.path.splitext(file_name)[1] == extension \
            and file_name[0] != filter_char


def default_comparer_func(obj:'DefaultResult', func:'Callable', func_args:list, func_kwargs:dict, expected_result=None):
    """
    :param obj:
    :param func:
    :param func_args:
    :param func_kwargs:
    :param expected_result:
    :return:
    """
    testResult = func(*func_args, **func_kwargs)

    #FIXME to modify into something like this:
    # test_data.update({"result": ResultClass(testResult)})
    # __eq__ etc being defined in ResultClass
    obj.assertEqual(DefaultResult(expected_result), DefaultResult(testResult))
    return testResult


def get_file_path(result:dict, root_folder_name:str, error:bool=False)->str:
    return ""

def get_file_path(result:dict, root_folder_name:str, error:bool=False)->str:
    return ""

