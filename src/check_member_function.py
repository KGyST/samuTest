import jsonpickle


# Decorator function to serialize function parameters to a JSON file
def parameterize_and_serialize(func):
    def wrapper(*args, **kwargs):
        instance = args[0] if args and hasattr(args[0], '__dict__') else None

        parameterization = {
            "name": func.__name__,
            "instance_data": instance,
            "args": args,
            "kwargs": kwargs
        }
        parameter_json = jsonpickle.encode(parameterization)
        with open(f'parameterization_{func.__name__}.json', 'w') as file:
            file.write(parameter_json)

        return func(*args, **kwargs)

    return wrapper


# Class with dummy function, class method, and static method
class MyClass:
    def __init__(self, value):
        self.value = value

    @parameterize_and_serialize
    def member_func(self, x, y):
        result = self.value * (x + y)
        print(f"member_func Result: {result}")

    @classmethod
    @parameterize_and_serialize
    def class_method(cls, x, y):
        result = x * y
        print(f"class_method Result: {result}")

    @staticmethod
    @parameterize_and_serialize
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

# Call the member_func with parameters
my_instance.member_func(5, 2)

# Call the class_method with parameters
MyClass.class_method(3, 4)

# Call the static_method with parameters
MyClass.static_method(6, 7)

# Call the standalone function
standalone_function(8, 9)


# Player side to run from .json files
def run_from_json(file_name):
    with open(file_name, 'r') as file:
        parameter_json = file.read()
    parameterization = jsonpickle.decode(parameter_json)

    if parameterization["instance_data"]:
        instance = parameterization["instance_data"]
        method = getattr(instance, parameterization["name"])
        method(*parameterization["args"][1:], **parameterization["kwargs"])
    else:
        # method = getattr(instance, parameterization["name"])
        standalone_function(*parameterization["args"], **parameterization["kwargs"])

print("****")

# Run examples from .json files
run_from_json('parameterization_member_func.json')
run_from_json('parameterization_class_method.json')
run_from_json('parameterization_static_method.json')
run_from_json('parameterization_standalone_function.json')
