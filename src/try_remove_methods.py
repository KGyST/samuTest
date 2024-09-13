import jsonpickle
import types

class ExampleClass:
    classVariable = 5

    @classmethod
    def class_method(cls):
        pass

    def member_method(self):
        pass

    def member_method_that_throws_exception(self):
        raise Exception("Test Exception")

    @staticmethod
    def static_method():
        pass

class NoMethodHandler(jsonpickle.handlers.BaseHandler):
    def flatten(self, obj, data):
        obj_dict = {}
        for key, value in obj.__class__.__dict__.items():
            if not isinstance(value, (types.MethodType, types.FunctionType, staticmethod, classmethod)):
                obj_dict[key] = value
        return self.context.flatten(obj_dict, data)

# Register the handler for the specific class
jsonpickle.handlers.registry.register(ExampleClass, NoMethodHandler)

# Instantiate the class
data = ExampleClass()

# Serialize with jsonpickle
json_output = jsonpickle.dumps(data, indent=4, make_refs=False, include_properties=True)
print(json_output)
