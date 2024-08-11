import copy
import functools

import hashlib
from common.constants import *
from common.privateFunctions import generateFolder, get_original_function_name, md5Collector
from io import StringIO
from copy import deepcopy
import sys
from importlib import import_module
from common.ICodec import *


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
                 target_folder: str = TEST_ITEMS,  # place everything into this dir
                 current_test_name: str = "current",  # test default name, like current
                 active=False,  # global on/off switch of the test dumper
                 # FIXME should be a (lambda) function based on criteria
                 # FIXME when ran by test_runner, active should be False all the time
                 generate_init_files: bool = False,  # generate init files, like WinMerge, typically for the first run
                 exceptions: list = [],
                 are_exceptions_included: bool = True,
                 hex_name_length: int = 12):                  # for default testcase filename generating
        self.bDump = active
        self.sMainTestFolder = target_folder
        self.sDefaultTest = current_test_name
        self.nNameHex = hex_name_length
        self.codec = codec
        self.bGenerateInitFiles = generate_init_files
        self.sModule: str
        self.sClass: str
        self.sFunction: str
        self.sTest: str
        self.sCaseFolder: str
        self.sErrorFolder: str
        self.collectedMD5S = set()
        self.bIncludeExceptions = are_exceptions_included
        self.lExceptions = exceptions if exceptions is not None else []
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

    # Misleading, this __call__ is called only once, at the beginning to create wrapped_function:
    def __call__(self, func, *args, **kwargs):
        if not self.__class__.bDump:
            return func
        self.sModule, self.sClass, self.sFunction = get_original_function_name(func)
        if self.sClass:
            self.sTest = ".".join([self.sModule, self.sClass, self.sFunction])
            self.sCaseFolder = os.path.join(self.sMainTestFolder, self.sModule, self.sClass, self.sFunction)
        else:
            self.sTest = ".".join([self.sModule, self.sFunction])
            self.sCaseFolder = os.path.join(self.sMainTestFolder, self.sModule, self.sFunction)
        self.sErrorFolder = self.sCaseFolder + ERROR_STR
        self.collectedMD5S.update(md5Collector(self.sCaseFolder))
        if self.bGenerateInitFiles:
            self._initFiles()

        functools.wraps(func)

        _mod = import_module(self.sModule)

        def wrapped_function(*argsWrap, **kwargsWrap):
            # MD5 is calculated from dPre
            self._args = copy.deepcopy(argsWrap)
            self._kwargs = copy.deepcopy(kwargsWrap)

            try:
                if isinstance(func, classmethod):
                    _class = getattr(_mod, self.sClass)
                    self._preClass = copy.deepcopy(_class)
                    self._result = func.__func__(_class, *argsWrap[1:], **kwargsWrap)
                    self._postClass = _class
                elif isinstance(func, staticmethod):
                    # self._args = argsWrap
                    self._result = func(*argsWrap[1:], **kwargsWrap)
                else:
                    if argsWrap and hasattr(argsWrap[0], '__dict__'):
                        # member method
                        self._preSelf = copy.deepcopy(argsWrap[0])
                        self._result = func(*[argsWrap[0], *argsWrap[1:]], **kwargsWrap)
                        self._postSelf = argsWrap[0]
                    else:
                        # standalone function
                        # self._args = argsWrap
                        self._result = func(*argsWrap, **kwargsWrap)
            except Exception as e:
                # FIXME Exception handling
                self._exception = e
                if (e.__class__ in self.lExceptions) == self.bIncludeExceptions:
                    self.bDump = True
                elif (e.__class__ == KeyboardInterrupt):
                    self.bDump = True
                raise
            finally:
                if self.bDump == True:
                    self.dump()
                elif isinstance(self.__class__.bDump, 'Callable'):
                    if self.bDump() == True:
                        # FIXME
                        self.dump()
            return self._result
        return wrapped_function

    def _initFiles(self):
        # FIXME WinMerge as only an option
        if not os.path.exists(sWinMergePath := os.path.join(self.sMainTestFolder, self.sTest + ".WinMerge")) \
                and not os.path.exists(self.sCaseFolder) \
                and not os.path.exists(self.sErrorFolder):
            generateFolder(self.sCaseFolder)

            import xml.etree.ElementTree as ET
            tree = ET.parse(StringIO(WINMERGE_TEMPLATE))
            root = tree.getroot()
            root.find('paths/left').text = os.path.relpath(self.sCaseFolder, self.sMainTestFolder)
            root.find('paths/right').text = os.path.relpath(self.sErrorFolder, self.sMainTestFolder)
            tree.write(sWinMergePath)

    def dump(self):
        _dPre = {
            MODULE_NAME: self.sModule,
            CLASS_NAME: self.sClass,
            FUNC_NAME: self.sFunction,
            ARGS: self._get_module(self._args),
            KWARGS: self._get_module(self._kwargs),
        }

        if self._postClass is not None:
            _class = self._postClass
        elif self._postSelf is not None:
            _class = self._postSelf.__class__
        else:
            _class = None

        # for k, v in _dPre.items():
        #     _dPre[k] = self._get_module(v)

        sHash = hashlib.md5(self.codec.dumps(_dPre, _class).encode("ansi")).hexdigest()[:self.nNameHex]

        if sHash in self.collectedMD5S and not self.bOverwrite:
            return

        dResult = {**_dPre,
                   MD5: sHash,
                   PRE: {},
                   POST: {}}

        dResult[POST][RESULT] = self._result
        dResult[POST][EXCEPTION] = self._exception
        dResult[PRE][SELF] = self._get_module(self._preSelf)
        dResult[PRE][CLASS] = self._get_module(self._preClass)
        # dResult[PRE][GLOBAL] = self._preGlobal
        dResult[POST][SELF] = self._get_module(self._postSelf)
        dResult[POST][CLASS] = self._get_module(self._postClass)
        # dResult[POST][GLOBAL] = self._postGlobal

        sFileName = "".join((sHash, self.codec.sExt))

        sOutput = self.codec.dumps(dResult, _class)

        if not os.path.exists(sFile := (os.path.join(self.sCaseFolder, sFileName))) or self.bOverwrite:
            with open_and_create_folders(sFile, "w") as f:
                f.write(sOutput)

        # Like current.json:
        dResult[NAME] = 'Current test'
        sOutput = self.codec.dumps(dResult, _class)
        # TODO to do this using ICodec:
        with open_and_create_folders(os.path.join(self.sMainTestFolder, self.sDefaultTest + self.codec.sExt), "w") as f:
            f.write(sOutput)

    def _get_module(self, obj:object):
        """
        Replaces '__main__' module to the actual module name of any object.
        :param obj: any object, preferably not a primitive type (having __dict__) and from the __main__ module
        :return: the object with the replaced module
        """
        if hasattr(obj, "__dict__") and hasattr(obj, "__module__"):
            if obj.__module__ == "__main__":
                _class = getattr(sys.modules[self.sModule], self.sClass)
                instance = _class.__new__(_class)
                instance.__dict__.update(obj.__dict__)
                for k, v in instance.__dict__.items():
                    instance.__dict__[k] = self._get_module(v)
                return instance
        return obj

