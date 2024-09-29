from enum import Enum


class Level(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5

    def __str__(self):
        return self.name


class Logger:
    def log(self, level: Level, message: str):
        print(f"{level}: {message}")

    def debug(self, message: str):
        self.log(Level.DEBUG, message)

    def info(self, message: str):
        self.log(Level.INFO, message)

    def warning(self, message: str):
        self.log(Level.WARNING, message)

    def error(self, message: str):
        self.log(Level.ERROR, message)

    def fatal(self, message: str):
        self.log(Level.FATAL, message)

