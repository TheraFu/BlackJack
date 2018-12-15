import re
import curses
from time import sleep

from minimenu import MiniMenu


class ScreenHelper:

    COLORS = {
        "red": 1,
        "cyan": 2,
        "black": 3,
        "blue": 4,
        "green": 5,
        "magenta": 6,
        "white": 7,
        "yellow": 8
    }

    def __init__(self, scr):
        self.scr = scr

    def clear_screen(self):
        self.scr.clear()

    def wait_for_enter(self):
        x = self.scr.getch()
        while x != curses.KEY_ENTER and x != 10 and x != 13:
            x = self.scr.getch()

    def print_string(self, string, colornum=0, bold=False, waittime=1):
        style = curses.color_pair(colornum) | curses.A_BOLD if bold else curses.color_pair(colornum)
        self.scr.addstr(string, style)
        sleep(waittime)
        self.scr.refresh()

    def get_nonempty_input(self):
        x = self.scr.getstr()
        while len(x) <= 0:
            self.scr.move(self.scr.getyx()[0] - 1, self.scr.getyx()[1])
            x = self.scr.getstr()
        return x

    def get_int_within_range(self, min, max):
        x = self.get_nonempty_input()
        while not re.match("b'[0-9]+'", str(x)) or not min <= int(x) <= max:
            self.print_string("Invalid input, input must be a integer in the range: " + str((min, max)) + "\n")
            x = self.get_nonempty_input()
        return int(x)

    def menu_from_list(self, elist):
        menu = MiniMenu(self.scr, elist)
        selected = menu.select()
        return selected