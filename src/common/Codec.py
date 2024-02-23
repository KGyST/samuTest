from common.privateFunctions import open_and_create_folders
import jsonpickle
from abc import ABC, abstractmethod


class Codec(ABC):
    sExt:str
    class StorageException(Exception):
        pass

    @staticmethod
    @abstractmethod
    def read(path:str)->dict:
        pass

    @staticmethod
    @abstractmethod
    def reads(data:str)->dict:
        pass

    @staticmethod
    @abstractmethod
    def dumps(data: dict):
        pass

    @staticmethod
    @abstractmethod
    def dump(path:str, data:dict):
        pass

class JSONCodec(Codec):
    sExt = ".json"

    @staticmethod
    def read(path:str)->dict:
        with open(path, "r") as jf:
            try:
                return jsonpickle.loads(jf.read())
            except Exception:
                raise JSONCodec.StorageException()

    @staticmethod
    def reads(data:str)->dict:
        return jsonpickle.loads(data)

    @staticmethod
    def dumps(data: dict):
        return jsonpickle.dumps(data, indent=4, make_refs=False, include_properties=True)

    @staticmethod
    def dump(path:str, data:dict):
        with open_and_create_folders(path, "w") as fOutput:
            fOutput.write(JSONCodec.dumps(data))



