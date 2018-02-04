# ============================================================================
# FILE: standalone.py
# AUTHOR: David Johansson
# License: MIT license
# ============================================================================

import curses

buffer = ['just an example', 'file 1', 'file 2', 'file 3']

def main(stdscr):

    # Clear screen
    stdscr.clear()
    
    while True:
        for i in range(len(buffer)):
            stdscr.addstr(i, 0, buffer[i])

        debug_line = len(buffer) + 1

        c = stdscr.getkey()


        if c == 'q':
            break
        elif c == '\t':
            stdscr.addstr(debug_line, 0, 'tab      ')
        elif c == 'KEY_UP':
            stdscr.addstr(debug_line, 0, 'up       ')
        elif c == 'KEY_DOWN':
            stdscr.addstr(debug_line, 0, 'down     ')
        elif c == '\x7f':
            stdscr.addstr(debug_line, 0, 'backspace')
        elif c == '\x0a' or c == '\x0d':
            stdscr.addstr(debug_line, 0, 'enter    ')


curses.wrapper(main)
