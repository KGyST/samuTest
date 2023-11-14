from typing import Callable

def ZeroDivisionErrorCatcher(func: Callable):
    def fResult(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return None
    return fResult