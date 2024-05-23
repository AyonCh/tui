def color(text, colors, forground="", background=""):
    return f"""{forground}{background}{text}{colors["RESET"]}"""
