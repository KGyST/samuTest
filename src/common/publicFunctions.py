import os


class DefaultResult:
    #FIXME __repr__ or __str__
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

    def __repr__(self):
        from pprint import pformat
        _dict = {k: v for k, v in self.__dict__.items() if k not in self.__class__.__dict__ }
        return pformat(_dict)


def case_filter_func(cases_to_be_tested:str, file_name:str) -> bool:
    """
    Allows to run against only a list of cases, including or excluding extension, like .json
    :param cases_to_be_tested: a string of filenames and ;
    :param file_name:
    :return: True if the case is to be tested, False if to be filtered out
    """
    lCaseS = cases_to_be_tested.split(";")
    return len(lCaseS) == 0  \
           or os.path.splitext(file_name)[0] in lCaseS \
           or file_name in lCaseS

def filename_filter_func(file_name:str, extension:str, fileter_char:str=".") -> bool:
    """
    Filter by filename and extension
    :param file_name: file name
    :param extension: expected extension
    :param fileter_char: if filename starts with this character, it is fitered out
    :return:
    """
    return os.path.splitext(file_name)[1] == extension \
    and file_name[0] != fileter_char

def default_comparer_func(obj:'DefaultResult', func, func_args:list, func_kwargs:dict, expected_result):
    testResult = func(*func_args, **func_kwargs)

    #FIXME to modify into something like this:
    # test_data.update({"result": ResultClass(testResult)})
    # __eq__ etc being defined in ResultClass
    obj.assertEqual(DefaultResult(expected_result), DefaultResult(testResult))

