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

settings = {"cursorcolor": "black", "scrolloff": 10}

colors = {
    "black": ["\033[40m", "\033[37m"],
    "red": ["\033[41m", "\033[32m"],
    "green": ["\033[42m", "\033[31m"],
    "yellow": ["\033[43m", "\033[34m"],
    "blue": ["\033[44m", "\033[33m"],
    "magenta": ["\033[45m", "\033[36m"],
    "cyan": ["\033[46m", "\033[35m"],
    "white": ["\033[47m", "\033[30m"],
    "RESET": "\033[0m",
}

mode = "normal"


def getch():
    global msg
    return _getch()


def color(text):
    return f"""{colors[settings["cursorcolor"]][1]}{colors[settings["cursorcolor"]][0]}{text}{colors["RESET"]}"""


def clear():
    if platform.system() == "Windows":
        system("cls")
    else:
        system("clear")


size = get_terminal_size()
args = argv
name = ""
content = [""]
viewY = 0
viewX = 0

if len(args) < 2:
    name = "[unamed]"
else:
    name = args[1]
    with open(name) as data:
        content = data.read().splitlines()
signcolum = len(str(len(content)))

resetTimer = 0
while True:
    screen = ["\n", "-" * size.columns]
    if pos[0] == size.lines - 2 + viewY - settings["scrolloff"]:
        viewY += 1
    if pos[0] == viewY - 2 + settings["scrolloff"]:
        if viewY > 0:
            viewY -= 1
    if pos[1] == size.columns - (signcolum + 4) + viewX:
        viewX += 1
    if pos[1] == viewX:
        if viewX > 0:
            viewX -= 1

    lineLen = len(content[pos[0]])
    for y in range(size.lines - 3):
        currentY = int(len(str(y + viewY + 1)))
        line = ""

        if len(content) > y + viewY:
            for x in range(len(content[y + viewY])):
                currentX = int(len(str(x + viewX)))
                if x < size.columns - (signcolum + 4):
                    if pos[1] >= lineLen:
                        if mode == "normal":
                            if [y + viewY, x + viewX] == [pos[0], lineLen - 1]:
                                line += color(content[y + viewY][x + viewX])
                            else:
                                if len(content[y + viewY]) > x + viewX:
                                    line += content[y + viewY][x + viewX]
                        elif mode == "insert":
                            if [y + viewY, x + viewX + 1] == [pos[0], lineLen]:
                                line += content[y + viewY][x + viewX]
                                line += color(" ")
                            else:
                                if len(content[y + viewY]) > x + viewX:
                                    line += content[y + viewY][x + viewX]
                    else:
                        if [y + viewY, x + viewX] == pos:
                            line += color(content[y + viewY][x + viewX])
                        else:
                            if len(content[y + viewY]) > x + viewX:
                                line += content[y + viewY][x + viewX]

            if line == "" and y + viewY == pos[0]:
                line += color(" ")

            screen.append(f"{y + viewY + 1}{' '*(signcolum-currentY)} | {line}")
        else:
            screen.append("")

    screen.append(
        f"- {mode.upper()} - {name} {'-'*(size.columns - 6 - len(name) - len(mode))}"
    )

    screen.append(msg)
    if len(msg) > 0 and msg[0] != ":":
        resetTimer += 1
    if resetTimer == 10:
        msg = ""
        resetTimer = 0

    print("\n".join(screen), end="")
    inp = getch()

    if mode == "normal":
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
                    viewX = 0

            case "$":
                if len(msg) > 0 and msg[0] == ":":
                    msg += "$"
                else:
                    pos[1] = lineLen
                    if lineLen > size.columns:
                        viewX = lineLen - (size.columns - (signcolum + 4)) // 2

            case "i":
                if len(msg) > 0 and msg[0] == ":":
                    msg += "i"
                else:
                    mode = "insert"
            case "a":
                if len(msg) > 0 and msg[0] == ":":
                    msg += "a"
                else:
                    mode = "insert"
                    pos[1] += 1
            case ":":
                if (len(msg) > 0 and msg[0] != ":") or msg == "":
                    msg = ":"
            case "\r":
                if len(msg) > 0 and msg[0] == ":":
                    commands = msg.strip().split(":")
                    match commands[1]:
                        case "q":
                            clear()
                            break
                        case "qa":
                            clear()
                            break
                        case "w" | "wq" | "wqa":
                            if len(commands) > 2:
                                with open(commands[2], "w") as data:
                                    data.write("\n".join(content))
                                msg = ""
                            else:
                                with open(name, "w") as data:
                                    data.write("\n".join(content))
                                msg = ""
                            if commands[1] == "wq" or commands[1] == "wqa":
                                clear()
                                break
                        case _:
                            msg = "Command doesn't exist!!"
            case "\x7f":
                if len(msg) > 0 and msg[0] == ":":
                    msg = msg[0:-1]
            case "\x03":
                msg = "Use :q to exit"
            case _:
                if len(msg) > 0 and msg[0] == ":":
                    msg += inp
    elif mode == "insert":
        match inp:
            case "\x03" | "\x1b":
                mode = "normal"
            case "\r":
                buf = content[pos[0]]
                before = buf[: pos[1]]
                after = buf[pos[1] :]
                content[pos[0]] = before
                content.insert(pos[0] + 1, after)
                pos[0] += 1
                pos[1] = 0
            case "\x7f":
                buf = content[pos[0]]
                before = buf[: pos[1]][0:-1]
                after = buf[pos[1] :]
                if len(before) == 0:
                    if pos[0] - 1 < len(content):
                        lastLineLen = len(content[pos[0] - 1]) + 1
                    else:
                        lastLineLen = 0
                    if pos[0] - 1 < len(content):
                        content.pop(pos[0])
                        content[pos[0] - 1] += after
                    else:
                        content.pop(-1)
                    if pos[0] > 0:
                        pos[0] -= 1
                        pos[1] = lastLineLen
                else:
                    content[pos[0]] = before + after
                if pos[1] > 0:
                    pos[1] -= 1
            case _:
                buf = content[pos[0]]
                before = buf[: pos[1]]
                after = buf[pos[1] :]
                content[pos[0]] = before + inp + after
                pos[1] += 1
