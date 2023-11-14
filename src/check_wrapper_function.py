#check_wrapper_function.py
import importlib

import jsonpickle
from importlib import import_module

# Decorator function to serialize function parameters to a JSON file
def parameterize_and_serialize(func):
    def wrapper(*args, **kwargs):
        if args and hasattr(args[0], '__dict__'):
            instance = args[0]
        else:
            instance = None

        if '.' in func.__qualname__:
            class_name, function_name = func.__qualname__.rsplit('.', 1)
        else:
            class_name, function_name = None, func.__qualname__

        parameterization = {
            "instance_data": instance,
            "args": args[1:] if instance else args,
            "kwargs": kwargs,
            "class_name": class_name,
            "function_name": function_name,
        }

        parameter_json = jsonpickle.encode(parameterization)
        with open(f'parameterization_{func.__name__}.json', 'w') as file:
            file.write(parameter_json)
        if isinstance(func, classmethod):
            if not instance:
                _mod = importlib.import_module(func.__module__)
                _class = getattr(_mod, class_name)
                return func.__func__(_class, *args, **kwargs)
            else:
                return func.__func__(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper