from common.ICodec import ICodec
import hashlib


class ProgramState:
    nNameHex = None
    codec = None

    def __init__(self, codec: "ICodec", hex_name_length: int = 12):
        self.__class__.codec = codec
        self.__class__.nNameHex = hex_name_length

        self.preState = None
        self.postState = None
        self.module = None
        self.className = None
        self.function = None
        self.args = None
        self.kwargs = None
        self._sMD5 = None

    @property
    def md5(self):
        if self._sMD5:
            self._sMD5 = hashlib.md5(self.__class__.codec.dumps(self.preState).encode("ansi")).hexdigest()[:self.__class__.nNameHex]
        return self._sMD5


class StateBase:
    def __init__(self):
        self.selfOrClass = None

    def __eq__(self, other: "StateBase"):
        ...


class PreState(StateBase):
    def __init__(self):
        super().__init__()


class PostState(StateBase):
    def __init__(self):
        super().__init__()
        self.result = None
        self.exception = None

