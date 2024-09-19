from jsonpickle import encode, decode

class MyClass(object):
    x = 1
    y = 2

obj = MyClass()

# Ki�rja az objektum publikus tulajdons�gait
json_data = encode(obj)
print(json_data)
# {"x": 1, "y": 2}

# Ki�rja az oszt�lyv�ltoz�kat is
json_data = encode(obj, include_properties=True)
print(json_data)
# {"x": 1, "y": 2, "__class__": "MyClass", "__module__": "__main__"}
