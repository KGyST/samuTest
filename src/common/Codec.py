from common.privateFunctions import open_and_create_folders
import jsonpickle

class JSONCodec:
    ext = ".json"

    class StorageException(Exception):
        pass

    @staticmethod
    def read(path:str)->dict:
        with open(path, "r") as jf:
            try:
                return jsonpickle.loads(jf.read())
            except Exception:
                raise JSONCodec.StorageException()

    @staticmethod
    def dump(path:str, data:dict):
        with open_and_create_folders(path, "w") as fOutput:
            fOutput.write(jsonpickle.dumps(data, indent=4, make_refs=False, include_properties=True))

