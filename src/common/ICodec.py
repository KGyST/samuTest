from common.privateFunctions import open_and_create_folders
import jsonpickle
from abc import ABC, abstractmethod

class ICodec(ABC):
    sExt: str

    class StorageException(Exception):
        pass

    @staticmethod
    @abstractmethod
    def read(path: str) -> dict:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def reads(data: str) -> dict:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def dumps(data: dict, class_):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def dump(path: str, data: dict):
        raise NotImplementedError()


class JSONCodec(ICodec):
    sExt = ".json"

    @staticmethod
    def read(path: str) -> dict:
        with open(path, "r") as jf:
            try:
                return jsonpickle.loads(jf.read())
            except Exception:
                raise JSONCodec.StorageException()

    @staticmethod
    def reads(data: str) -> dict:
        return jsonpickle.loads(data)

    @staticmethod
    def dumps(data: dict, class_) -> str:
        # data = JSONCodec._remove_undumpable(data)

        return jsonpickle.dumps(data, indent=4, make_refs=False, include_properties=False)

    @staticmethod
    def dump(path: str, data: dict):
        with open_and_create_folders(path, "w") as fOutput:
            fOutput.write(JSONCodec.dumps(data))

    @staticmethod
    def _remove_undumpable(data):
        _stuff_to_remove = []

        if isinstance(data, dict):
            for k, v in data.items():
                try:
                    _a = jsonpickle.dumps(v)
                except:
                    try:
                        data[k] = JSONCodec._remove_undumpable(v)
                    except:
                        _stuff_to_remove.append(k)
            for k in _stuff_to_remove:
                del data[k]
        elif isinstance(data, list):
            for v in data:
                try:
                    _a = jsonpickle.dumps(v)
                except:
                    try:
                        data[v] = JSONCodec._remove_undumpable(v)
                    except:
                        _stuff_to_remove.append(v)
            for k in _stuff_to_remove:
                data.remove(k)
        elif hasattr(data, '__dict__'):
            for k, v in data.__dict__.items():
                try:
                    if callable(v):
                        _stuff_to_remove.append(k)
                    else:
                        _a = jsonpickle.dumps(v)
                except:
                    try:
                        data.__dict__[k] = JSONCodec._remove_undumpable(v)
                    except:
                        _stuff_to_remove.append(k)
            for k in _stuff_to_remove:
                del data.__dict__[k]
        else:
            _a = jsonpickle.dumps(data)
        return data
