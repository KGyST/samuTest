from decorator.decorators import JSONFunctionDumper
from typing import Callable
from helpers import ZeroDivisionErrorCatcher


@JSONFunctionDumper(active=True)
@ZeroDivisionErrorCatcher
def funcTestee(number):
    return 1 / number


if __name__ == "__main__":
    for i in range(-1, 3):
        i = funcTestee(i)
        print(i)

    print(funcTestee(100))

