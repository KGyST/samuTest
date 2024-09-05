class LoggerMeta:
    def __init__(self, *args, **kwargs):
        # Needed just to absorb args
        pass
        print(1)

    def __call__(self, logger_arg, *args, **kwargs):
        class _Logger:
            def __init__(self, func):
                self.func = func

            def __call__(self, *args, **kwargs):
                print(f"Function {self.func.__name__} | args: {args} | kwargs: {kwargs}")
                print(logger_arg)
                return self.func(*args, **kwargs)

            def __get__(self, instance, owner):
                # Ensure the method is correctly bound when accessed as a classmethod
                if isinstance(self.func, classmethod):
                    self.func = self.func.__get__(owner, owner)
                else:
                    self.func = self.func.__get__(instance, owner)
                return self.__call__
        return _Logger


class Logger(metaclass=LoggerMeta):
    pass


class SomeClass:
    @Logger(1)
    @classmethod
    def class_method(cls, some_var: str, *args, **kwargs):
        print(f"Class method: {some_var}")
        print(f"Class method args: {args}")
        print(f"Class method kwargs: {kwargs}")

    @Logger(2)
    def instance_method(self, some_var: str, *args, **kwargs):
        print(f"Instance method: {some_var}")
        print(f"Instance method args: {args}")
        print(f"Instance method kwargs: {kwargs}")

    @Logger(3)
    @staticmethod
    def static_method(some_var: str, *args, **kwargs):
        print(f"Static method: {some_var}")
        print(f"Static method args: {args}")
        print(f"Static method kwargs: {kwargs}")


@Logger(4)
def standalone_function(some_var: str, *args, **kwargs):
    print(f"Standalone function: {some_var}")
    print(f"Standalone function args: {args}")
    print(f"Standalone function kwargs: {kwargs}")


if __name__ == '__main__':
    some_instance = SomeClass()
    some_instance.class_method('Test2', "class_method_called_by_instance", a2="class_method_called_by_instance",
                               b2="class_method_called_by_instance")
    # some_instance.class_method('Test2')
    print('---')

    some_instance.instance_method("Test3", "instance", a3="instance_a", b3="instance_b")
    # some_instance.instance_method("Test3")
    print('---')

    SomeClass.static_method('Test4', "static", a4="static_a", b4="static_b")
    # SomeClass.static_method('Test4')
    print('---')

    standalone_function('Test5', "standalone", a5="standalone_a", b5="standalone_b")
    # standalone_function('Test5')
    print('---')

    SomeClass.class_method("Test1", "class", a1="class_a", b1="class_b")
    # SomeClass.class_method("Test1")
    print('---')