ERROR_STR = "_errors"

import os

with open(os.path.join(os.path.dirname(__file__), "..", "templates", "WinMerge.xml"), "r") as wf:
    WINMERGE_TEMPLATE = wf.read()

NAME        = "name"
ARGS        = "args"
KWARGS      = "kwargs"
FUNC_NAME   = "function"
MODULE_NAME = "module"
CLASS_NAME  = "class_name"
MD5         = "MD5"
PATH        = "path"

PRE          = "data_pre"
POST         = "data_post"

EXCEPTION   = "exception"
RESULT      = "result"
SELF        = "self"
CLASS       = "class"
GLOBAL      = "globals"

TEST_ITEMS  = "tests"
TEST_ERRORS = "_errors"
CURRENT     = "current"

BUILTINS = 'builtins.'
MAIN = '__main__'

ENCODING = 'utf-8'
HOSTED = 'PYCHARM_HOSTED'

