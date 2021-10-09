#!/usr/bin/env python3

import curses
from curses import wrapper

from wikijscmd import util, commands

def pager(stdscr, lst):
    '''
    Runs a pager for each string item in lst
    '''
    cols = stdscr.getmaxyx()[1]
    rows = stdscr.getmaxyx()[0]
    offset = 0
    selected = 0
    while True:
        stdscr.clear()
        for i in range(min(rows-1, len(lst))):
            x = lst[i+offset]
            if i+offset == selected:
                stdscr.addstr(i, 0, x[:cols], curses.A_UNDERLINE)
            else:
                stdscr.addstr(i, 0, x[:cols])
        if offset == 0:
            stdscr.addstr(rows-1, 0, "--top--", curses.A_REVERSE)
        elif offset + rows <= len(lst):
            stdscr.addstr(rows-1, 0, "--more--", curses.A_REVERSE)
        else:
            stdscr.addstr(rows-1, 0, "--end--", curses.A_REVERSE)
        k = stdscr.getch()
        if k == curses.KEY_DOWN or k == ord('j'):
            selected = min(len(lst), selected+1)
            if (selected - offset) > (2 * rows / 3):
                offset = min(len(lst)-rows+1, offset+1)
        elif k == curses.KEY_UP or k == ord('k'):
            selected = max(0, selected-1)
            if (selected - offset) < (rows / 3):
                offset = max(0, offset-1)
        elif k == curses.KEY_NPAGE:
            offset = min(len(lst)-rows+1, offset+rows-2)
            selected = min(len(lst)-rows+1, selected+rows-2)
        elif k == curses.KEY_PPAGE:
            offset = max(0, offset-rows+2)
            selected = max(0, selected-rows+2)
        elif k == curses.KEY_HOME:
            offset = 0
            selected = 0
        elif k == curses.KEY_END:
            offset = len(lst)-rows+1
            selected = len(lst)-1
        elif k == curses.KEY_ENTER or k == 10:
            return {"index": selected, "action": "select"}
        elif k == ord('q'):
            return {"index": selected, "action": "quit"}
        elif k == ord('e'):
            return {"index": selected, "action": "edit"}
        elif k == ord('c'):
            return {"index": selected, "action": "create"}
        elif k == ord('t'):
            return {"index": selected, "action": "today"}
        stdscr.refresh()

def enter_value(stdscr, prefix, row):
    """
    Creates a prompt to enter a value on the given row
    """
    title = ""
    stdscr.addstr(row,0, prefix + title)
    k = stdscr.getch()
    while k != 10 and k != curses.KEY_ENTER:
        if k in (curses.KEY_BACKSPACE, '\b', '\x7f'):
            if len(title) > 0:
                title = title[:-1]
        else:
            title += chr(k)
        stdscr.deleteln()
        stdscr.addstr(row,0, prefix + title)
        k = stdscr.getch()
    return title

def m(stdscr):
    """
    The main method for the ncurses wrapper
    """
    items = util.get_tree("")
    while True:
        ret = pager(stdscr, [x["path"] + "\t" + x["title"] for x in items])
        if ret["action"] == "select":
            selected = items[ret["index"]]
            ret = pager(stdscr, util.get_single_page(selected["path"])["content"].split("\n"))
        elif ret["action"] == "edit":
            selected = items[ret["index"]]
            commands.edit(selected["path"], True)
        elif ret["action"] == "create":
            stdscr.clear()
            title = enter_value(stdscr, "Enter title: ", 0)
            path = enter_value(stdscr, "Enter path: ", 1)
            commands.create(path, title)
        elif ret["action"] == "today":
            commands.today()
        else:
            break

def tui():
    try:
        wrapper(m)
    except Exception as e:
        raise e
