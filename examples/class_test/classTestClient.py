from decorator.decorators import JSONClassDumper, JSONFunctionDumper

# ------- Settings -----------------------------------
isClassDumperActive = True
# ----------------------------------------------------


# @JSONClassDumper(active=isClassDumperActive)
class ClassTestee:
    # FIXME class variables: how to deal with them?
    classVariable = 0
    def __init__(self, p_a: int):
        self.a = p_a

    # @JSONFunctionDumper(active=isClassDumperActive)
    def __str__(self)->str:
        return f'ClassTestee: {str(self.a)}'

    @JSONFunctionDumper(active=isClassDumperActive)
    @classmethod
    def clsm(cls):
        ClassTestee.classVariable += 1
        return "classmethod called"

    @JSONFunctionDumper(active=isClassDumperActive)
    @staticmethod
    def stm():
        ClassTestee.classVariable += 1
        return "staticmethod called"

    @JSONFunctionDumper(active=isClassDumperActive)
    def some_func(self):
        print(self.a)
        return self.a


@JSONFunctionDumper(active=isClassDumperActive)
def some_func(a):
    print(a)
    return a


if __name__ == "__main__":
    for i in range(-1, 3):
        a = ClassTestee(i)
        b = ClassTestee(i)

        # import os
        # with open(os.path.join('test_folder', f'{str(i)}'), "w") as f:
        #     f.write(json.dumps(a.__dict__))

        # _obj = ClassTestee(0)
        # _obj.__dict__ = json.load(open(os.path.join('test_folder', f'{str(i)}'), 'r'))
        # print(_obj)

        print(a.some_func())
        # print(a)
        print(ClassTestee.clsm())
        # print(ClassTestee.stm())

print(some_func(1))
