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

INST_PRE    = "instance_data_pre"
INST_POST   = "instance_data_post"
GLOBAL_PRE    = "instance_data_pre"
GLOBAL_POST   = "instance_data_post"

EXCEPTION   = "exception"
RESULT      = "result"

TEST_ITEMS  = "tests"
TEST_ERRORS = "test_errors"
CURRENT     = "current"