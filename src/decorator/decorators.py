import jsonpickle
import os
import hashlib
from common.constants import ERROR_STR, WINMERGE_TEMPLATE
from common.privateFunctions import generateFolder
from io import StringIO
from typing import Callable
import importlib, inspect


class DumperBase:
    """
    Decorator functor to modify the tested functions
    Reason for having a Base class is for potentially being able to inherit into an xml or yaml writer
    """
    # FIXME mocked functions
    # FIXME global vars handling
    active = True

    class DumperException(Exception):
        pass

    def __init__(self,
                 testExt: str,                       #test default name, like .json
                 fExport: Callable,                  #data export function, like jsondumper
                 target_folder: str=".",             #place everything into this dir
                 current_test_name: str ="current",  #test default name, like current
                 active: bool=True,                  #global on/off switch of the test dumper
                 generate_files: bool=True,          #generate files, typically for the first run
                 nNameHex: int=12):                  #for default testcase filename generating
        self.sTargetFolder = target_folder
        self.sDefaultTest = current_test_name
        self.isActive = active
        self.nNameHex = nNameHex
        self.sExt = testExt
        self.fExport = fExport
        self.bGenerateFiles = generate_files

    def __initFiles(self):
        if not os.path.exists(sWinMergePath := os.path.join(self.sTargetFolder, self.sTest + ".WinMerge")) \
                and not os.path.exists(self.sFolder) \
                and not os.path.exists(self.sFolder + ERROR_STR):
            import xml.etree.ElementTree as ET
            tree = ET.parse(StringIO(WINMERGE_TEMPLATE))
            root = tree.getroot()
            root.find('paths/left').text = self.sFolder
            root.find('paths/right').text = self.sFolder + ERROR_STR
            tree.write(sWinMergePath)

            generateFolder(self.sFolder)

    # Very much misleading, this __call__ is called only once, at the beginning to create wrapped_function:
    def __call__(self, func: Callable, *args, **kwargs):
        if not self.active:
            return func
        self.sTest = func.__name__
        self.sFolder = os.path.join(os.getcwd(), self.sTargetFolder, self.sTest)
        if self.bGenerateFiles:
            self.__initFiles()

        def wrapped_function(*argsWrap, **kwargsWrap):
            fResult = None
            try:
                fResult = func(*argsWrap, **kwargsWrap)
                if self.isActive:
                    raise self.DumperException()
                return fResult
            except TypeError as e:
                pass
            except Exception as e:
                sOutput = self.fExport({"args": argsWrap,
                                 "kwargs": kwargsWrap,
                                 "result": fResult,
                                 "function": None,
                                 "module": None,
                                },
                               )
                sHash = hashlib.md5(sOutput.encode("ansi")).hexdigest()[:self.nNameHex]
                fileName = self.sTest + "_" + sHash + self.sExt

                if self.isActive:
                    #Like current.json:
                    with open(os.path.join(self.sFolder, fileName), "w") as f:
                        f.write(sOutput)
                    # sOutput['name'] = 'Current test'
                    with open(os.path.join(self.sFolder, self.sDefaultTest + self.sExt), "w") as f:
                        f.write(sOutput)
                return fResult
        wrapped_function.__name__ = func.__name__
        return wrapped_function


class JSONDumper(DumperBase):
    def __init__(self, *args, **kwargs):
        def jsonEx(p_sDict):
            return jsonpickle.dumps(p_sDict, indent=4)
        super() .__init__(".json", jsonEx, *args, **kwargs)

    def __call__(self, func: Callable, *args, **kwargs):
        return super().__call__(func, *args, **kwargs)


class JSONClassDumper:
    # FIXME class variables as properties?
    def __init__(self,
                 target_folder: str=".",             #place everything into this dir
                 nNameHex: int = 12
                 ):
        self.sTargetFolder = target_folder
        self.nNameHex = nNameHex
        self.sExt = ".json"


    def __call__(self, cls):
        generateFolder(os.path.join(self.sTargetFolder, cls.__name__))

        class DecoratedClass(cls):
            sTargetFolder = self.sTargetFolder
            nNameHex = self.nNameHex
            sExt = self.sExt
            sTest = cls.__name__

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                sDict = {"args": args,
                         "kwargs": kwargs,
                         # "module": importlib.import_module(cls.__module__),
                         "path": inspect.getsourcefile(importlib.import_module(cls.__module__)),
                         "result": cls(*args, **kwargs)}
                sOutput = jsonpickle.dumps(sDict, indent=4)
                sHash = hashlib.md5(sOutput.encode("ansi")).hexdigest()[:self.nNameHex]
                fileName = self.sTest + "_" + sHash + self.sExt

                with open(os.path.join(os.getcwd(), self.sTargetFolder, self.sTest, fileName), "w") as f:
                    f.write(sOutput)
        DecoratedClass.__name__ = cls.__name__
        return DecoratedClass

