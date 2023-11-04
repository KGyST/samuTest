#check_member_function.py

import jsonpickle
from check_wrapper_function import ParameterizeSwitch

# Player side to run from .json files
def run_from_json(file_name):
    apply_wrapper = False

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
    class_value = 0

    def __init__(self, value):
        self.value = value
        MyClass.class_value = value

    # @ParameterizeSwitch(apply_wrapper)
    def dummy_func(self, x, y):
        result = self.value * (x + y)
        print(f"dummy_func Result: {result}")

    @ParameterizeSwitch(apply_wrapper)
    @classmethod
    def class_method(cls, x, y):
        result = x * y * cls.class_value
        print(f"class_method Result: {result}")

    # @ParameterizeSwitch(apply_wrapper)
    @staticmethod
    def static_method(x, y):
        result = x * y
        print(f"static_method Result: {result}")

    def __repr__(self):
        return f"MyClass(value={self.value})"


# Standalone function
# @ParameterizeSwitch(apply_wrapper)
def standalone_function(x, y):
    result = x * y
    print(f"standalone_function Result: {result}")


# Instantiate the class
my_instance = MyClass(value=100)

# Call the dummy_func with parameters
# my_instance.dummy_func(5, 2)

# Call the class_method with parameters
# my_instance.class_method(3, 4)
MyClass.class_method(1,1)

# Call the static_method with parameters
# MyClass.static_method(6, 7)

# Serialize parameters for standalone function
# standalone_function(10, 11)

# Run examples from .json files
# run_from_json('parameterization_dummy_func.json', apply_wrapper=False)
run_from_json('parameterization_class_method.json')
# run_from_json('parameterization_static_method.json', apply_wrapper=False)
# run_from_json('parameterization_standalone_function.json', apply_wrapper=False)

# print(locals())
# print(globals())