from decorator.decorators import JSONFunctionDumper

# ------- Settings -----------------------------------
isFunctionDumperActive = True
# ----------------------------------------------------

class ClassToBeNested:
    nestedClassVariable = 1
    def __init__(self):
        self.nestedInstanceVariable = 2


class ClassTestee:
    classVariable = 0
    @JSONFunctionDumper(active=isFunctionDumperActive)
    def __init__(self, param):
        self.instance_variable = param
        self.nestedInstance = ClassToBeNested()

    @JSONFunctionDumper(active=isFunctionDumperActive)
    def __str__(self)->str:
        return f'ClassTestee: {str(self.instance_variable)}'

    @JSONFunctionDumper(active=isFunctionDumperActive)
    @classmethod
    def class_method(cls, param=1)->str:
        print(f"BEGIN class_method, ClassTestee.classVariable = {ClassTestee.classVariable}")
        ClassTestee.classVariable += param
        print(f"END class_method, ClassTestee.classVariable = {ClassTestee.classVariable}")
        return "classmethod called"

    @JSONFunctionDumper(active=isFunctionDumperActive)
    @staticmethod
    def static_method(param=1)->str:
        print(f"static_method called {param}")
        return "staticmethod called"

    @JSONFunctionDumper(active=isFunctionDumperActive)
    def member_method(self, param = 1):
        print(f"BEGIN member_method called, instance_variable = {self.instance_variable}")
        # self.instance_variable += ClassTestee.classVariable + p_var
        self.instance_variable += param
        print(f"END member_method called, instance_variable = {self.instance_variable}")
        return self.instance_variable


@JSONFunctionDumper(active=isFunctionDumperActive)
def some_function(param="Nothing"):
    print(param)
    return param


if __name__ == "__main__":
    classTestee_object = ClassTestee(1)

    print(classTestee_object)

    print(classTestee_object.class_method(1))
    print(classTestee_object.static_method(1))
    print(classTestee_object.member_method(1))

    print(ClassTestee.class_method(1))
    print(ClassTestee.static_method(1))

    print(some_function("Something"))

