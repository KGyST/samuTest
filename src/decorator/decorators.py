import functools

import hashlib
from common.constants import *
from common.privateFunctions import generateFolder, get_original_function_name, md5Collector
from io import StringIO
from copy import deepcopy
import sys
from importlib import import_module
from common.Codec import *


class Dumper:
    """
    Decorator functor to modify the tested functions
    """

    # FIXME mocked functions
    # FIXME global vars handling
    bDump = False

    class DumperException(Exception):
        pass

    def __init__(self,
                 codec:'Codec' = JSONCodec,
                 target_folder: str=TEST_ITEMS,  # place everything into this dir
                 current_test_name: str ="current",  # test default name, like current
                 active: bool=False,  # global on/off switch of the test dumper
                 generate_init_files: bool=True,  # generate init files, like WinMerge, typically for the first run
                 exceptions: list[Exception] = None,
                 are_exceptions_included:bool=True,
                 nNameHex: int=12):                  # for default testcase filename generating
        self.__class__.bDump = active
        self.sMainTestFolder = target_folder
        self.sDefaultTest = current_test_name
        self.nNameHex = nNameHex
        self.codec = codec
        self.bGenerateInitFiles = generate_init_files
        self.sModule:str
        self.sClass:str
        self.sFunction:str
        self.sTest:str
        self.sCaseFolder:str
        self.sErrorFolder:str
        self.md5S = set()
        self.bIncludeExceptions = are_exceptions_included
        self.lExceptions = exceptions if exceptions is not None else []

    # Very much misleading, this __call__ is called only once, at the beginning to create wrapped_function:
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
        self.md5S.update(md5Collector(self.sCaseFolder))
        if self.bGenerateInitFiles:
            self._initFiles()

        functools.wraps(func)

        dPre = ({
            MODULE_NAME: self.sModule,
            CLASS_NAME: self.sClass,
            FUNC_NAME: self.sFunction,
        })
        dPost = {}

        _mod = import_module(self.sModule)
        def wrapped_function(*argsWrap, **kwargsWrap):
            if argsWrap and hasattr(argsWrap[0], '__dict__') and self.sFunction != '__new__':
                instance = argsWrap[0]
                argsWrap = argsWrap[1:]
                instance_pre = deepcopy(instance)
                dPre.update({INST_PRE: instance_pre})
            else:
                instance = None
                instance_pre = None

            dPre.update({ARGS: argsWrap,
                         KWARGS: kwargsWrap,
                         })
            try:
                if isinstance(func, classmethod):
                    _class = getattr(_mod, self.sClass)
                    fResult = func.__func__(_class, *argsWrap[1:], **kwargsWrap)
                elif isinstance(func, staticmethod):
                    fResult = func(*argsWrap[1:], **kwargsWrap)
                else:
                    if instance_pre:
                        # member method
                        fResult = func(instance, *argsWrap, **kwargsWrap)
                        argsWrap = (instance_pre, *argsWrap)
                    else:
                        # standalone function
                        fResult = func(*argsWrap, **kwargsWrap)
                dPost.update({RESULT: fResult,
                              INST_POST: instance, })
            except Exception as e:
                # FIXME Exception handling
                if (e.__class__ in self.lExceptions) == self.bIncludeExceptions:
                    dPost.update({EXCEPTION: e,})
                raise
            finally:
                self.dump(dPre, dPost)
            return fResult
        return wrapped_function

    def _initFiles(self):
        # FIXME WinMerge as an option
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

    def dump(self, pre:dict, post: dict):
        sHash = hashlib.md5(self.codec.dumps(pre).encode("ansi")).hexdigest()[:self.nNameHex]
        if sHash in self.md5S:
            return

        sFileName = "".join((sHash, self.codec.sExt))
        post[MD5] = sHash
        pre.update(post)
        for k, v in pre.items():
            pre[k] = self._get_module(v)
        sOutput = self.codec.dumps(pre)

        if not os.path.exists(sFile:=(os.path.join(self.sCaseFolder, sFileName))):
            with open_and_create_folders(sFile, "w") as f:
                f.write(sOutput)

        # Like current.json:
        pre[NAME] = 'Current test'
        sOutput = self.codec.dumps(pre)
        with open_and_create_folders(os.path.join(self.sMainTestFolder, self.sDefaultTest + self.codec.sExt), "w") as f:
            f.write(sOutput)

    def _get_module(self, obj:object):
        """
        Replaces '__main__' module to the actual module name of any object.
        :param obj: any object, preferably not a primitive type (having __dict__) and from the __main__ module
        :return: the object with the replaced module
        """
        if hasattr(obj, "__dict__"):
            if obj.__module__ == "__main__":
                _class = getattr(sys.modules[self.sModule], self.sClass)
                instance = _class.__new__(_class)
                instance.__dict__ = obj.__dict__
                for k, v in instance.__dict__.items():
                    instance.__dict__[k] = self._get_module(v)
                return instance
        return obj

