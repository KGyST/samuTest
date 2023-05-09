from decorator.decorators import JSONDumper
import called_package


@JSONDumper(mocked_functions=[called_package.CalledModule.called_function])
def called_function_with_another_function(p_iNum):
    return called_package.CalledModule.called_function(p_iNum)


if __name__ == "__main__":
    for i in range(-1, 3):
        i = called_function_with_another_function(i)
        print(i)
