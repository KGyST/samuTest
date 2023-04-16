import pytest
import os
import jsonpickle

def getTests(dir_basename):
    tests = []
    for fileName in os.listdir(dir_basename):
        if not fileName.startswith('_') and os.path.splitext(fileName)[1] == '.json':
                test_case = jsonpickle.loads(open (os.path.join(dir_basename, fileName), "r").read())
                tests.append(test_case)
    return tests

