import sys
from types import ModuleType

def create_virtual_module(module_name, module_content):
    """
    Create a virtual module without using exec.

    Parameters:
    - module_name: The name of the new module.
    - module_content: The content for the module.

    Returns:
    - The newly created module.
    """
    new_module = ModuleType(module_name)

    for item_name, item in module_content.items():
        setattr(new_module, item_name, item)

    # Set the module in sys.modules
    sys.modules[module_name] = new_module

    return new_module

# Example: Creating a virtual module with a class
module_content = {
    'FirstTestCase': type('FirstTestCase', (object,), {'test_example_1': lambda self: print("Test Example 1 executed.")})
}

# Specify the path where the virtual module would reside
module_path = "/path/to/virtual_module_folder"

create_virtual_module('path.to.virtual_module_folder.Class', module_content)

# Now you can use the new module
from path.to.virtual_module_folder.Class import FirstTestCase

if __name__ == "__main__":
    test_instance = FirstTestCase()
    test_instance.test_example_1()
