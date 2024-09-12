import copy

import hashlib
import os.path

from common.constants import *
from common.privateFunctions import md5Collector
import sys
from importlib import import_module
from common.ICodec import *
from types import FunctionType, MethodType
import inspect
from collections.abc import Callable


class _Dumper:
    """
    Decorator functor to modify the tested functions
    """

    # FIXME mocked functions
    # FIXME global vars handling

    bDump: bool | Callable = True

    class DumperException(Exception):
        pass

    def __init__(self, func, dumper_instance):  # for default testcase filename generating
        self.func = func
        self.dumperInstance = dumper_instance

        self.sModule: str
        self.sClass: str
        self.sFunction: str
        self.collectedMD5S = set()

        self.args_ = None
        self.kwargs_ = None
        self.preClass_ = None
        self.postClass_ = None
        self.preSelf_ = None
        self.postSelf_ = None
        self.result_ = None
        self.exception_ = None

        self.preGlobal_ = None
        self.postGlobal_ = None
        self._sTestMD5 = None

    def __get__(self, instance, owner):
        if not Dumper.bDump:
            return self.func
        Dumper.bDump = False
        # https://stackoverflow.com/questions/78928486/how-to-deduce-whether-a-classmethod-is-called-on-an-instance-or-on-a-class
        if isinstance(self.func, classmethod):
            self.preClass_ = copy.deepcopy(owner)
            self.func = self.func.__get__(owner, owner)
            self.postClass_ = owner
        elif isinstance(self.func, staticmethod):
            self.preClass_ = copy.deepcopy(owner)
            self.func = self.func.__get__(None, owner)
            self.postClass_ = owner
        else:
            self.preSelf_ = copy.deepcopy(instance)
            self.func = self.func.__get__(instance, owner)
            self.postSelf_ = instance
        Dumper.bDump = True
        return self.__call__

    # Misleading, this __call__ is called only once, at the beginning to create wrapped_function:
    def __call__(self, *argsWrap, **kwargsWrap):
        if not Dumper.bDump:
            return self.func(*argsWrap, **kwargsWrap)
        _bDump = Dumper.bDump
        Dumper.bDump = False

        from common.privateFunctions import get_original_function_name

        self.sModule, self.sClass, self.sFunction = get_original_function_name(self.func)

        _mod = import_module(self.sModule)

        self.collectedMD5S.update(md5Collector(self.dumperInstance.codec, self.sRelativeDir))

        self.args_ = copy.deepcopy(argsWrap)
        self.kwargs_ = copy.deepcopy(kwargsWrap)

        try:
            self.result_ = self.func(*argsWrap, **kwargsWrap)
        except Exception as e:
            self.exception_ = e
            if (e.__class__ in self.dumperInstance.tExceptions) == self.dumperInstance.bIncludeExceptions:
                self.bDump = True
            elif e.__class__ == KeyboardInterrupt:
                self.sTest = CURRENT
                self.bDump = True
            raise
        finally:
            if self.bDump and _bDump:
                if not self.sTestMD5 in self.collectedMD5S or self.dumperInstance.bOverwrite:
                    self.dump()
            elif isinstance(_bDump, FunctionType):
                # FIXME
                if self.bDump() == True:
                    self.dump()
        Dumper.bDump = _bDump
        return self.result_

    @property
    def dPre(self) -> dict:
        return {
            MODULE_NAME: self.sModule,
            CLASS_NAME: self.sClass,
            FUNC_NAME: self.sFunction,
            ARGS: self._get_module(self.args_),
            KWARGS: self._get_module(self.kwargs_),
        }

    @property
    def sTestMD5(self) -> str:
        if self._sTestMD5 == None:
            self._sTestMD5 = hashlib.md5(self.dumperInstance.codec.dumps(self.dPre).encode("ansi")).hexdigest()[:self.dumperInstance.nNameHex]
        return self._sTestMD5

    @property
    def sDullyQualifiedTest(self) -> str:
        if self.sClass:
            return ".".join([self.sModule, self.sClass, self.sFunction])
        else:
            return ".".join([self.sModule, self.sFunction])

    @property
    def sRelativeDir(self) -> str:
        if self.sClass:
            return os.path.join(self.sModule, self.sClass, self.sFunction)
        else:
            return os.path.join(self.sModule, self.sFunction)

    @property
    def sFullDir(self) -> str:
        return os.path.join(self.dumperInstance.sTestRootDir, self.sRelativeDir)

    @property
    def sFullPath(self) -> str:
        return os.path.join(self.sFullDir, self.sTestMD5 + self.dumperInstance.codec.sExt)

    def dump(self):
        if self.postClass_ is not None:
            _class = self.postClass_
        elif self.postSelf_ is not None:
            _class = self.postSelf_.__class__
        else:
            _class = None

        dResult = {**self.dPre,
                   MD5: self.sTestMD5,
                   PRE: {},
                   POST: {}}

        dResult[PRE][SELF] = self._get_module(self.preSelf_)
        dResult[PRE][CLASS] = self._get_module(self.preClass_)
        # dResult[PRE][GLOBAL] = self._preGlobal
        dResult[POST][SELF] = self._get_module(self.postSelf_)
        dResult[POST][CLASS] = self._get_module(self.postClass_)
        # dResult[POST][GLOBAL] = self._postGlobal
        dResult[POST][RESULT] = self._get_module(self.result_)
        dResult[POST][EXCEPTION] = self._get_module(self.exception_)

        if (not os.path.exists(self.sFullPath)
                or self.dumperInstance.bOverwrite
                or self.sTest == CURRENT):
            self.dumperInstance.codec.dump(self.sFullPath, dResult)

    def _get_module(self, obj: object):
        """
        Replaces '__main__' module to the actual module name of any object.

        :param obj: any object, preferably not a primitive type (having __dict__) and from the __main__ module
        :return: the object with the replaced module
        """
        if hasattr(obj, "__module__") and obj.__module__ == "__main__":
            if isinstance(obj, type):
                sClass = obj.__name__
            else:
                sClass = obj.__class__.__name__
            _class = getattr(sys.modules.get(self.sModule, None), sClass, None)
            if _class and inspect.isclass(_class) and _class.__module__ != 'builtins':
                obj.__module__ = _class.__module__
            if not isinstance(obj, type):
                for attr_name in dir(obj):
                    try:
                        attr_value = getattr(obj, attr_name)
                        if attr_value.__class__.__module__ != "builtins":
                            updated_attr_value = self._get_module(attr_value)
                            setattr(obj, attr_name, self._get_module(updated_attr_value))
                    except (AttributeError, TypeError):
                        # Catch and handle any AttributeError (read-only attributes, etc.)
                        pass
        elif isinstance(obj, (list, tuple, set)):
            obj = type(obj)(self._get_module(item) for item in obj)
        elif isinstance(obj, dict):
            obj = {k: self._get_module(v) for k, v in obj.items()}
        # elif not isinstance(obj, type):
        #     for attr_name in dir(obj):
        #         try:
        #             attr_value = getattr(obj, attr_name)
        #             if attr_value.__class__.__module__ != "builtins":
        #                 updated_attr_value = self._get_module(attr_value)
        #                 setattr(obj, attr_name, self._get_module(updated_attr_value))
        #         except (AttributeError, TypeError):
        #             # Catch and handle any AttributeError (read-only attributes, etc.)
        #             pass
        return obj


class Dumper:
    bDump = True

    def __init__(self,
            codec: 'ICodec' = JSONCodec,
            overwrite: bool = True,
            target_dir: str = TEST_ITEMS,  # place everything into this dir
            active=False,  # global on/off switch of the test dumper
            # FIXME should be a (lambda) function based on criteria
            # FIXME when ran by test_runner, active should be False all the time
            exceptions: tuple[type] = (AssertionError, ),
            are_exceptions_included: bool = True,
            hex_name_length: int = 12, *args, **kwargs):
        self.dumper_instance = None
        self.bDump = active
        self.sTestRootDir = target_dir
        self.nNameHex = hex_name_length
        self.codec = codec
        self.bIncludeExceptions = are_exceptions_included
        self.tExceptions = exceptions if exceptions is not None else ()
        self.bOverwrite = overwrite

    def __call__(self, func):
        self.dumper_instance = _Dumper(func, self)
        return self.dumper_instance

