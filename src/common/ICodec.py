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
    def dumps(data) -> str:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def dump(path: str, data):
        raise NotImplementedError()

