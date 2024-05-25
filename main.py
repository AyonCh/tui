from os import (
    get_terminal_size,
    listdir,
    path,
    mkdir,
    remove,
    rename,
    chdir,
    getcwd,
)
from shutil import rmtree
from sys import argv
from display import Display
from utility import color, getch, clear, colors

msgs = ["testing", "multiline", "msg"]
settings = {"cursorcolor": "black", "scrolloff": 10, "tabwidth": 4}

size = get_terminal_size()
args = argv

buffers = []
currentBuffer = 0

if len(args) < 2:
    buffers.append(
        {
            "name": "[unamed]",
            "content": [""],
            "originalContent": [""],
            "viewY": 0,
            "viewX": 0,
            "pos": [0, 0],
            "mode": "normal",
            "modifiable": True,
        }
    )
else:
    with open(args[1]) as data:
        content = data.read().splitlines()
        buffers.append(
            {
                "name": args[1],
                "content": content if content else [""],
                "originalContent": list(content) if content else [""],
                "viewY": 0,
                "viewX": 0,
                "pos": [0, 0],
                "mode": "normal",
                "modifiable": True,
            }
        )


resetTimer = 0

inp = ""

while buffers:
    bufData = buffers[currentBuffer]

    signcolumn = len(str(len(bufData["content"])))

    try:
        lineLen = int(len(bufData["content"][bufData["pos"][0]]))
    except:
        lineLen = 0

    if bufData["pos"][0] == size.lines - 2 + bufData["viewY"] - settings["scrolloff"]:
        bufData["viewY"] += 1
    if bufData["pos"][0] == bufData["viewY"] - 2 + settings["scrolloff"]:
        if bufData["viewY"] > 0:
            bufData["viewY"] -= 1
    if bufData["pos"][1] == size.columns - (signcolumn + 4) + bufData["viewX"]:
        bufData["viewX"] += 1
    if bufData["pos"][1] == bufData["viewX"]:
        if bufData["viewX"] > 0:
            bufData["viewX"] -= 1

    # Screen(msg, pos, screen, resetTimer)

    Display(
        size,
        msgs,
        lineLen,
        bufData["content"],
        bufData["originalContent"],
        bufData["viewY"],
        bufData["viewX"],
        signcolumn,
        bufData["mode"],
        bufData["name"],
        bufData["pos"],
        bufData["modifiable"],
        colors,
        color,
    )

    if resetTimer > 0:
        resetTimer += 1
    if resetTimer == 11:
        msgs = [""]
        resetTimer = 0

    inp = getch()

    if bufData["mode"] == "normal":
        match inp:
            case "j":
                if bufData["pos"][0] + 1 < len(bufData["content"]):
                    bufData["pos"][0] += 1
            case "k":
                if bufData["pos"][0] > 0:
                    bufData["pos"][0] -= 1
            case "l":
                if bufData["pos"][1] + 1 < lineLen:
                    bufData["pos"][1] += 1
            case "h":
                if bufData["pos"][1] > 0:
                    bufData["pos"][1] -= 1
            case "0":
                bufData["pos"][1] = 0
                bufData["viewX"] = 0
            case "$":
                bufData["pos"][1] = lineLen
                if lineLen > size.columns:
                    bufData["viewX"] = lineLen - (size.columns - (signcolumn + 4)) // 2
            case "g":
                bufData["mode"] = "waiting"
            case "G":
                bufData["pos"][0] = len(bufData["content"]) - 1
                if len(bufData["content"]) - 1 > size.lines:
                    bufData["viewY"] = len(bufData["content"]) - (size.lines - 3) // 2
            case "i":
                if bufData["modifiable"]:
                    bufData["mode"] = "insert"
                else:
                    msgs = ["This buffer is not modifiable"]
                    resetTimer = 1
            case "a":
                if bufData["modifiable"]:
                    bufData["mode"] = "insert"
                    bufData["pos"][1] += 1
                else:
                    msgs = ["This buffer is not modifiable"]
                    resetTimer = 1
            case "d":
                if bufData["modifiable"]:
                    bufData["mode"] = "waiting"
                else:
                    msgs = ["This buffer is not modifiable"]
                    resetTimer = 1
            case "\r":
                if bufData["name"] == "Explore":
                    currentLine = bufData["content"][bufData["pos"][0]]
                    if path.isdir(bufData["baseDir"] + currentLine):
                        chdir(bufData["baseDir"] + currentLine)
                        bufData["baseDir"] = getcwd() + "/"
                        directory = []
                        for dir in listdir(bufData["baseDir"]):
                            if path.isdir(bufData["baseDir"] + dir):
                                directory.append(dir + "/")
                            if path.isfile(bufData["baseDir"] + dir):
                                directory.append(dir)
                        bufData["content"] = ["../", *directory]
                        bufData["originalContent"] = ["../", *directory]
                        if bufData["pos"][0] >= len(bufData["content"]):
                            bufData["pos"][0] = len(bufData["content"]) - 1

                        if bufData["pos"][1] >= len(
                            bufData["content"][bufData["pos"][0]]
                        ):
                            bufData["pos"][1] = len(
                                bufData["content"][bufData["pos"][0]]
                            )
                            if (
                                len(bufData["content"][bufData["pos"][0]])
                                > size.columns
                            ):
                                bufData["viewX"] = (
                                    len(bufData["content"][bufData["pos"][0]])
                                    - (size.columns - (signcolumn + 4)) // 2
                                )
                    if path.isfile(bufData["baseDir"] + currentLine):
                        buffers.pop(currentBuffer)
                        for buffer in range(len(buffers)):
                            if buffers[buffer]["name"] == currentLine:
                                currentBuffer = buffer
                                break
                        else:
                            with open(bufData["baseDir"] + currentLine) as data:
                                content = data.read().splitlines()
                                buffers.append(
                                    {
                                        "name": currentLine,
                                        "content": content,
                                        "originalContent": list(content),
                                        "viewY": 0,
                                        "viewX": 0,
                                        "pos": [0, 0],
                                        "mode": "normal",
                                        "modifiable": True,
                                    }
                                )
                                currentBuffer = len(buffers) - 1
                else:
                    if bufData["pos"][0] + 1 < len(bufData["content"]):
                        bufData["pos"][0] += 1
            case "%":
                if bufData["name"] == "Explore":
                    bufData["mode"] = "command"
                    msgs = ["Enter filename: "]
            case "r":
                if bufData["name"] == "Explore":
                    bufData["mode"] = "command"
                    msgs = ["Rename to: "]
            case "D":
                if bufData["name"] == "Explore":
                    bufData["mode"] = "command"
                    msgs = ["Delete file: "]
            case "d":
                if bufData["name"] == "Explore":
                    bufData["mode"] = "command"
                    msgs = ["Enter directory name: "]
            case ":":
                bufData["mode"] = "command"
                msgs = [":"]
            case "\x03":
                msgs = ["Use :q to exit"]
                resetTimer = 1
    elif bufData["mode"] == "insert":
        match inp:
            case "\x03" | "\x1b":
                bufData["mode"] = "normal"
            case "\r":
                buf = bufData["content"][bufData["pos"][0]]
                before = buf[: bufData["pos"][1]]
                after = buf[bufData["pos"][1] :]
                bufData["content"][bufData["pos"][0]] = before
                bufData["content"].insert(bufData["pos"][0] + 1, after)
                bufData["pos"][0] += 1
                bufData["pos"][1] = 0
            case "\t":
                buf = bufData["content"][bufData["pos"][0]]
                before = buf[: bufData["pos"][1]]
                after = buf[bufData["pos"][1] :]
                bufData["content"][bufData["pos"][0]] = (
                    before + " " * settings["tabwidth"] + after
                )
                bufData["pos"][1] += settings["tabwidth"]

            case "\x7f":
                if bufData["pos"][0] != 0:
                    buf = bufData["content"][bufData["pos"][0]]
                    before = buf[: bufData["pos"][1]]
                    after = buf[bufData["pos"][1] :]
                    if len(before) == 0:
                        if bufData["pos"][0] - 1 < len(bufData["content"]):
                            lastLineLen = (
                                len(bufData["content"][bufData["pos"][0] - 1]) + 1
                            )
                        else:
                            lastLineLen = 0
                        if bufData["pos"][0] - 1 < len(bufData["content"]):
                            bufData["content"].pop(bufData["pos"][0])
                            bufData["content"][bufData["pos"][0] - 1] += after
                        else:
                            bufData["content"].pop(-1)
                        if bufData["pos"][0] > 0:
                            bufData["pos"][0] -= 1
                            bufData["pos"][1] = lastLineLen
                    else:
                        bufData["content"][bufData["pos"][0]] = before[0:-1] + after
                    if bufData["pos"][1] > 0:
                        bufData["pos"][1] -= 1
            case _:
                buf = bufData["content"][bufData["pos"][0]]
                before = buf[: bufData["pos"][1]]
                after = buf[bufData["pos"][1] :]
                bufData["content"][bufData["pos"][0]] = before + inp + after
                bufData["pos"][1] += 1
    elif bufData["mode"] == "command":
        match inp:
            case "\r":
                arguments = msgs[0].strip().split(":")
                commands = arguments[1].split(" ")
                if arguments[0] == "Enter filename":
                    if arguments[1]:
                        try:
                            with open(
                                bufData["baseDir"] + arguments[1].strip(), "w"
                            ) as data:
                                data.write("")
                            msgs = [""]
                            directory = []
                            for dir in listdir(bufData["baseDir"]):
                                if path.isdir(bufData["baseDir"] + dir):
                                    directory.append(dir + "/")
                                if path.isfile(bufData["baseDir"] + dir):
                                    directory.append(dir)
                            bufData["content"] = ["../", *directory]
                            bufData["originalContent"] = ["../", *directory]
                        except:
                            msgs = ["Directory doesn't exists"]
                            resetTimer = 1
                    else:
                        msgs = [""]
                elif arguments[0] == "Rename to":
                    if arguments[1]:
                        try:
                            currentLine = bufData["content"][bufData["pos"][0]]
                            rename(
                                bufData["baseDir"] + currentLine,
                                bufData["baseDir"] + arguments[1].strip(),
                            )
                            directory = []
                            for dir in listdir(bufData["baseDir"]):
                                if path.isdir(bufData["baseDir"] + dir):
                                    directory.append(dir + "/")
                                if path.isfile(bufData["baseDir"] + dir):
                                    directory.append(dir)
                            bufData["content"] = ["../", *directory]
                            bufData["originalContent"] = ["../", *directory]
                            msgs = [""]
                        except:
                            msgs = ["Directory doesn't exists"]
                            resetTimer = 1
                    else:
                        msgs = [""]
                elif arguments[0] == "Delete file":
                    if (
                        arguments[1].strip().lower() == "y"
                        or arguments[1].strip().lower() == "yes"
                    ):
                        currentLine = bufData["content"][bufData["pos"][0]]
                        if path.isfile(bufData["baseDir"] + currentLine):
                            remove(bufData["baseDir"] + currentLine)
                        if path.isdir(bufData["baseDir"] + currentLine):
                            rmtree(bufData["baseDir"] + currentLine)
                        directory = []
                        for dir in listdir(bufData["baseDir"]):
                            if path.isdir(bufData["baseDir"] + dir):
                                directory.append(dir + "/")
                            if path.isfile(bufData["baseDir"] + dir):
                                directory.append(dir)
                        bufData["content"] = ["../", *directory]
                        bufData["originalContent"] = ["../", *directory]
                    msgs = [""]
                elif arguments[0] == "Enter directory name":
                    if arguments[1]:
                        mkdir(bufData["baseDir"] + arguments[1].strip())
                        directory = []
                        for dir in listdir(bufData["baseDir"]):
                            if path.isdir(bufData["baseDir"] + dir):
                                directory.append(dir + "/")
                            if path.isfile(bufData["baseDir"] + dir):
                                directory.append(dir)
                        bufData["content"] = ["../", *directory]
                        bufData["originalContent"] = ["../", *directory]
                    msgs = [""]
                else:
                    match commands[0]:
                        case "q" | "q!":
                            if commands[0] == "q":
                                if bufData["name"] != "Explore":
                                    if bufData["originalContent"] == bufData["content"]:
                                        buffers.pop(currentBuffer)
                                        currentBuffer = len(buffers) - 1
                                        msgs = [""]
                                    else:
                                        msgs = [
                                            "Unsaved changes, pls save before closing the buffer"
                                        ]
                                        resetTimer = 1
                                else:
                                    buffers.pop(currentBuffer)
                                    currentBuffer = len(buffers) - 1
                                    msgs = [""]

                            else:
                                buffers.pop(currentBuffer)
                                currentBuffer = len(buffers) - 1
                                msgs = [""]
                        case "qa" | "qa!":
                            if commands[0] == "qa":
                                for buffer in range(len(buffers)):
                                    if (
                                        buffers[buffer]["content"]
                                        != buffers[buffer]["originalContent"]
                                    ):
                                        msgs = [
                                            f"Unsaved changes in buffer {buffer}, pls save before exiting"
                                        ]
                                        break
                                else:
                                    buffers = []
                            else:
                                buffers = []
                        case "w" | "wq" | "wq!":
                            if bufData["modifiable"]:
                                if len(commands) > 1:
                                    with open(commands[1], "w") as data:
                                        data.write("\n".join(bufData["content"]))
                                else:
                                    with open(bufData["name"], "w") as data:
                                        data.write("\n".join(bufData["content"]))
                                bufData["originalContent"] = list(bufData["content"])
                                msgs = [""]
                            else:
                                msgs = ["Buffer is not modifiable"]
                                resetTimer = 1
                            if commands[0] == "wq" or commands[0] == "wq!":
                                buffers.pop(currentBuffer)
                                if currentBuffer >= len(buffers):
                                    currentBuffer = len(buffers) - 1
                                msgs = [""]
                        case "wa" | "wqa" | "wqa!":
                            for buffer in range(len(buffers)):
                                if buffers[buffer]["modifiable"]:
                                    with open(buffers[buffer]["name"], "w") as data:
                                        data.write(
                                            "\n".join(buffers[buffer]["content"])
                                        )
                                    buffers[buffer]["originalContent"] = list(
                                        buffers[buffer]["content"]
                                    )
                                    msgs = [""]
                                    if commands[0] == "wqa" or commands[0] == "wqa!":
                                        buffers.pop(buffer)
                                        if currentBuffer >= len(buffers):
                                            currentBuffer = len(buffers) - 1
                                        msgs = [""]
                                else:
                                    msgs = [f"Buffer {buffer} is not modifiable"]
                                    resetTimer = 1
                                    break
                        case "Explore" | "Ex":
                            msgs = [""]
                            for buffer in range(len(buffers)):
                                if buffers[buffer]["name"] == "Explore":
                                    currentBuffer = buffer
                                    break
                            else:
                                directory = []
                                for dir in listdir(getcwd()):
                                    if path.isdir(dir):
                                        directory.append(dir + "/")
                                    if path.isfile(dir):
                                        directory.append(dir)

                                buffers.append(
                                    {
                                        "name": "Explore",
                                        "content": ["../", *directory],
                                        "originalContent": ["../", *directory],
                                        "viewY": 0,
                                        "viewX": 0,
                                        "pos": [0, 0],
                                        "mode": "normal",
                                        "modifiable": False,
                                        "baseDir": getcwd() + "/",
                                    }
                                )
                                currentBuffer = len(buffers) - 1
                        case "buffer":
                            if len(commands) > 1:
                                if int(commands[1]) < len(buffers):
                                    currentBuffer = int(commands[1])
                                    msgs = [""]
                                else:
                                    msgs = ["That buffer doesn't exists"]
                                    resetTimer = 1
                            else:
                                msgs = [str(currentBuffer)]
                        case "badd" | "e":
                            if len(commands) > 1:
                                try:
                                    with open(commands[1]) as data:
                                        content = data.read().splitlines()
                                        buffers.append(
                                            {
                                                "name": commands[1],
                                                "content": content,
                                                "originalContent": list(content),
                                                "viewY": 0,
                                                "viewX": 0,
                                                "pos": [0, 0],
                                                "mode": "normal",
                                                "modifiable": True,
                                            }
                                        )
                                    msgs = [""]
                                except:
                                    msgs = ["File/Folder doesn't exists!"]
                                    resetTimer = 1
                            else:
                                msgs = ["Argument required!"]
                                resetTimer = 1

                        case "bdel":
                            if len(commands) > 1:
                                if int(commands[1]) < len(buffers):
                                    buffers.pop(int(commands[1]))
                                    if currentBuffer >= len(buffers):
                                        currentBuffer = len(buffers) - 1
                                    msgs = [""]
                                else:
                                    msgs = ["That buffer doesn't exists"]
                                    resetTimer = 1
                            else:
                                msgs = ["Argument required!"]
                                resetTimer = 1
                        case _:
                            msgs = ["Command doesn't exist!!"]
                            resetTimer = 1
                bufData["mode"] = "normal"
            case "\x7f":
                if not (len(msgs[0]) > 1 and msgs[0].strip()[-1] == ":"):
                    msgs[0] = msgs[0][0:-1]
                    if msgs[0] == "":
                        bufData["mode"] = "normal"
            case "\x03" | "\x1b":
                bufData["mode"] = "normal"
                msgs = [""]
            case _:
                msgs[0] += inp
    elif bufData["mode"] == "waiting":
        match inp:
            case "g":
                bufData["viewY"] = 0
                bufData["pos"][0] = 0
            case "d":

                bufData["content"].pop(bufData["pos"][0])
                if bufData["pos"][0] == len(bufData["content"]):
                    bufData["pos"][0] -= 1
            case "\x03" | "\x1b":
                bufData["mode"] = "normal"
        bufData["mode"] = "normal"
clear()
