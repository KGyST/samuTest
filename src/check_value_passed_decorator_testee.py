#check_value_passed_decorator_testee.py
from check_value_passed_decorator import WrapperFunctor


@WrapperFunctor()
def testFunction(*args, **kwargs):
    print('testFunction ran')