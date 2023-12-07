#try_classes.py

from classTestClient import *

if __name__ == "__main__":
    ct1 = ClassTestee(1)

    print(ct1.class_method(1))
    print(ct1.static_method(1))
    print(ct1.member_method(1))

    print(ClassTestee.class_method(1))
    print(ClassTestee.static_method(1))

    print(some_function("Something"))