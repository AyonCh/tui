from curses import window, wrapper, A_UNDERLINE
from sys import argv

args = argv


def main(stdscr: window):
    name = ""
    content = [""]
    y, x = stdscr.getmaxyx()
    stdscr.nodelay(True)

    signcolum = int(len(str(y)))

    if len(args) < 2:
        name = "[unamed]"
    else:
        name = args[1]
        with open(name) as data:
            content = data.read().splitlines()
    while True:
        try:
            key = stdscr.getkey()
        except:
            key = None

        for line in content:
            stdscr.addstr(line)
            stdscr.refresh()


wrapper(main)
