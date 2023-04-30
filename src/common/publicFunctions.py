from common.constants import ERROR_STR

def case_filter_func(cases_to_be_tested:str, file_name:str) -> bool:
    lCaseS = cases_to_be_tested.split(";")
    return lCaseS \
           and file_name[:-5] not in lCaseS \
           and file_name not in lCaseS

def filename_filter_func(file_name:str, extension:str) -> bool:
    return not file_name.startswith('_') \
           and os.path.splitext(file_name)[1] == extension

def default_comparer_func(obj:object, tested_function, test_data:dict, *args, **kwargs):
    testResult = tested_function(*test_data["args"], **test_data["kwargs"])
    test_data.update({"result": testResult})
    #FIXME to modify into something like this:
    # test_data.update({"result": ResultClass(testResult)})
    # __eq__ etc being defined in ResultClass
    obj.assertEqual(test_data["result"], testResult)

