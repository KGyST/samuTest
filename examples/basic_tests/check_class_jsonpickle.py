class MyTemplateClass:
    pass
    # def __init__(self):
    #     self.__class__.class_variable = 2
    #
    # def some_method(self):
    #     print(f"This is a custom method {self.__class__.class_variable}")

class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(MyMeta, cls).__new__(cls, name, bases, attrs)
        new_class.class_variable = attrs.get('class_variable', None)
        return new_class

# Create a class using MyMeta based on the MyTemplateClass
class1 = MyMeta("MyTemplateClass", (MyTemplateClass,), {'class_variable': 5})

# Usage
instance1 = class1()
print(instance1.class_variable)  # This will print 1
print(class1.class_variable)  # This will print 1

print (vars(instance1))
