from typing import Callable

def ZeroDivisionErrorCatcher(p_func: Callable):
    def fResult(p_):
        try:
            return p_func(p_)
        except:
            return None
    return fResult