from decorator.decorators import JSONFunctionDumper
from helpers import ZeroDivisionErrorCatcher


@JSONFunctionDumper(active=True)
@ZeroDivisionErrorCatcher
def funcTestee(p_iNum):
    return 1 / p_iNum, p_iNum


if __name__ == "__main__":
    for i in range(-1, 3):
        i = funcTestee(i)
        print(i)

    print(funcTestee(100))

