ERROR_STR = "_errors"

import os

with open(os.path.join(os.path.dirname(__file__), "..", "templates", "WinMerge.xml"), "r") as wf:
    WINMERGE_TEMPLATE = wf.read()