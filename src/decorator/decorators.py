import jsonpickle
import os
import hashlib
from common.constants import ERROR_STR, WINMERGE_TEMPLATE
from common.privateFunctions import generateFolder
from io import StringIO

class DumperBase:
    """
    Decorator functor to modify the tested functions
    Reason for having a Base class is for potentially being able to inher into an xml or yaml writer
    """
    #FIXME add first_run -> generate_files
    # FIXME multiple results
    # FIXME global vars handling
    #FIXME mocked functions
    #FIXME isActive: writing out the last tested function all the time including testset for an easy rerun

    class DumperException(Exception):
        #FIXME doesn't work
        pass

    #FIXME devise actual function name test_func_name, first param
    def __init__(self,
                 test_func_name,
                 testExt,  #test default name, like .json
                 fExport,
                 currentTestName = "current",  #test default name, like current
                 target_folder=".",  #place everything into this dir
                 active=True,           #to switch on/off the test
                 generate_files=True,   #generate files, typically for the first run
                 nNameHex=12):          #for default testcase filename generating
        self.sTargetFolder = target_folder
        self.sDefaultTest = currentTestName
        self.sTest = test_func_name
        self.isActive = active
        self.nNameHex = nNameHex
        self.sExt = testExt
        self.fExport = fExport

        self.sFolder = os.path.join(self.sTargetFolder, self.sTest)
        generateFolder(self.sFolder + ERROR_STR, p_bForceDelete=True)

        if generate_files:
            self._initFiles()

    def _initFiles(self):
        import xml.etree.ElementTree as ET
        tree = ET.parse(StringIO(WINMERGE_TEMPLATE))
        root = tree.getroot()
        root.find('paths/left').text = os.path.join(os.getcwd(), self.sTargetFolder, self.sTest)
        root.find('paths/right').text = os.path.join(os.getcwd(), self.sTargetFolder, self.sTest + ERROR_STR)
        tree.write(os.path.join(self.sTargetFolder, self.sTest + ".WinMerge"))

        generateFolder(self.sFolder)

    def __call__(self, func, *args, **kwargs):
        def wrapped_function(*argsWrap, **kwargsWrap):
            fResult = None
            try:
                fResult = func(*argsWrap, **kwargsWrap)
                if self.isActive:
                    raise DumperException()
                return fResult
            except TypeError as e:
                pass
            #FIXME custom Exception class
            except Exception as e:
                sOutput = self.fExport({"args": argsWrap,
                                 "kwargs": kwargsWrap,
                                 "result": fResult,
                                 "function": None,
                                 "module": None,
                                },
                               )

                sHash = hashlib.md5(sOutput.encode("ansi")).hexdigest()[:self.nNameHex]
                fileName = func.__name__ + "_" + sHash + self.sExt

                #FIXME folder existance check
                #Like current.json:
                with open(os.path.join(self.sFolder, self.sDefaultTest + self.sExt), "w") as f:
                    f.write(sOutput)
                if self.isActive:
                    with open(os.path.join(self.sFolder, fileName), "w") as f:
                        f.write(sOutput)
                return fResult
        return wrapped_function


class JSONDumper(DumperBase):
    def __init__(self, test_name, *args, **kwargs):
        super(JSONDumper, self) .__init__(test_name, ".json", jsonpickle.dumps, *args, **kwargs)

    def __call__(self, func, *args, **kwargs):
        return super(JSONDumper, self).__call__(func, *args, **kwargs)

