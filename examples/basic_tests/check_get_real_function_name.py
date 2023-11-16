# main.py

from check_get_real_function_name_module import MyClass, my_function, get_original_function_name

# Getting real names from module_example
module_name_method, class_name_method, real_name_method = get_original_function_name(MyClass.my_method)
module_name_function, class_name_function, real_name_function = get_original_function_name(my_function)

print("Real name of the method in main:", module_name_method, class_name_method, real_name_method)
print("Real name of the function in main:", module_name_function, class_name_function, real_name_function)
