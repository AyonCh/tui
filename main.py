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

    lineLen = len(content[pos[0]])
    for y in range(size.lines - 3):
        current = int(len(str(y + view + 1)))
        line = ""

        if len(content) > y + view:
            for x in range(len(content[y + view])):
                if x < size.columns - (signcolum + 4):

                    if pos[1] >= lineLen:
                        if [y + view, x] == [pos[0], lineLen - 1]:
                            line += settings["character"]
                        else:
                            line += content[y + view][x]
                    else:
                        if [y + view, x] == pos:
                            line += settings["character"]
                        else:
                            line += content[y + view][x]

            if line == "" and y + view == pos[0]:
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
        case "l":
            if len(msg) > 0 and msg[0] == ":":
                msg += "l"
            else:
                if pos[1] + 1 < lineLen:
                    pos[1] += 1
        case "h":
            if len(msg) > 0 and msg[0] == ":":
                msg += "j"
            else:
                if pos[1] > 0:
                    pos[1] -= 1
        case "0":
            if len(msg) > 0 and msg[0] == ":":
                msg += "0"
            else:
                pos[1] = 0

        case "$":
            if len(msg) > 0 and msg[0] == ":":
                msg += "$"
            else:
                pos[1] = lineLen

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
                    case "qa":
                        system("clear")
                        break
                    case _:
                        msg = "Command doesn't exist!!"
        case "\x7f":
            if len(msg) > 0 and msg[0] == ":":
                msg = msg[0:-1]

        case _:
            if len(msg) > 0 and msg[0] == ":":
                msg += inp
