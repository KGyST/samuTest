from decorator.decorators import JSONFunctionDumper

# ------- Settings -----------------------------------
isFunctionDumperActive = True
# ----------------------------------------------------


class ClassTestee:
    classVariable = 0
    @JSONFunctionDumper(active=isFunctionDumperActive)
    def __init__(self, p_var):
        self.instance_variable = p_var

    @JSONFunctionDumper(active=isFunctionDumperActive)
    def __str__(self)->str:
        return f'ClassTestee: {str(self.instance_variable)}'

    @JSONFunctionDumper(active=isFunctionDumperActive)
    @classmethod
    def class_method(cls, p_var=1)->str:
        print(f"BEGIN class_method, ClassTestee.classVariable = {ClassTestee.classVariable}")
        ClassTestee.classVariable += p_var
        print(f"END class_method, ClassTestee.classVariable = {ClassTestee.classVariable}")
        return "classmethod called"

    @JSONFunctionDumper(active=isFunctionDumperActive)
    @staticmethod
    def static_method(p_var=1)->str:
        print(f"static_method called {p_var}")
        return "staticmethod called"

    @JSONFunctionDumper(active=isFunctionDumperActive)
    def member_method(self, p_var = 1):
        print(f"BEGIN member_method called, instance_variable = {self.instance_variable}")
        # self.instance_variable += ClassTestee.classVariable + p_var
        self.instance_variable += p_var
        print(f"END member_method called, instance_variable = {self.instance_variable}")
        return self.instance_variable


@JSONFunctionDumper(active=isFunctionDumperActive)
def some_function(p_var="Nothing"):
    print(p_var)
    return p_var


if __name__ == "__main__":
    classTestee_object = ClassTestee(1)

    print(classTestee_object)

    print(classTestee_object.class_method(1))
    print(classTestee_object.static_method(1))
    print(classTestee_object.member_method(1))

    print(ClassTestee.class_method(1))
    print(ClassTestee.static_method(1))

    print(some_function("Something"))

