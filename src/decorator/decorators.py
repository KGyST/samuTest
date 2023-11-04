import jsonpickle
import os
import hashlib
from common.constants import ERROR_STR, WINMERGE_TEMPLATE
from common.privateFunctions import generateFolder, open_and_create_folders
from io import StringIO
from typing import Callable, Type
import inspect
from copy import deepcopy


class DumperBase:
    # FIXME mocked functions
    # FIXME global vars handling
    isActive = False

    class DumperException(Exception):
        pass
    def __init__(self,
                 testExt: str,                       #test default name, like '.json'
                 fExport: Callable,                  #data export function, like jsondumper
                 target_folder: str="test",          #place everything into this dir
                 current_test_name: str ="current",  #test default name, like current
                 active: bool=False,                 #global on/off switch of the test dumper
                 generate_files: bool=True,          #generate files, typically for the first run
                 nNameHex: int=12):                  #for default testcase filename generating
        self.sTargetFolder = target_folder
        self.sDefaultTest = current_test_name
        self.isActive = active
        self.nNameHex = nNameHex
        self.sExt = testExt
        self.fExport = fExport
        self.bGenerateFiles = generate_files

    def __call__(self, func_or_class, *args, **kwargs):
        if not self.isActive:
            return func_or_class
        self.sTest = func_or_class.__name__
        self.sFolder = os.path.join(self.sTargetFolder, self.sTest)
        if self.bGenerateFiles:
            self._initFiles()

    def _initFiles(self):
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

    def dump(self, argsWrap, kwargsWrap, func_or_class, dResult: dict):
        _dict = {"args": argsWrap,
                "kwargs": kwargsWrap,
                "function": func_or_class.__name__,
                "module": os.path.splitext(os.path.basename(inspect.getmodule(func_or_class).__file__))[0],
                }
        sHash = hashlib.md5(self.fExport(_dict).encode("ansi")).hexdigest()[:self.nNameHex]

        fileName = "".join((self.sTest, "_", sHash, self.sExt))

        _dict.update(dResult)

        sOutput = self.fExport(_dict)

        # Like current.json:
        with open_and_create_folders(os.path.join(self.sFolder, fileName), "w") as f:
            f.write(sOutput)
        # sOutput['name'] = 'Current test'
        with open_and_create_folders(os.path.join(self.sTargetFolder, self.sDefaultTest + self.sExt), "w") as f:
            f.write(sOutput)
        with open_and_create_folders(os.path.join(os.getcwd(), self.sTargetFolder, self.sTest, fileName), "w") as f:
            f.write(sOutput)


class FunctionDumper(DumperBase):
    """
    Decorator functor to modify the tested functions
    Reason for having a Base class is for potentially being able to inherit into an xml or yaml writer
    """
    isActive = False

    # Very much misleading, this __call__ is called only once, at the beginning to create wrapped_function:
    def __call__(self, func, *args, **kwargs):
        super().__call__(func, *args, **kwargs)
        # FIXME why here?:
        fDump = super().dump
        if not self.isActive:
            return func

        dResult = {}

        if '.' in func.__qualname__:
            class_name, function_name = func.__qualname__.rsplit('.', 1)
        else:
            class_name, function_name = None, func.__qualname__

        dResult.update({
            "class_name": class_name,
            "function_name": function_name,
        })

        def wrapped_function(*argsWrap, **kwargsWrap):
            fResult = None
            try:
                if argsWrap and hasattr(argsWrap[0], '__dict__'):
                    instance = deepcopy(argsWrap[0])
                else:
                    instance = None

                if argsWrap and hasattr(instance, '__dict__'):
                    dResult.update({"instance_data_pre": instance})

                from importlib import import_module
                _mod = import_module(func.__module__)
                # _ = getattr(_mod, class_name)
                # locals()[class_name] = getattr(_mod, class_name)
                # globals()[class_name] = getattr(_mod, class_name)

                if isinstance(func, classmethod):
                    if not instance:
                        _class = getattr(_mod, class_name)
                        fResult = func.__func__(_class, *argsWrap, **kwargsWrap)
                    else:
                        fResult = func.__func__(*argsWrap, **kwargsWrap)
                elif isinstance(func, staticmethod):
                    fResult = func(*argsWrap[1:], **kwargsWrap)
                else:
                    if not instance:
                        fResult = func(*argsWrap, **kwargsWrap)
                    else:
                        fResult = func(instance, *argsWrap[1:], **kwargsWrap)
            except (Exception, TypeError, ZeroDivisionError) as e:
                # FIXME
                raise
            else:
                dResult.update({"result": fResult})
                dResult.update({"instance_data_post": instance})

                fDump(argsWrap, kwargsWrap, func, dResult)

                return fResult
        wrapped_function.__name__ = func.__name__
        return wrapped_function


class MemberFuncttionDumper(FunctionDumper):
    def __call__(self, func, *args, **kwargs):
        super().__call__(func, *args, **kwargs,)
        dResult = {}
        dResult.update({"self": self.__class__.__dict__})


class ClassDumper(DumperBase):
    # FIXME class variables as properties?

    def __call__(self, cls: Type, *args, **kwargs):
        super().__call__(cls, *args, **kwargs)
        generateFolder(os.path.join(self.sTargetFolder, cls.__name__))
        fDump = super().dump

        class DecoratedClass(cls):
            sTargetFolder = self.sTargetFolder
            nNameHex = self.nNameHex
            sExt = self.sExt
            sTest = cls.__name__

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                if DumperBase.isActive:
                    return
                dResult = {"result": cls(*args, **kwargs)}

                fDump(args, kwargs, cls, dResult)
        DecoratedClass.__name__ = cls.__name__
        return DecoratedClass


class JSONDumper(DumperBase):
    def __init__(self, *args, **kwargs):
        def jsonEx(p_sDict):
            return jsonpickle.dumps(p_sDict, indent=4, make_refs=False)
        super() .__init__(".json", jsonEx, *args, **kwargs)


class YAMLDumper(DumperBase):
    def __init__(self, *args, **kwargs):
        import yaml
        super() .__init__(".yaml", yaml.dump, *args, **kwargs)


class JSONFunctionDumper(JSONDumper, FunctionDumper, ):
    pass


class YAMLFunctionDumper(YAMLDumper, FunctionDumper, ):
    pass


class JSONClassDumper(JSONDumper, ClassDumper):
    pass


class YAMLClassDumper(YAMLDumper, ClassDumper):
    pass

