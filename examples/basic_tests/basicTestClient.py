from decorator.decorators import Dumper
from helpers import ZeroDivisionErrorCatcher

# glob_variable = 1

# ------- Settings -----------------------------------
isFuncTesteeActive = True
isFuncTesteeWithMultipleReturnValues = True
# ----------------------------------------------------


@Dumper(active=isFuncTesteeActive)
@ZeroDivisionErrorCatcher
def funcTestee(number):
    return 1 / number

@Dumper(active=isFuncTesteeWithMultipleReturnValues)
@ZeroDivisionErrorCatcher
def funcTesteeWithMultipleReturnValues(number):
    return number, 1 / number

@Dumper(active=True)
def simplestFunction(number):
    return 1+number

@Dumper()
def calledFunction(number):
    return number + 1

@Dumper(active=True)
def callerFunction(number):
    return calledFunction(number)


if __name__ == "__main__":
    for i in range(-1, 3):
        j = funcTestee(i)
        print(j)
        j = funcTesteeWithMultipleReturnValues(i)
        print(j)
        j = simplestFunction(i)
        print(j)
        j = callerFunction(i)
        print(j)

