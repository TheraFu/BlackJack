import curses


class MiniMenu:
    def __init__(self, scr, items):
        self.scr = scr
        self.items = items
        self.selected = 0
        self.coor = self.scr.getyx()

    def draw(self):
        if len(self.items) > self.scr.getmaxyx()[0] - self.coor[0]:
            n = len(self.items)
            for i in range(n): self.scr.addstr("\n")
            self.coor = (self.coor[0] - n, self.coor[1])
            self.scr.move(self.coor[0], self.coor[1])
        for i in range(len(self.items)):
            if i == self.selected:
                self.scr.addstr(self.coor[0] + i, self.coor[1], self.items[i] + "\n", curses.A_REVERSE)
            else:
                self.scr.addstr(self.coor[0] + i, self.coor[1], self.items[i] + "\n")
        self.scr.refresh()

    def erase(self):
        for i in range(len(self.items)):
            self.scr.move(self.coor[0] + i, self.coor[1])
            self.scr.clrtoeol()
        self.scr.move(self.coor[0], self.coor[1])

    def select(self):
        self.draw()
        x = self.scr.getch()
        while x != curses.KEY_ENTER and x != 10 and x != 13:
            if x == curses.KEY_UP and self.selected > 0:
                self.selected -= 1
                self.draw()
            elif x == curses.KEY_DOWN and self.selected < len(self.items) - 1:
                self.selected += 1
                self.draw()
            x = self.scr.getch()
        self.erase()
        self.scr.addstr(self.coor[0], self.coor[1], self.items[self.selected] + "\n", curses.A_REVERSE)
        return self.items[self.selected]
