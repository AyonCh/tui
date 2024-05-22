from os import get_terminal_size, system, listdir
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

mode = "normal"
screen = "editor"


def getch():
    global msg
    return _getch()


def color(text, forground="", background=""):
    return f"""{forground}{background}{text}{colors["RESET"]}"""


def clear():
    if platform.system() == "Windows":
        system("cls")
    else:
        system("clear")


size = get_terminal_size()
args = argv
name = ""
content = [""]
originalContent = [""]
exploreContent = [""]
dir = listdir()
if len(args) < 2:
    name = "[unamed]"
else:
    name = args[1]
    with open(name) as data:
        content = data.read().splitlines()
        originalContent = list(content)
signcolumn = len(str(len(content)))
signcolumnDir = len(str(len(dir)))

resetTimer = 0

viewY = 0
viewX = 0


def editorScreen(msg, lineLen):
    screen = ["\n", color("-" * size.columns, forground=colors["forground_black"])]

    for y in range(size.lines - 3):
        currentY = int(len(str(y + viewY + 1)))
        line = ""

        if len(content) > y + viewY:
            for x in range(len(content[y + viewY])):
                if x < size.columns - (signcolumn + 4):
                    if pos[1] >= lineLen:
                        if mode == "normal":
                            if [y + viewY, x + viewX] == [pos[0], lineLen - 1]:
                                line += color(
                                    content[y + viewY][x + viewX],
                                    forground=colors["forground_white"],
                                    background=colors["background_black"],
                                )
                            else:
                                if len(content[y + viewY]) > x + viewX:
                                    line += content[y + viewY][x + viewX]
                        elif mode == "insert":
                            if [y + viewY, x + viewX + 1] == [pos[0], lineLen]:
                                line += content[y + viewY][x + viewX]
                                line += color(
                                    " ",
                                    forground=colors["forground_white"],
                                    background=colors["background_black"],
                                )
                            else:
                                if len(content[y + viewY]) > x + viewX:
                                    line += content[y + viewY][x + viewX]
                    else:
                        if [y + viewY, x + viewX] == pos:
                            line += color(
                                content[y + viewY][x + viewX],
                                forground=colors["forground_white"],
                                background=colors["background_black"],
                            )
                        else:
                            if len(content[y + viewY]) > x + viewX:
                                line += content[y + viewY][x + viewX]

            if line == "" and y + viewY == pos[0]:
                line += color(
                    " ",
                    forground=colors["forground_white"],
                    background=colors["background_black"],
                )

            screen.append(
                f"{color(y + viewY + 1, forground=colors['forground_black'])}{' '*(signcolumn-currentY)} {color('|', forground=colors['forground_black'])} {line}"
            )
        else:
            screen.append("")

    if originalContent == content:
        screen.append(
            f"{color('-', forground=colors['forground_black'])} {mode.upper()} {color('-', forground=colors['forground_black'])} {name} {color('-'*(size.columns - 6 - len(name) - len(mode)), forground=colors['forground_black'])}"
        )
    else:
        screen.append(
            f"{color('-', forground=colors['forground_black'])} {mode.upper()} {color('-', forground=colors['forground_black'])} {name} [+] {color('-'*(size.columns - 10 - len(name) - len(mode)), forground=colors['forground_black'])}"
        )

    screen.append(msg)

    print("\n".join(screen), end="")


def exploreScreen(msg, lineLen):
    screen = ["\n", color("-" * size.columns, forground=colors["forground_black"])]
    for y in range(size.lines - 3):
        line = ""

        if len(dir) > y + viewY:
            for x in range(len(dir[y + viewY])):
                if x < size.columns - (signcolumnDir + 4):
                    if pos[1] >= lineLen:
                        if mode == "normal":
                            if [y + viewY, x + viewX] == [pos[0], lineLen - 1]:
                                line += color(
                                    dir[y + viewY][x + viewX],
                                    forground=colors["forground_white"],
                                    background=colors["background_black"],
                                )
                            else:
                                if len(dir[y + viewY]) > x + viewX:
                                    line += dir[y + viewY][x + viewX]
                        elif mode == "insert":
                            if [y + viewY, x + viewX + 1] == [pos[0], lineLen]:
                                line += dir[y + viewY][x + viewX]
                                line += color(
                                    " ",
                                    forground=colors["forground_white"],
                                    background=colors["background_black"],
                                )
                            else:
                                if len(dir[y + viewY]) > x + viewX:
                                    line += dir[y + viewY][x + viewX]
                    else:
                        if [y + viewY, x + viewX] == pos:
                            line += color(
                                dir[y + viewY][x + viewX],
                                forground=colors["forground_white"],
                                background=colors["background_black"],
                            )
                        else:
                            if len(dir[y + viewY]) > x + viewX:
                                line += dir[y + viewY][x + viewX]

            if line == "" and y + viewY == pos[0]:
                line += color(
                    " ",
                    forground=colors["forground_white"],
                    background=colors["background_black"],
                )

            screen.append(f"{' '*signcolumnDir}{line}")
        else:
            screen.append("")

    screen.append(
        f"{color('-', forground=colors['forground_black'])} {mode.upper()} {color('-', forground=colors['forground_black'])} Explore {color('-'*(size.columns - 13 - len(mode)), forground=colors['forground_black'])}"
    )
    screen.append(msg)
    print("\n".join(screen), end="")


while True:
    lineLen = 0
    if pos[0] == size.lines - 2 + viewY - settings["scrolloff"]:
        viewY += 1
    if pos[0] == viewY - 2 + settings["scrolloff"]:
        if viewY > 0:
            viewY -= 1
    if pos[1] == size.columns - (signcolumn + 4) + viewX:
        viewX += 1
    if pos[1] == viewX:
        if viewX > 0:
            viewX -= 1

    if screen == "editor":
        lineLen = len(content[pos[0]])
        editorScreen(msg, lineLen)
    elif screen == "explore":
        lineLen = len(dir[pos[0]])
        exploreScreen(msg, lineLen)

    if len(msg) > 0 and msg[0] != ":":
        resetTimer += 1
    if resetTimer == 10:
        msg = ""
        resetTimer = 0

    inp = getch()

    if mode == "normal":
        match inp:
            case "j":
                if pos[0] + 1 < len(content):
                    pos[0] += 1
            case "k":
                if pos[0] > 0:
                    pos[0] -= 1
            case "l":
                if pos[1] + 1 < lineLen:
                    pos[1] += 1
            case "h":
                if pos[1] > 0:
                    pos[1] -= 1
            case "0":
                pos[1] = 0
                viewX = 0
            case "$":
                pos[1] = lineLen
                if lineLen > size.columns:
                    viewX = lineLen - (size.columns - (signcolumn + 4)) // 2
            case "i":
                mode = "insert"
            case "a":
                mode = "insert"
                pos[1] += 1
            case ":":
                mode = "command"
                msg = ":"
            case "\x03":
                msg = "Use :q to exit"
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
                before = buf[: pos[1]]
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
                    content[pos[0]] = before[0:-1] + after
                if pos[1] > 0:
                    pos[1] -= 1
            case _:
                buf = content[pos[0]]
                before = buf[: pos[1]]
                after = buf[pos[1] :]
                content[pos[0]] = before + inp + after
                pos[1] += 1
    elif mode == "command":
        match inp:
            case "\r":
                commands = (msg.strip().split(":"))[1].split(" ")
                match commands[0]:
                    case "q" | "q!":
                        if commands[0] == "q":
                            if originalContent == content:
                                clear()
                                break
                            else:
                                msg = "Unsaved changes, pls save before exiting"
                        else:
                            clear()
                            break
                    case "qa" | "qa!":
                        if commands[0] == "qa":
                            if originalContent == content:
                                clear()
                                break
                            else:
                                msg = "Unsaved changes, pls save before exiting"
                        else:
                            clear()
                            break
                    case "w" | "wq" | "wqa" | "wq!" | "wqa!":
                        if len(commands) > 1:
                            with open(commands[1], "w") as data:
                                data.write("\n".join(content))
                        else:
                            with open(name, "w") as data:
                                data.write("\n".join(content))
                        originalContent = list(content)
                        msg = ""
                        if commands[0] == "wq" or commands[0] == "wqa":
                            if originalContent == content:
                                clear()
                                break
                            else:
                                msg = "Unsaved changes, pls save before exiting"
                        if commands[0] == "wq!" or commands[0] == "wqa!":
                            clear()
                            break
                    case "Explore" | "Ex":
                        screen = "explore"
                        msg = ""
                    case _:
                        msg = "Command doesn't exist!!"
                mode = "normal"
            case "\x7f":
                msg = msg[0:-1]
                if msg == "":
                    mode = "normal"
            case "\x03" | "\x1b":
                mode = "normal"
                msg = ""
            case _:
                msg += inp
