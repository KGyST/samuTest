from decorator import Dumper

# ------- Global settings example --------------------
isFunctionDumperActive = True
# ----------------------------------------------------

class ClassToBeNested:
    nestedClassVariable = 1
    def __init__(self):
        self.nestedInstanceVariable = 2

    def puclicMemberMethod(self):
        pass

    def _privateMemberMethod(self):
        pass

    @classmethod
    def classMethod(cls):
        pass

    @staticmethod
    def statiMethod():
        pass


class ExampleException(Exception):
    exceptionClassVariable = "ExampleException Class Variable"


class ClassTestee:
    classVariable = 0

    # @Dumper(active=isFunctionDumperActive)
    def __new__(cls, *args, **kwargs):
        _instance = super().__new__(cls)
        _instance.__class__.classVariable += 1
        return _instance

    # @Dumper(active=isFunctionDumperActive)
    def __init__(self, param):
        self.instance_variable = param
        self.nestedInstance = ClassToBeNested()

    # @Dumper(active=isFunctionDumperActive)
    def __str__(self) -> str:
        return f'ClassTestee: {str(self.instance_variable)}'

    # @Dumper(active=isFunctionDumperActive)
    @classmethod
    def class_method(cls, param=1) -> str:
        print(f"BEGIN class_method, ClassTestee.classVariable = {ClassTestee.classVariable}")
        ClassTestee.classVariable += param
        print(f"END class_method, ClassTestee.classVariable = {ClassTestee.classVariable}")
        return "classmethod called"

    # @Dumper(active=isFunctionDumperActive)
    @staticmethod
    def static_method(param=1) -> str:
        print(f"static_method called {param}")
        return "staticmethod called"

    @Dumper(active=isFunctionDumperActive)
    def member_method(self, param=1):
        print(f"BEGIN member_method called, instance_variable = {self.instance_variable}")
        # self.instance_variable += ClassTestee.classVariable + p_var
        self.instance_variable += param
        print(f"END member_method called, instance_variable = {self.instance_variable}")
        return self.instance_variable

    # @Dumper(active=True, exceptions=[ExampleException])
    def member_method_that_throws_exception(self):
        raise ExampleException()


# @Dumper(active=isFunctionDumperActive)
def some_function(param="Nothing"):
    print(param)
    return param


if __name__ == "__main__":
    classTestee_object = ClassTestee(1)

    print(classTestee_object)

    print(classTestee_object.class_method(1))
    print(classTestee_object.static_method(1))
    print(classTestee_object.member_method(1))
    try:
        print(classTestee_object.member_method_that_throws_exception())
    except ExampleException:
        pass

    print(ClassTestee.class_method(1))
    print(ClassTestee.static_method(1))

    print(some_function("Something"))

