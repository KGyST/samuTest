class LoggerMeta(type):
    @property
    def class_attrib(cls):
        return cls._class_attrib

    @class_attrib.setter
    def class_attrib(cls, value):
        cls._class_attrib = value


class Logger(metaclass=LoggerMeta):
    _class_attrib = 11

    def __init__(self, logger_arg):
        self.logger_instance = None
        self.logger_arg = logger_arg

    def __call__(self, func):
        self.logger_instance = _Logger(func, self)
        return self.logger_instance


class _Logger:
    def __init__(self, func, logger_instance):
        self.func = func
        self.logger_instance = logger_instance
        self.extra_attr = None  # Attribute to be set later

    def __call__(self, *args, **kwargs):
        print(f"Function {self.func.__name__} | args: {args} | kwargs: {kwargs}")
        print(f"Class Attrib: {self.logger_instance.__class__.class_attrib}")
        print(f"Logger Arg: {self.logger_instance.logger_arg}")
        print(f"Extra Attr: {self.extra_attr}")
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner):
        if isinstance(self.func, classmethod):
            self.func = self.func.__get__(owner, owner)
        elif isinstance(self.func, staticmethod):
            self.func = self.func.__get__(None, owner)
        else:
            self.func = self.func.__get__(instance, owner)
        return self.__call__


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


@Logger(9)
def standalone_function(some_var: str, *args, **kwargs):
    print(f"Standalone function: {some_var}")
    print(f"Standalone function args: {args}")
    print(f"Standalone function kwargs: {kwargs}")


if __name__ == '__main__':
    some_instance = SomeClass()

    # Class method called by instance
    some_instance.class_method('Test2', "class_method_called_by_instance", a2="class_method_called_by_instance",
                               b2="class_method_called_by_instance")
    print('---')

    print(Logger.class_attrib)
    Logger.class_attrib = 22
    print(Logger.class_attrib)

    # Instance method
    some_instance.instance_method("Test3", "instance", a3="instance_a", b3="instance_b")
    print('---')

    # Static method
    SomeClass.static_method('Test4', "static", a4="static_a", b4="static_b")
    print('---')

    # Standalone function
    standalone_function('Test5', "standalone", a5="standalone_a", b5="standalone_b")
    print('---')

    Logger.class_attrib = 33

    # Class method called by class
    SomeClass.class_method("Test1", "class", a1="class_a", b1="class_b")
    print('---')
