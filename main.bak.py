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
    ch = _getch()
    if ch.encode() == b"\x03":
        msg = "Use :q to exit"
    if ch.encode() == b"\x1a":
        sys.exit(0)
    return ch


print(getch())
