# SamuTest

## What is this?
## How it works
## Development Driven Testing Manifesto

## TODOs
- PublicFunctions parameters fixes, docstrings
- Variable/parameter naming conventions
- Folder structure *items/errors*
  - Class names in folder names, customizable
  - There should be a `tests` folder. If not in the actual folder, one has to handle the paths in order not to have two source files with the same name at different paths. So multiple `tests` folders, each besides the actual source file.   
  - Under it, a (module).class.function (+ `_items`. or not)
  - Besides it, an `_errors`
  - And there a `.WinMerge`
- Facelift/update outdated stuff
  - ~~WinMerge~~
  - ... as an option
- Object-oriented issues
  - Class variable handling by metaclass
  - `__new__()` parameter anomalies 
---
- Global variable handling pre/post
- Options to be added
- Parametrization, new parameters
  - `run_only`
- Exception as a result handling + config
  - Whether to run `current.json` 
- Function mocking
- Test fixtures and `__init__.json` 
- Packaging and distribution
  - Case names
- Simple test runner, PyCharm integration
- ~~MD5 checking: if another file with the same MD5 is there, but with another filename, don't write it.~~
- Config object
  - .json, .yaml, .xml
- `current.json` issues rotating (.001, .002 etc) 