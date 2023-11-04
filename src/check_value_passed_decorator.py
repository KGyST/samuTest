#check_value_passed_decorator.py


class WrapperFunctor:
    def __init__(self, p_doRun:bool=True):
        self.doRun = p_doRun

    def __call__(self, func, *args, **kwargs):
        if self.doRun:
            print("doRun")
        def wrapped_function(*argsWrap, **kwargsWrap):
            return func(*argsWrap, **kwargsWrap)

        return wrapped_function


