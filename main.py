from os import get_terminal_size, listdir, path
from sys import argv
from display import Display
from utility import color, getch, clear, colors

msg = ""
settings = {"cursorcolor": "black", "scrolloff": 10}

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
                "content": content,
                "originalContent": list(content),
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

    lineLen = int(len(bufData["content"][bufData["pos"][0]]))

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
        msg,
        lineLen,
        bufData["content"],
        bufData["originalContent"],
        bufData["viewY"],
        bufData["viewX"],
        signcolumn,
        bufData["mode"],
        bufData["name"],
        bufData["pos"],
        colors,
        color,
    )

    if len(msg) > 0 and msg[0] != ":":
        resetTimer += 1
    if resetTimer == 10:
        msg = ""
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
                    msg = "This buffer is not modifiable"
            case "a":
                bufData["mode"] = "insert"
                bufData["pos"][1] += 1
            case "\r":
                if bufData["name"] == "Explore":
                    currentLine = bufData["content"][bufData["pos"][0]]
                    if path.isdir(bufData["baseDir"] + currentLine):
                        bufData["baseDir"] = bufData["baseDir"] + currentLine
                        bufData["content"] = ["../", *listdir(bufData["baseDir"])]
                    if path.isfile(bufData["baseDir"] + currentLine):
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
            case ":":
                bufData["mode"] = "command"
                msg = ":"
            case "\x03":
                msg = "Use :q to exit"
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
                commands = (msg.strip().split(":"))[1].split(" ")
                match commands[0]:
                    case "q" | "q!":
                        if commands[0] == "q":
                            if bufData["name"] != "Explore":
                                if bufData["originalContent"] == bufData["content"]:
                                    buffers.pop(currentBuffer)
                                    currentBuffer = len(buffers) - 1
                                    msg = ""
                                else:
                                    msg = "Unsaved changes, pls save before closing the buffer"
                            else:
                                buffers.pop(currentBuffer)
                                currentBuffer = len(buffers) - 1
                                msg = ""

                        else:
                            buffers.pop(currentBuffer)
                            currentBuffer = len(buffers) - 1
                            msg = ""
                    # case "qa" | "qa!":
                    #     if commands[0] == "qa":
                    #         if originalContent == content:
                    #             clear()
                    #             break
                    #         else:
                    #             msg = "Unsaved changes, pls save before exiting"
                    #     else:
                    #         clear()
                    #         break
                    case "w" | "wq" | "wq!":
                        if bufData["modifiable"]:
                            if len(commands) > 1:
                                with open(commands[1], "w") as data:
                                    data.write("\n".join(bufData["content"]))
                            else:
                                with open(bufData["name"], "w") as data:
                                    data.write("\n".join(bufData["content"]))
                            bufData["originalContent"] = list(bufData["content"])
                            msg = ""
                            if commands[0] == "wq":
                                if bufData["name"] != "Explore":
                                    if bufData["originalContent"] == bufData["content"]:
                                        buffers.pop(currentBuffer)
                                        currentBuffer = len(buffers) - 1
                                        msg = ""
                                    else:
                                        msg = "Unsaved changes, pls save before exiting"
                                else:
                                    buffers.pop(currentBuffer)
                                    currentBuffer = len(buffers) - 1
                                    msg = ""
                            if commands[0] == "wq!":
                                buffers.pop(currentBuffer)
                                currentBuffer = len(buffers) - 1
                                msg = ""
                        else:
                            msg = "This buffer is not modifiable"
                    case "Explore" | "Ex":
                        msg = ""
                        for buffer in range(len(buffers)):
                            if buffers[buffer]["name"] == "Explore":
                                currentBuffer = buffer
                                break
                        else:
                            buffers.append(
                                {
                                    "name": "Explore",
                                    "content": ["../", *listdir("./")],
                                    "originalContent": ["../", *listdir("./")],
                                    "viewY": 0,
                                    "viewX": 0,
                                    "pos": [0, 0],
                                    "mode": "normal",
                                    "modifiable": False,
                                    "baseDir": "./",
                                }
                            )
                            currentBuffer = len(buffers) - 1
                    case "buffer":
                        if len(commands) > 1:
                            if int(commands[1]) < len(buffers):
                                currentBuffer = int(commands[1])
                                msg = ""
                            else:
                                msg = "That buffer doesn't exists"
                        else:
                            msg = str(currentBuffer)
                    case "badd" | "e":
                        if len(commands) > 1:
                            try:
                                with open(commands[1]) as data:
                                    content = data.read().splitlines()
                                    buffers.append(
                                        {
                                            "name": "Explore",
                                            "content": content,
                                            "originalContent": list(content),
                                            "viewY": 0,
                                            "viewX": 0,
                                            "pos": [0, 0],
                                            "mode": "normal",
                                            "modifiable": True,
                                        }
                                    )
                                msg = ""
                            except:
                                msg = "File/Folder doesn't exists!"
                        else:
                            msg = "Argument required!"

                    case "bdel":
                        if len(commands) > 1:
                            if int(commands[1]) < len(buffers):
                                buffers.pop(int(commands[1]))
                                if currentBuffer >= len(buffers):
                                    currentBuffer = len(buffers) - 1
                                msg = ""
                            else:
                                msg = "That buffer doesn't exists"
                        else:
                            msg = "Argument required!"
                    case _:
                        msg = "Command doesn't exist!!"
                bufData["mode"] = "normal"
            case "\x7f":
                msg = msg[0:-1]
                if msg == "":
                    bufData["mode"] = "normal"
            case "\x03" | "\x1b":
                bufData["mode"] = "normal"
                msg = ""
            case _:
                msg += inp
    elif bufData["mode"] == "waiting":
        match inp:
            case "g":
                bufData["viewY"] = 0
                bufData["pos"][0] = 0
            case "\x03" | "\x1b":
                bufData["mode"] = "normal"
        bufData["mode"] = "normal"
clear()
