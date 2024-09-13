#check_value1.py

from try_value_passed_decorator_testee import testFunction
from try_value_passed_decorator import WrapperFunctor

WrapperFunctor.doRun = False
testFunction()