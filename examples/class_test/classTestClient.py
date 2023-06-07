from decorator.decorators import JSONClassDumper

# ------- Settings -----------------------------------
isJSONClassDumperActive = True
# ----------------------------------------------------

@JSONClassDumper(active=isJSONClassDumperActive)
class ClassTestee():
    # FIXME class variables: how to deal with them?
    # classVariable = 0
    def __init__(self, p_a: int):
        self.a = p_a
        # self.classVariable += 1
        # ClassTestee.classVariable += 1

    def __str__(self)->str:
        return f'ClassTestee: {str(self.a)}'


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

        print(a)

