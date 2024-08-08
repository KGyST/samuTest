class CustomDebugException(Exception):
    def __init__(self):
        print ("CustomDebugException __init__")

def decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("KeyboardInterrupt caught")
        except CustomDebugException:
            print("CustomDebugException caught")
    return wrapper

@decorator
def my_function():
    # Some code here
    print("Test")

# Call the function normally
my_function()

