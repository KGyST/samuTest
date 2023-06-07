from typing import Callable

def ZeroDivisionErrorCatcher(p_func: Callable):
    def fResult(*args, **kwargs):
        try:
            return p_func(*args, **kwargs)
        except:
            return None
    fResult.__name__ = p_func.__name__
    fResult.__module__ = p_func.__module__
    return fResult