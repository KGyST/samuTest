class MyTemplateClass:
    # def __init__(self):
    #     self.class_variable = None

    def some_method(self):
        print("This is a custom method")

class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        class_variable = attrs.get('class_variable', None)
        new_class = super(MyMeta, cls).__new__(cls, name, bases, attrs)
        new_class.class_variable = class_variable
        return new_class

# Create a class using MyMeta based on the MyTemplateClass
class1 = MyMeta("Class1", (MyTemplateClass,), {'class_variable': 1})

# Usage
instance1 = class1()
print(instance1.class_variable)  # This will print 1
instance1.some_class_method()  # This will call the custom method
