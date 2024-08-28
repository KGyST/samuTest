import copy
import functools

import hashlib
import os.path

from common.constants import *
from common.privateFunctions import get_original_function_name, md5Collector, _get_original_function
import sys
from importlib import import_module
from common.ICodec import *
from types import FunctionType, MethodType
import inspect


class Dumper:
    """
    Decorator functor to modify the tested functions
    """
    bDump = True

    # FIXME mocked functions
    # FIXME global vars handling

    class DumperException(Exception):
        pass

    def __init__(self,
                 codec: 'ICodec' = JSONCodec,
                 overwrite: bool = True,
                 target_dir: str = TEST_ITEMS,  # place everything into this dir
                 active=False,  # global on/off switch of the test dumper
                 # FIXME should be a (lambda) function based on criteria
                 # FIXME when ran by test_runner, active should be False all the time
                 exceptions: tuple[type] = (AssertionError, ),
                 are_exceptions_included: bool = True,
                 hex_name_length: int = 12):                  # for default testcase filename generating
        self.bDump = active
        self.sTestRootDir = target_dir
        self.nNameHex = hex_name_length
        self.codec = codec
        self.sModule: str
        self.sClass: str
        self.sFunction: str
        self.collectedMD5S = set()
        self.bIncludeExceptions = are_exceptions_included
        self.tExceptions = exceptions if exceptions is not None else ()
        self.bOverwrite = overwrite
        self._args = None
        self._kwargs = None
        self._preClass = None
        self._postClass = None
        self._preSelf = None
        self._postSelf = None
        self._result = None
        self._exception = None

        self._preGlobal = None
        self._postGlobal = None

    @classmethod
    def _undumpable(cls, func):
        _bDump = cls.bDump
        cls.bDump = False
        try:
            _res = func()
        finally:
            cls.bDump = _bDump
        return _res

    # Misleading, this __call__ is called only once, at the beginning to create wrapped_function:
    def __call__(self, func, *args, **kwargs):
        if not self.__class__.bDump:
            return func

        self.sModule, self.sClass, self.sFunction = get_original_function_name(func)

        _mod = self._undumpable(lambda: import_module(self.sModule))

        self.collectedMD5S.update(md5Collector(self.codec, self.getRelativeDirName()))
        self.sTest = self.getTestMD5()

        @functools.wraps(func)
        def wrapped_function(*argsWrap, **kwargsWrap):
            def _func():
                self._args = copy.deepcopy(argsWrap)
                self._kwargs = copy.deepcopy(kwargsWrap)
            self._undumpable(_func)

            try:
                if isinstance(func, classmethod):
                    _class = getattr(_mod, self.sClass)
                    self._preClass = copy.deepcopy(_class)
                    self._result = func.__func__(_class, *argsWrap[1:], **kwargsWrap)
                    self._postClass = _class
                elif isinstance(func, staticmethod):
                    # self._args = argsWrap
                    self._result = func(*argsWrap[1:], **kwargsWrap)
                elif isinstance(func, MethodType):
                    self._preSelf = copy.deepcopy(argsWrap[0])
                    self._result = func(*[argsWrap[0], *argsWrap[1:]], **kwargsWrap)
                    self._postSelf = argsWrap[0]
                elif isinstance(func, FunctionType):
                    # self._args = argsWrap
                    self._result = func(*argsWrap, **kwargsWrap)
            except Exception as e:
                self._exception = e
                if (e.__class__ in self.tExceptions) == self.bIncludeExceptions:
                    self.bDump = True
                elif e.__class__ == KeyboardInterrupt:
                    self.sTest = CURRENT
                    self.bDump = True
                raise
            finally:
                if self.bDump and self.__class__.bDump:
                    if not self.getTestMD5() in self.collectedMD5S or self.bOverwrite:
                        self.dump()
                elif isinstance(self.__class__.bDump, FunctionType):
                    # FIXME
                    if self.bDump() == True:
                        self.dump()
            return self._result
        return wrapped_function

    def getDict(self) -> dict:
        return {
            MODULE_NAME: self.sModule,
            CLASS_NAME: self.sClass,
            FUNC_NAME: self.sFunction,
            ARGS: self._get_module(self._args),
            KWARGS: self._get_module(self._kwargs),
        }

    def getTestMD5(self) -> str:
        return hashlib.md5(self.codec.dumps(self.getDict()).encode("ansi")).hexdigest()[:self.nNameHex]

    def getFullyQualifiedTestName(self) -> str:
        if self.sClass:
            return ".".join([self.sModule, self.sClass, self.sFunction])
        else:
            return ".".join([self.sModule, self.sFunction])

    def getRelativeDirName(self) -> str:
        if self.sClass:
            return os.path.join(self.sModule, self.sClass, self.sFunction)
        else:
            return os.path.join(self.sModule, self.sFunction)

    def getFullDirName(self) -> str:
        return os.path.join(self.sTestRootDir, self.getRelativeDirName())

    def getFullPath(self) -> str:
        return os.path.join(self.getFullDirName(), self.getTestMD5() + self.codec.sExt)

    def dump(self):
        if self._postClass is not None:
            _class = self._postClass
        elif self._postSelf is not None:
            _class = self._postSelf.__class__
        else:
            _class = None

        dResult = {**self.getDict(),
                   MD5: self.getTestMD5(),
                   PRE: {},
                   POST: {}}

        dResult[PRE][SELF] = self._get_module(self._preSelf)
        dResult[PRE][CLASS] = self._get_module(self._preClass)
        # dResult[PRE][GLOBAL] = self._preGlobal
        dResult[POST][SELF] = self._get_module(self._postSelf)
        dResult[POST][CLASS] = self._get_module(self._postClass)
        # dResult[POST][GLOBAL] = self._postGlobal
        dResult[POST][RESULT] = self._get_module(self._result)
        dResult[POST][EXCEPTION] = self._get_module(self._exception)

        if (not os.path.exists(self.getFullPath())
                or self.bOverwrite
                or self.sTest == CURRENT):
            self.codec.dump(self.getFullPath(), dResult)

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
                        setattr(obj, attr_name, self._get_module(attr_value))
                    except AttributeError:
                        pass
        elif isinstance(obj, (list, tuple)):
            obj = type(obj)(self._get_module(item) for item in obj)
        elif isinstance(obj, dict):
            obj = {k: self._get_module(v) for k, v in obj.items()}
        return obj

