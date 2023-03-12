from decorator.decorators import JSONDumper
from decorator.decorators import XMLDumper
from JSONtest_TestTestClient import test_JSONTestTestClient
from XMLtest_TestTestClient import test_XMLTestTestClient

test_glob_variable = 1


# @JSONDumper(testSuite=test_JSONTestTestClient)
@XMLDumper(testSuite=test_XMLTestTestClient)
def funcTestee(p_iNum1, p_iNum2):
    return 1 / p_iNum1


# def funcTesteeWithMultipleReturnValues(p_iNum):
#     return p_iNum, 1/p_iNum
#
# def simplestFunction(p_iNum):
#     return 1+p_iNum


if __name__ == '__main__':
    for i in range(-1, 3):
        i = funcTestee(i, i+1)
        print(i)
