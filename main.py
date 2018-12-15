import curses
from curses import wrapper
from game import Game
from screen import ScreenHelper


def main(stdscr):
    # set up for curses
    curses.start_color()
    curses.use_default_colors()
    curses.echo()
    curses.init_pair(0, -1, -1)
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_CYAN, -1)
    curses.init_pair(3, curses.COLOR_BLACK, -1)
    curses.init_pair(4, curses.COLOR_BLUE, -1)
    curses.init_pair(5, curses.COLOR_GREEN, -1)
    curses.init_pair(6, curses.COLOR_MAGENTA, -1)
    curses.init_pair(7, curses.COLOR_WHITE, -1)
    curses.init_pair(8, curses.COLOR_YELLOW, -1)
    stdscr.scrollok(True)
    stdscr.clear()

    helper = ScreenHelper(stdscr)

    # determine player and deck number
    helper.print_string("How many players will be playing?\n" +
                        "(Enter a number between 1 and 3 then press ENTER)\n", helper.COLORS["cyan"])
    num_player = helper.get_int_within_range(1, 3)
    helper.print_string("How many decks of cards do you want to use?\n" +
                        "(Enter a number between 1 and 8 then press ENTER)\n", helper.COLORS["cyan"])
    num_deck = helper.get_int_within_range(0, 9)
    helper.clear_screen()

    # call game and keep gaming
    game = Game(num_deck, num_player, helper)
    game.keep_gaming()


if __name__ == "__main__":
    wrapper(main)
