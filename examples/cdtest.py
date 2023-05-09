class CallCountDecorator:
    """
    A decorator that will count and print how many times the decorated function was called
    """

    def __init__(self, a):
        self.call_count = a


    def __call__(self, inline_func, *args, **kwargs):
        self.inline_func = inline_func
        def wrapper(*args, **kwargs):
            self.call_count += 1
            self._print_call_count()
            return self.inline_func(*args, **kwargs)
        return wrapper

    def _print_call_count(self):
        print(f"The {self.inline_func.__name__} called {self.call_count} times")


@CallCountDecorator(1)
def function():
    pass


@CallCountDecorator(200)
def function2(a, b):
    pass


if __name__ == "__main__":
    for i in range(10):
        function()
        function()
        function2(1, b=2)
