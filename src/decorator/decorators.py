import copy

import hashlib
import os.path
import types

from common.constants import *
from common.privateFunctions import md5Collector, get_original_function_name
from importlib import import_module
from common.ICodec import *
from types import FunctionType
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

        self.sModule, self.sClass, self.sFunction = get_original_function_name(self.func)

        import_module(self.sModule)

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
            ARGS: (self.args_ if not isinstance(self.func, types.MethodType) else [self.preSelf_, *self.args_]),
            KWARGS: (self.kwargs_),
        }

    @property
    def sTestMD5(self) -> str:
        # if self._sTestMD5 == None:
        _pre = self.dPre
        self._sTestMD5 = hashlib.md5(self.dumperInstance.codec.dumps(_pre).encode("utf-8")).hexdigest()[:self.dumperInstance.nNameHex]
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

        dResult[PRE][SELF] = self.preSelf_
        dResult[PRE][CLASS] = self.preClass_
        # dResult[PRE][GLOBAL] = self._preGlobal
        dResult[POST][SELF] = self.postSelf_
        dResult[POST][CLASS] = self.postClass_
        # dResult[POST][GLOBAL] = self._postGlobal
        dResult[POST][RESULT] = self.result_
        dResult[POST][EXCEPTION] = self.exception_

        if (not os.path.exists(self.sFullPath)
                or self.dumperInstance.bOverwrite
                or self.sTest == CURRENT):
            self.dumperInstance.codec.dump(self.sFullPath, dResult)


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

