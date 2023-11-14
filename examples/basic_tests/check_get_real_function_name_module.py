# module_example.py

import functools

def my_decorator(func):
    # @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Decorator: Something is happening before the function is called.")
        result = func(*args, **kwargs)
        print("Decorator: Something is happening after the function is called.")
        return result
    return wrapper

def get_real_function_name(func):
    """
    Get the real function name considering module names, class names, decorators, etc.
    """
    module_name, class_name, func_name = None, None, func.__name__

    # Extract the original function from the closure attribute of the wrapper
    if hasattr(func, '__closure__') and func.__closure__:
        original_func = func.__closure__[0].cell_contents
        if original_func:
            module_name = original_func.__module__
            class_name = original_func.__qualname__.split('.')[0]
            func_name = original_func.__name__

            if module_name == "__main__":
                import os
                import inspect
                module_name = os.path.splitext(os.path.basename(inspect.getmodule(func).__file__))[0]
    return module_name, class_name, func_name

# Example usage:

class MyClass:
    @my_decorator
    @staticmethod
    def my_method():
        print("Method: Hello from MyClass!")

@my_decorator
def my_function():
    print("Function: Hello!")

# Getting real names
module_name_method, class_name_method, func_name_method = get_real_function_name(MyClass.my_method)
module_name_function, class_name_function, func_name_function = get_real_function_name(my_function)

print("Module, class, and method name of the method:", module_name_method, class_name_method, func_name_method)
print("Module, class, and function name of the function:", module_name_function, class_name_function, func_name_function)
