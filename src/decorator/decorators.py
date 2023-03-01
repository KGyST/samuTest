import jsonpickle
import os
import hashlib


class JSONDumper():
    """
    Decorator functor to modify the tested functions
    """
    # FIXME global vars
    # FIXME multiple results
    # FIXME Inheritance

    def __init__(self, testSuite=None, targetDir=".", defaultName="current.json", isActive=False, nNameHex=8):
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

    def __call__(self, func, *args, **kwargs):
        def wrapped_function(*argsWrap, **kwargsWrap):
            res = None
            try:
                res = func(*argsWrap, **kwargsWrap)
                if self.isActive:
                    raise Exception

                return res
            except:
                sJSON = jsonpickle.dumps({"args": [*argsWrap], "kwargs": kwargsWrap, "result": res}, indent=2)
                sHash = hashlib.md5(sJSON.encode("ansi")).hexdigest()[:self.nNameHex]
                fileName = func.__name__ + "_" + sHash + ".json"

                with open(os.path.join(self.targetDir + "_suites", self.defaultName), "w") as f:
                    f.write(sJSON)

                if self.isActive:
                    with open(os.path.join(self.targetDir + "_suites", fileName), "w") as f:
                        f.write(sJSON)
                return res
        return wrapped_function
