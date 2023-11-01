import jsonpickle


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
        return func(*args, **kwargs)
    return wrapper


# Player side to run from .json files
def run_from_json(file_name):
    with open(file_name, 'r') as file:
        parameter_json = file.read()
    parameterization = jsonpickle.decode(parameter_json)

    if parameterization["instance_data"]:
        instance = parameterization["instance_data"]
        method = getattr(instance, parameterization["function_name"], None)
        method(*parameterization["args"], **parameterization["kwargs"])
    else:
        class_name = parameterization["class_name"]
        function_name = parameterization["function_name"]
        if class_name in (_globals := globals()):
            _class = _globals[class_name]
            function = getattr(_class, function_name)
        else:
            function = _globals[function_name]
        function(*parameterization["args"], **parameterization["kwargs"])


# Class with dummy function, class method, and static method
class MyClass:
    def __init__(self, value):
        self.value = value

    @parameterize_and_serialize
    def dummy_func(self, x, y):
        result = self.value * (x + y)
        print(f"dummy_func Result: {result}")

    @classmethod
    @parameterize_and_serialize
    def class_method(cls, x, y):
        result = x * y
        print(f"class_method Result: {result}")

    @parameterize_and_serialize
    @staticmethod
    def static_method(x, y):
        result = x * y
        print(f"static_method Result: {result}")

    def __repr__(self):
        return f"MyClass(value={self.value})"


# Standalone function
@parameterize_and_serialize
def standalone_function(x, y):
    result = x * y
    print(f"standalone_function Result: {result}")


# Instantiate the class
my_instance = MyClass(value=10)

# Call the dummy_func with parameters
my_instance.dummy_func(5, 2)

# Call the class_method with parameters
MyClass.class_method(3, 4)

# Call the static_method with parameters
MyClass.static_method(6, 7)

# Serialize parameters for standalone function
standalone_function(10, 11)

# Run examples from .json files
run_from_json('parameterization_dummy_func.json')
run_from_json('parameterization_class_method.json')
run_from_json('parameterization_static_method.json')
run_from_json('parameterization_standalone_function.json')

# print(locals())
# print(globals())