#check_value_passed_decorator.py


class WrapperFunctor:
    doRun = True

    def __call__(self, func, *args, **kwargs):
        if self.doRun:
            print("doRun")
        def wrapped_function(*argsWrap, **kwargsWrap):
            return func(*argsWrap, **kwargsWrap)

        return wrapped_function


