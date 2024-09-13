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
    def staticMethod():
        pass


class ExampleException(Exception):
    exceptionClassVariable = "ExampleException Class Variable"


class ClassTestee:
    classVariable = 0

    @Dumper(active=isFunctionDumperActive)
    def __new__(cls, *args, **kwargs):
        _instance = super().__new__(cls)
        _instance.__class__.classVariable += 1
        return _instance

    @Dumper(active=isFunctionDumperActive)
    def __init__(self, param):
        self.instance_variable = param
        self.nestedInstance = ClassToBeNested()
        self._someProperty = param

    @Dumper()
    def __str__(self) -> str:
        return f'ClassTestee: {str(self.instance_variable)}'

    @Dumper()
    @classmethod
    def class_method(cls, param=1) -> str:
        print(f"BEGIN class_method, ClassTestee.classVariable = {ClassTestee.classVariable}")
        ClassTestee.classVariable += param
        print(f"END class_method, ClassTestee.classVariable = {ClassTestee.classVariable}")
        return "classmethod called"

    @Dumper()
    @staticmethod
    def static_method(param=1) -> str:
        print(f"static_method called {param}")
        return "staticmethod called"

    @Dumper()
    def member_method(self, param=1):
        print(f"BEGIN member_method called, instance_variable = {self.instance_variable}")
        # self.instance_variable += ClassTestee.classVariable + p_var
        self.instance_variable += param
        print(f"END member_method called, instance_variable = {self.instance_variable}")
        return self.instance_variable

    @Dumper(active=True, exceptions=(ExampleException, ))
    def member_method_that_throws_exception(self):
        print(f"member_method_that_throws_exception called, instance_variable = {self.instance_variable}")
        raise ExampleException()

    # FIXME property handling
    # @Dumper()
    @property
    def someProperty(self):
        print(f"someProperty called, instance_variable = {self._someProperty}")
        return self._someProperty

    # FIXME property handling
    # @Dumper()
    @someProperty.setter
    def someProperty(self, value):
        self._someProperty = value

    # FIXME assertions


@Dumper()
def some_function(param="Nothing"):
    print(f"some_function called, param = {param}")
    print(param)
    return param


if __name__ == "__main__":
    classTestee_member_object = ClassTestee(2)
    classTestee_member_object.someProperty = 3

    print(classTestee_member_object)
    print(classTestee_member_object.class_method(2))
    print(classTestee_member_object.static_method(2))
    print(classTestee_member_object.member_method(2))
    print(classTestee_member_object.someProperty)
    try:
        print(classTestee_member_object.member_method_that_throws_exception())
    except ExampleException:
        pass
    print(ClassTestee.class_method(2))
    print(ClassTestee.static_method(2))

    print(some_function("Something"))

