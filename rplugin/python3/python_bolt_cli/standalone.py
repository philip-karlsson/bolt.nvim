# ============================================================================
# FILE: standalone.py
# AUTHOR: David Johansson
# License: MIT license
# ============================================================================

import sys
sys.path.append('..')

import curses
from bolt_tui import tui

def print_panes(stdscr, bolt):
    buffer = bolt.get_panes()
    for i in range(0, len(buffer)):
        stdscr.addstr(i, 0, buffer[i])

def main(stdscr):

    bolt = tui.tui()

    # Clear screen
    stdscr.clear()
    print_panes(stdscr, bolt)
    
    debug_line = 10

    while True:

        c = stdscr.getkey()
        stdscr.clear()

        if c == 'q':
            break
        elif c == '\t':
            bolt.cmd_tab()
            print_panes(stdscr, bolt)
            stdscr.addstr(debug_line, 0, 'tab      ')
        elif c == 'KEY_UP':
            bolt.cmd_up()
            print_panes(stdscr, bolt)
            stdscr.addstr(debug_line, 0, 'up       ')
        elif c == 'KEY_DOWN':
            bolt.cmd_down()
            print_panes(stdscr, bolt)
            stdscr.addstr(debug_line, 0, 'down     ')
        elif c == '\x7f':
            stdscr.addstr(debug_line, 0, 'backspace')
        elif c == '\x0a' or c == '\x0d':
            stdscr.addstr(debug_line, 0, 'enter    ')


curses.wrapper(main)
