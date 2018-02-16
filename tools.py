
from enum import Enum

class PrintOutput(Enum):
    OK = 0
    DEBUG = 1
    WARNING = 2
    ERROR = 3

class OsType(Enum):
    LINUX = 0
    OSX = 1
    WIN = 2

class LastAction(Enum):
    START = 0
    EXPLORE = 1
    SEARCH = 2

class InfoPrinter():
    w = "\033[0m"  # white (normal)
    r = "\033[31m"  # red
    g = "\033[32m"  # green
    o = "\033[33m"  # orange
    b = "\033[34m"  # blue
    p = "\033[35m"  # purple

    @staticmethod
    def out(type, text):
        # fatal error
        if (type == PrintOutput.ERROR):
            print('[{}  Error{}] - '.format(InfoPrinter.r, InfoPrinter.w), end="")
            print(text)
            exit()
        # task ok
        elif (type == PrintOutput.OK):
            print('[{}     Ok{}] - '.format(InfoPrinter.g, InfoPrinter.w), end="")
            print(text)
        # ignorable error
        elif (type == PrintOutput.WARNING):
            print('[{}Warning{}] - '.format(InfoPrinter.o, InfoPrinter.w), end="")
            print(text)
        # debug info
        elif (type == PrintOutput.DEBUG):
            print('[{}  Debug{}] - '.format(InfoPrinter.b, InfoPrinter.w), end="")
            print(text)
        # nothing
        else:
            InfoPrinter.out(PrintOutput.ERROR, "Bad \"col\" function call")

    @staticmethod
    def input(text):
        print('[{}  Input{}] - '.format(InfoPrinter.p, InfoPrinter.w), end="")
        print(text + ": ", end="")

        try:
            return input()
        except:
            print()
            InfoPrinter.out(PrintOutput.ERROR, "Keyboard Interrupt")
            exit()
