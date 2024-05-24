from os import get_terminal_size, listdir
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
    name = "[unamed]"
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


# def ExploreScreen(
#     size,
#     msg,
#     lineLen,
#     buffer,
#     viewY,
#     viewX,
#     mode,
#     pos,
#     colors,
#     dir,
# ):
#     for y in range(size.lines - 3):
#         line = ""
#
#         if len(dir) > y + viewY:
#             for x in range(len(dir[y + viewY])):
#                 if x < size.columns - (signcolumnDir + 4):
#                     if pos[1] >= lineLen:
#                         if mode == "normal":
#                             if [y + viewY, x + viewX] == [pos[0], lineLen - 1]:
#                                 line += color(
#                                     dir[y + viewY][x + viewX],
#                                     forground=colors["forground_white"],
#                                     background=colors["background_black"],
#                                 )
#                             else:
#                                 if len(dir[y + viewY]) > x + viewX:
#                                     line += dir[y + viewY][x + viewX]
#                         elif mode == "insert":
#                             if [y + viewY, x + viewX + 1] == [pos[0], lineLen]:
#                                 line += dir[y + viewY][x + viewX]
#                                 line += color(
#                                     " ",
#                                     forground=colors["forground_white"],
#                                     background=colors["background_black"],
#                                 )
#                             else:
#                                 if len(dir[y + viewY]) > x + viewX:
#                                     line += dir[y + viewY][x + viewX]
#                     else:
#                         if [y + viewY, x + viewX] == pos:
#                             line += color(
#                                 dir[y + viewY][x + viewX],
#                                 forground=colors["forground_white"],
#                                 background=colors["background_black"],
#                             )
#                         else:
#                             if len(dir[y + viewY]) > x + viewX:
#                                 line += dir[y + viewY][x + viewX]
#
#             if line == "" and y + viewY == pos[0]:
#                 line += color(
#                     " ",
#                     forground=colors["forground_white"],
#                     background=colors["background_black"],
#                 )
#
#             buffer.append(f"{' '*signcolumnDir}{line}")
#         else:
#             buffer.append("")
#
#     buffer.append(
#         f"{color('-', forground=colors['forground_black'])} {mode.upper()} {color('-', forground=colors['forground_black'])} Explore {color('-'*(size.columns - 13 - len(mode)), forground=colors['forground_black'])}"
#     )
#     buffer.append(msg)
#     print("\n".join(buffer), end="")
#

# def Screen():
#     global msg
#     global pos
#     global screen
#     global resetTimer
#     global size
#     global msg
#     global lineLen
#     global buffer
#     global content
#     global originalContent
#     global viewY
#     global viewX
#     global signcolumn
#     global mode
#     global name
#     global pos
#     global colors
#     global dir
#     global inp
#
#     prevInp = str(inp)
#     while True:
#         if prevInp != inp:
#             clear()
#             buffer = [
#                 "\n",
#                 color("-" * size.columns, forground=colors["forground_black"]),
#             ]
#
#             if screen == "editor":
#                 lineLen = len(content[pos[0]])
#                 EditorScreen(
#                     size,
#                     msg,
#                     lineLen,
#                     buffer,
#                     content,
#                     originalContent,
#                     viewY,
#                     viewX,
#                     signcolumn,
#                     mode,
#                     name,
#                     pos,
#                     colors,
#                 )
#             elif screen == "explore":
#                 lineLen = len(dir[pos[0]])
#                 ExploreScreen(
#                     size, msg, lineLen, buffer, viewY, viewX, mode, pos, colors, dir
#                 )
#             prevInp = str(inp)
#
#         if len(msg) > 0 and msg[0] != ":":
#             resetTimer += 1
#         if resetTimer == 10:
#             msg = ""
#             resetTimer = 0


# Thread(target=Screen, daemon=True).start()

while buffers:
    bufData = buffers[currentBuffer]

    name = bufData["name"]
    content = bufData["content"]
    originalContent = bufData["originalContent"]
    pos = bufData["pos"]
    viewY = bufData["viewY"]
    viewX = bufData["viewX"]
    mode = bufData["mode"]
    modifiable = bufData["modifiable"]

    signcolumn = len(str(len(content)))

    lineLen = int(len(content[pos[0]]))

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

    # Screen(msg, pos, screen, resetTimer)

    Display(
        size,
        msg,
        lineLen,
        content,
        originalContent,
        viewY,
        viewX,
        signcolumn,
        mode,
        name,
        pos,
        colors,
        color,
    )

    # elif screen == "explore":
    #     lineLen = len(dir[pos[0]])
    #     ExploreScreen(size, msg, lineLen, buffer, viewY, viewX, mode, pos, colors, dir)

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
                bufData["mode"] = "command"
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
                                buffers.pop(currentBuffer)
                                currentBuffer = len(buffers) - 1
                                msg = ""
                            else:
                                msg = "Unsaved changes, pls save before closing the buffer"
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
                        if modifiable:
                            if len(commands) > 1:
                                with open(commands[1], "w") as data:
                                    data.write("\n".join(content))
                            else:
                                with open(name, "w") as data:
                                    data.write("\n".join(content))
                            originalContent = list(content)
                            msg = ""
                            if commands[0] == "wq":
                                if originalContent == content:
                                    buffers.pop(currentBuffer)
                                    currentBuffer = len(buffers) - 1
                                    msg = ""
                                else:
                                    msg = "Unsaved changes, pls save before exiting"
                            if commands[0] == "wq!":
                                buffers.pop(currentBuffer)
                                currentBuffer = len(buffers) - 1
                                msg = ""
                        else:
                            msg = "This buffer is not modifiable"
                    case "Explore" | "Ex":
                        msg = ""
                        buffers.append(
                            {
                                "name": "Explore",
                                "content": listdir(),
                                "originalContent": listdir(),
                                "viewY": 0,
                                "viewX": 0,
                                "pos": [0, 0],
                                "mode": "normal",
                                "modifiable": False,
                            }
                        )
                        currentBuffer = len(buffers) - 1
                    case "buffer":
                        if len(commands) > 1:
                            if int(commands[1]) < len(buffers):
                                currentBuffer = int(commands[1])
                            else:
                                msg = "That buffer doesn't exists"
                        else:
                            msg = str(currentBuffer)
                    case "badd":
                        pass
                    case "bdel":
                        pass
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
clear()
