from decorator.decorators import Dumper
from helpers import ZeroDivisionErrorCatcher


@Dumper()
@ZeroDivisionErrorCatcher
def funcTestee(num: int):
    return 1 / num, num


if __name__ == "__main__":
    for i in range(-1, 3):
        i = funcTestee(i)
        print(i)

    print(funcTestee(100))

