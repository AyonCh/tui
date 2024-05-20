from os import get_terminal_size, system
from sys import argv
import platform

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


msg = ""
pos = [0, 0]

settings = {"character": "|", "scrolloff": 10}


def getch():
    global msg
    ch = _getch()
    if ch.encode() == b"\x03":
        msg = "Use :q to exit"
    if ch.encode() == b"\x1a":
        sys.exit(0)
    return ch


size = get_terminal_size()
args = argv
name = ""
content = [""]
view = 0

signcolum = int(len(str(size.lines)))
if len(args) < 2:
    name = "[unamed]"
else:
    name = args[1]
    with open(name) as data:
        content = data.read().splitlines()

resetTimer = 0
while True:
    screen = ["-" * size.columns]
    if pos[0] == size.lines - 2 + view - settings["scrolloff"]:
        view += 1
    if pos[0] == view - 2 + settings["scrolloff"]:
        if view > 0:
            view -= 1

    for y in range(size.lines - 3):
        current = int(len(str(y + view + 1)))
        line = ""

        if len(content) > y + view:
            for x in range(len(content[y + view])):
                if x < size.columns - (signcolum + 4):

                    if [y + view, x] == pos:
                        line += settings["character"]
                    else:
                        line += content[y + view][x]

            if line == "" and [y + view, 0] == pos:
                line += settings["character"]

            screen.append(f"{y + view + 1}{' '*(signcolum-current+1)} | {line}")
        else:
            screen.append("")
    if msg:
        screen.append(msg)
        if len(msg) > 0 and msg[0] != ":":
            resetTimer += 1
        if resetTimer == 10:
            msg = ""
            resetTimer = 0
    else:
        screen.append(f"- {name} {'-'*(size.columns - 3 - len(name))}")

    print("\n".join(screen))
    inp = getch()
    match inp:
        case "j":
            if len(msg) > 0 and msg[0] == ":":
                msg += "j"
            else:
                if pos[0] + 1 < len(content):
                    pos[0] += 1
        case "k":
            if len(msg) > 0 and msg[0] == ":":
                msg += "k"
            else:
                if pos[0] > 0:
                    pos[0] -= 1

        case ":":
            if (len(msg) > 0 and msg[0] != ":") or msg == "":
                msg = ":"
        case "\r":
            if len(msg) > 0 and msg[0] == ":":
                commands = msg.strip().split(":")
                match commands[1]:
                    case "q":
                        system("clear")
                        break
                    case _:
                        msg = "Command doesn't exist!!"
        case _:
            if len(msg) > 0 and msg[0] == ":":
                msg += inp
