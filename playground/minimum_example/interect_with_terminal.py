import curses
from typing import Any

try:
    curses._CursesWindow
except Exception as e:
    curses._CursesWindow = Any

IN = False

def the_function(stdscr: curses._CursesWindow):
    global IN

    stdscr.clear()
    stdscr.refresh()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE);
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLUE);
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_MAGENTA);

    color_index = 1
    while True:
        if not 1 <= color_index <= 3:
            color_index = 1

        if color_index == 3:
            stdscr.bkgd(' ', curses.color_pair(color_index) | curses.A_BOLD | curses.A_REVERSE)
        else:
            stdscr.bkgd(' ', curses.color_pair(color_index) | curses.A_BOLD)

        char = stdscr.getch()
        stdscr.addstr(1,1, str(char))

        if char == ord('q'):
            break  # Exit the while loop
        elif char == curses.KEY_ENTER or char == 10:
            IN = True
            break  # Exit the while loop

        color_index += 1

curses.wrapper(the_function)
if IN:
    print("\nWelcome to the matrix!")
