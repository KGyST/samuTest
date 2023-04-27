import jsonpickle
import os
import hashlib


class DumperBase:
    """
    Decorator functor to modify the tested functions
    """
    # FIXME global vars
    # FIXME multiple results
    #FIXME add first_run
    #FIXME WinMerge file generation
    
    def __init__(self, defaultName, testSuite=None, targetDir=".", isActive=False, nNameHex=12):
        self.targetDir = targetDir
        self.defaultName = defaultName
        self.isActive = isActive
        self.nNameHex = nNameHex

        if testSuite:
            if "targetDir" in testSuite.__dict__:
                self.targetDir = testSuite.targetDir
            if "testOnly" in testSuite.__dict__:
                self.testOnly = testSuite.testOnly
            if "isActive" in testSuite.__dict__:
                self.isActive = testSuite.isActive
            if "nNameHex" in testSuite.__dict__:
                self.nNameHex = testSuite.nNameHex

    def __call__(self, func, fExport, sExt, *args, **kwargs):
        def wrapped_function(*argsWrap, **kwargsWrap):
            res = None
            try:
                res = func(*argsWrap, **kwargsWrap)
                if self.isActive:
                    raise Exception
                return res
            except TypeError as e:
                pass
            except Exception as e:
                sXML = fExport({"args": argsWrap,
                                 "kwargs": kwargsWrap,
                                 "result": res,
                                 "function": None,
                                 "module": None,
                                },
                               # indent=2
                               )

                sHash = hashlib.md5(sXML.encode("ansi")).hexdigest()[:self.nNameHex]
                fileName = func.__name__ + "_" + sHash + sExt

                #FIXME folder existance check
                with open(os.path.join(self.targetDir, self.defaultName), "w") as f:
                    f.write(sXML)
                # if self.isActive:
                #     #FIXME constantly False from testRunner
                #     with open(os.path.join(self.targetDir, fileName), "w") as f:
                #         f.write(sXML)
                return res
        return wrapped_function


class JSONDumper(DumperBase):
    def __init__(self, *args, **kwargs):
        super(JSONDumper, self) .__init__("current.json", *args, **kwargs)

    def __call__(self, func, *args, **kwargs):
        return super(JSONDumper, self).__call__(func, jsonpickle.dumps, ".json", *args, **kwargs)

