import jsonpickle
from jsonpickle import handlers

class DictHandler(handlers.BaseHandler):
    def flatten(self, obj, data):
        # if isinstance(obj, dict):
        #     pass
        return obj

    def restore(self, data):
        # Customize how the dict is deserialized
        return data


test = {"a": 2}

# class Foo:
#     def __init__(self, a=2):
#         self.a = a

jsonpickle.handlers.register(dict, DictHandler)


# test = Foo(2)

print(jsonpickle.dumps(test))