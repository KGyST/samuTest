# SamuTeszt

## What is this?
This is a unit-testing metaframework (built on top of unittest and pytest) that makes it possible to automatize both the test writing ("Recording") and testing itself ("Playing").
## How it works
Instead of writing test functions, one only has to put a decorator to the function to be tested. 
Anytime (if conditions met; during functional testing or even in production) the decorator dumps out function arguments (like args, kwargs, global variables etc.) and the results (returned values, raised exceptions, modified values of global variables) into data (by default .json) files.
This is the "Recording" phase.

When running tests ("Playing"), the test runner function reads all data files, calls the function according the data in them and compares the results. If the test fails, it writes another data file (or record), making it easy to compare the expected and the given result.
## Development Driven Testing Manifesto

## TODOs

- A `FunctionData` class, with `PreFunctiodData(FunctionData)` and `PostFunctionData(FunctionData)` subclasses, also for mocked functions. Maybe checking state inbetween.
  - Global variable handling pre/post, handled by the same `FunctionData` class
  - Function mocking
- Parametrization, new parameters
  - `run_only`
- Test fixtures and `__init__.json` 
- Packaging and distribution
  - Case names
  - Importing issues
- Test runner:
  - Simple test runner, PyCharm integration
- Config object
  - .json, .yaml, .xml
    - these encoders plus pickler as DI
  - Dumping into a database instead of files
- `current.json` issues rotating (.001, .002 etc)
  - Driving it through a local bool variable
- `@JSONFunctionDumper` to be able to be run as `@JSONFunctionDumper` (not only as `@JSONFunctionDumper()`)
- If `tests` is not a subfolder of the tested function, it's not possible to import the module (no `folder.module`)
- A `isValid()` function for all Codecs (`tryToInterpret()`)
- Property handling (.setter etc.)

---

- Case tagging, plus via params
  - Automatically tag when a test fails
- 1000s of cases: sorting
- Assertions
- Logging facility integration instead of prints
- Self.tests: running all the examples: record and play
- `__slots__` handling

## Version history
- 0.02: 231123 Object-oriented functions except for class attributes and `__new__()` 
- 0.03: 240913 Redesign + more object-oriented functions except for properties 
