import jsonpickle
import os
import hashlib


class DumperBase:
    def __init__(self):
        pass


class JSONDumper(DumperBase):
    '''
    Decorator functor to modify the tested functions
    '''
    #FIXME global vars
    #FIXME multiple results
    #FIXME Inheritance

    def __init__(self, testSuite=None, targetDir = ".", defaultName="current.json", isActive=False, nNameHex=8):
        super(DumperBase, self).__init__()
        self.targetDir = targetDir
        self.defaultName = defaultName
        self.isActive = isActive
        self.nNameHex = nNameHex


    def __call__(self, func, *args, **kwargs):
        def wrapped_function(*args, **kwargs):
            res = None
            try:
                res = func(*args, **kwargs)
                if self.isActive:
                    raise Exception

                return res
            except:
                sJSON = jsonpickle.dumps({"args": [*args], "kwargs": kwargs, "result": res}, indent=2)
                sHash = hashlib.md5(sJSON.encode("ansi")).hexdigest()[:self.nNameHex]
                fileName = func.__name__  + "_" + sHash + ".json"

                with open(os.path.join(self.targetDir, self.defaultName), "w") as f:
                    f.write(sJSON)

                if self.isActive:
                    with open(os.path.join(self.targetDir, fileName), "w") as f:
                        f.write(sJSON)
                return res
        return wrapped_function
