# module_example.py

import functools
import os

def my_decorator2(func):
    # @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Decorator: Something is happening before the function is called. 2")
        result = func(*args, **kwargs)
        print("Decorator: Something is happening after the function is called. 2")
        return result
    return wrapper

def my_decorator(func):
    # @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Decorator: Something is happening before the function is called.")
        result = func(*args, **kwargs)
        print("Decorator: Something is happening after the function is called.")
        return result
    return wrapper


def _get_original_function(func):
    if hasattr(func, '__closure__') and func.__closure__:
        return _get_original_function(func.__closure__[0].cell_contents)
    elif hasattr(func, '__cloaure__'):
        return func.__closure__[0].cell_contents
    else:
        return func


def get_original_function_name(func):
    """
    Get the real function name considering module names, class names, decorators, etc.
    """
    module_name, class_name, func_name = None, None, func.__name__

    # Extract the original function from the closure attribute of the wrapper
    original_func = _get_original_function(func)
    if original_func:
        module_name = original_func.__module__
        class_name = original_func.__qualname__.split('.')[0] if '.' in original_func.__qualname__ else None
        func_name = original_func.__name__

    # When the script is run directly, use __file__ to get the module name
    if module_name == '__main__':
        module_name = os.path.splitext(os.path.basename(__file__))[0]

    return module_name, class_name, func_name

# Example usage:

class MyClass:
    @my_decorator2
    @my_decorator
    @staticmethod
    def my_method():
        print("Method: Hello from MyClass!")

@my_decorator2
@my_decorator
def my_function():
    print("Function: Hello!")

# Getting real names
module_name_method, class_name_method, func_name_method = get_original_function_name(MyClass.my_method)
module_name_function, class_name_function, func_name_function = get_original_function_name(my_function)

print("Module, class, and method name of the method:", module_name_method, class_name_method, func_name_method)
print("Module, class, and function name of the function:", module_name_function, class_name_function, func_name_function)
