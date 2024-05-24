def Display(
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
):
    buffer = ["\n", color("-" * size.columns, forground=colors["forground_black"])]
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

            buffer.append(
                f"{color(y + viewY + 1, forground=colors['forground_black'])}{' '*(signcolumn-currentY)} {color('|', forground=colors['forground_black'])} {line}"
            )
        else:
            buffer.append("")

    if originalContent == content:
        buffer.append(
            f"{color('-', forground=colors['forground_black'])} {mode.upper()} {color('-', forground=colors['forground_black'])} {name} {color('-'*(size.columns - 6 - len(name) - len(mode)), forground=colors['forground_black'])}"
        )
    else:
        buffer.append(
            f"{color('-', forground=colors['forground_black'])} {mode.upper()} {color('-', forground=colors['forground_black'])} {name} [+] {color('-'*(size.columns - 10 - len(name) - len(mode)), forground=colors['forground_black'])}"
        )

    buffer.append(msg)

    print("\n".join(buffer), end="")
