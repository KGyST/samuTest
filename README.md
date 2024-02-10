# SamuTest

## What is this?
This is a unit-testing metaframework (built on top of unittest and pytest) that makes it possible to automatize both the test writing ("Recording") and testing itself ("Playing").
## How it works
Instead of writing test functions, one only has to put a decorator to the function to be tested. 
Anytime (if conditions met; during functional testing or even in production) the decorator dumps out function arguments (like args, kwargs, global variables, etc) and the results (returned values, raised exceptions, modified values of global variables) into data (by default .json) files.
This is the "Recording" phase.

When running tests ("Playing"), the test runner function reads all data files, calls the function according the data in them and compares the results. If the test fails, it writes another data file (or record), making it easy to compare the expected and the given result.
## Development Driven Testing Manifesto

## TODOs
- PublicFunctions parameters fixes, docstrings
- Variable/parameter naming conventions
- `test_runner` considerations (these 4 should be implemented as classes):
  - file or DB
  - if file, json/xml/yaml/native pickle encoder/decoder as DI
  - unittest or pytest or something else
  - client program, like PyCharm or VS Code
- Folder structure *items/errors*
  - Class names in folder names, customizable
  - There should be a `tests` folder. If not in the actual folder, one has to handle the paths in order not to have two source files with the same name at different paths. 
    So multiple `tests` folders, each besides the actual source file.
  - Under it, a module(+ `_items` or not).(class.)function
    - Note that in Pycharm test tree structurization works by a simple string processing folders/subfolders are marked by simple dots, like `1.2.3`
    - It would be more elegant to create suites in a module/class/function manner. All these would be suites.
      This is only a by-default structure, so one can create a different folder structure.
      Folders should represent test suites, so test suite structure should be according to the folder structure.
  - ~~~Besides it, an `_errors`, like `module_errors`, and in it class/function.~~~
    - There will be a `test_errors` folder somewhere else (define, wheere) . Reasons for this:
      - excluded from git, not part of the source (unlike the `tests` folder). This is a temporary folder.
      - this way folder structure will be a perfect mirror, functions can be simpler. One WinMerge file is enought for comparison.
    - This structure follows the folder structure. 
  - And there a `.WinMerge`, like `module.WinMerge`
- Facelift/update outdated stuff
  - WinMerge
    - ... as an option, DI
    - Actually if there is a test/test_errors folder pair, maybe one central WinMerge file is enough.
- Exception as a result: handling + config
- Whether to run `current.json`
- Include or exclude
- Global variable handling pre/post

---

- Options to be added
- Parametrization, new parameters
  - `run_only`
- Function mocking
- Test fixtures and `__init__.json` 
- Packaging and distribution
  - Case names
- Test runner:
  - Simple test runner, PyCharm integration
  - Test stuites based on mod/class/func
- ~~MD5 checking: if another file with the same MD5 is there, but with another filename, don't write it.~~
- Config object
  - .json, .yaml, .xml
    - these encoders plus pickler as DI
  - Dumping into a database instead of files
- `current.json` issues rotating (.001, .002 etc)
  - Driving it through a local bool wariable
- `@JSONFunctionDumper` to be able to be run as `@JSONFunctionDumper` (not only as `@JSONFunctionDumper()`)
- If `tests` is not a subfolder of the tested function, it's not possible to import the module (no `folder.module`)
---
- Object-oriented issues
  - `__new__()` cannot be currently tested. 

## Version history
- 0.02: 231123 Object-oriented functions except for class attributes and `__new__()` 