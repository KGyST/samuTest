#check_value1.py

from check_value_passed_decorator_testee import testFunction
from check_value_passed_decorator import WrapperFunctor

WrapperFunctor.doRun = False
testFunction()