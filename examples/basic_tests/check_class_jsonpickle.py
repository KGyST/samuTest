from jsonpickle import encode, decode

class MyClass(object):
    x = 1
    y = 2

obj = MyClass()

# Kiírja az objektum publikus tulajdonságait
json_data = encode(obj)
print(json_data)
# {"x": 1, "y": 2}

# Kiírja az osztályváltozókat is
json_data = encode(obj, include_properties=True)
print(json_data)
# {"x": 1, "y": 2, "__class__": "MyClass", "__module__": "__main__"}
