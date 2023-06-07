from decorator.decorators import JSONFunctionDumper, YAMLFunctionDumper
from typing import Callable
from helpers import ZeroDivisionErrorCatcher

# glob_variable = 1

# ------- Settings -----------------------------------
isFuncTesteeActive = True
isFuncTesteeWithMultipleReturnValues = True
# ----------------------------------------------------


@YAMLFunctionDumper(active=isFuncTesteeActive)
@ZeroDivisionErrorCatcher
def funcTestee(p_iNum):
    return 1 / p_iNum

@YAMLFunctionDumper(active=isFuncTesteeWithMultipleReturnValues)
@ZeroDivisionErrorCatcher
def funcTesteeWithMultipleReturnValues(p_iNum):
    return p_iNum, 1/p_iNum

def simplestFunction(p_iNum):
    return 1+p_iNum

def calledFunction(p_iNum):
    return p_iNum + 1

def callerFunction(p_iNum):
    return calledFunction(p_iNum)

if __name__ == "__main__":
    for i in range(-1, 3):
        j = funcTestee(i)
        print(j)
        j = funcTesteeWithMultipleReturnValues(i)
        print(j)
