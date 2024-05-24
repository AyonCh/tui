import platform
from os import system

colors = {
    "background_black": "\033[40m",
    "background_red": "\033[41m",
    "background_green": "\033[42m",
    "background_yellow": "\033[43m",
    "background_blue": "\033[44m",
    "background_magenta": "\033[45m",
    "background_cyan": "\033[46m",
    "background_white": "\033[47m",
    "forground_black": "\033[30m",
    "forground_red": "\033[31m",
    "forground_green": "\033[32m",
    "forground_yellow": "\033[33m",
    "forground_blue": "\033[34m",
    "forground_magenta": "\033[35m",
    "forground_cyan": "\033[36m",
    "forground_white": "\033[37m",
    "RESET": "\033[0m",
}

if platform.system() == "Windows":
    import msvcrt
    import sys

    def _getch():
        return msvcrt.getwch()

else:
    import tty
    import termios
    import sys

    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def getch():
    global msg
    return _getch()


def color(text, forground="", background=""):
    return f"""{forground}{background}{text}\033[0m"""


def clear():
    if platform.system() == "Windows":
        system("cls")
    else:
        system("clear")
