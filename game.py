from deck import Deck
from player import Player, Dealer


class Game:
    def __init__(self, num_deck, num_player, screen):
        self.round = 1
        self.deck = Deck(num_deck)
        self.players = [Player("Player " + str(i)) for i in range(1, num_player + 1)]
        self.dealer = Dealer()
        self.screen = screen

    def new_game(self):
        self.screen.print_string("\n===================\nRound "
                                 + str(self.round)
                                 + "!\n===================\n\n", self.screen.COLORS["yellow"])

        self.round += 1
        self.dealer.start_game(self.deck)

        for player in self.players:
            player.start_game(self.deck)
            self.screen.print_string(player.print_token(), self.screen.COLORS["yellow"])

    def place_bets(self):
        self.screen.print_string("\n\nPlayers, please first place your bets!\n"
                                 + "(Enter a integer between 1 and your current tokens, then hit ENTER to confirm)\n\n",
                                 self.screen.COLORS["cyan"])

        for player in self.players:
            self.screen.print_string(player.name + ", please place your bet.\n", self.screen.COLORS["green"])
            x = self.screen.get_int_within_range(1, player.tokens)
            player.place_bet(x)
            self.screen.print_string(player.print_bet(), self.screen.COLORS["green"])

    def get_initial_two_cards(self):
        self.screen.print_string("Now everyone gets their starting cards!\n\n", self.screen.COLORS["cyan"])

        self.dealer.get_initial_two()
        self.screen.print_string(self.dealer.print_hand(), waittime=2)

        for player in self.players:
            player.get_initial_two()
            self.screen.print_string(player.print_hand(), waittime=2)

        if self.dealer.blackjack():
            self.screen.print_string("Dealer's got blackjack!\n", self.screen.COLORS["red"], waittime=2)
            for player in self.players:
                player.playing = False
                self.screen.print_string(player.final_check(self.dealer.get_score()), self.screen.COLORS["red"],
                                         waittime=2)
                self.screen.print_string(player.print_token(), self.screen.COLORS["yellow"])

        else:
            for player in self.players:
                if player.blackjack():
                    player.blackjack_clearing()
                    self.screen.print_string(player.name + " BlackJack!\n", self.screen.COLORS["red"], waittime=2)
                    self.screen.print_string(player.print_token(), self.screen.COLORS["yellow"])

    def play(self):
        first = True
        while any([(not p.standing) and p.playing for p in self.players]):

            if first:
                self.screen.print_string("Now the action starts!\n"
                                         + "(Use up and down keys to choose an action, then hit ENTER to confirm)\n\n",
                                         self.screen.COLORS["cyan"], waittime=2)
                first = False

            for player in self.players:
                if player.playing and not player.standing:
                    self.screen.print_string(player.name + ", please choose your action.\n", self.screen.COLORS[
                        "green"])
                    x = self.screen.menu_from_list(list(player.valid_actions().keys()))

                    player.take_action(x)
                    self.screen.print_string(player.name + " choose to " + x + "\n\n", self.screen.COLORS["green"])

                    if x == "split" or x == "double down":
                        self.screen.print_string(player.print_bet(), self.screen.COLORS["green"])

                    self.screen.print_string(player.print_hand(), waittime=2)
                    if len(player.hand2) > 0:
                        self.screen.print_string(player.print_hand2())

                    if player.busted():
                        self.screen.print_string(player.name + " is busted!\n", self.screen.COLORS["red"])
                        self.screen.print_string(player.print_token(), self.screen.COLORS["yellow"])
                        player.playing = False

    def dealer_round(self):
        if any([p.playing for p in self.players]):
            self.screen.print_string("Now it's the dealer's turn!\n\n", self.screen.COLORS["cyan"])
            self.screen.print_string("The dealer reveals his hand\n", self.screen.COLORS["cyan"])

            self.screen.print_string(self.dealer.hand_reveal(), waittime=2)

            while self.dealer.get_score() <= 17 and not self.dealer.busted():
                self.screen.print_string("The dealer is now drawing cards...\n\n", self.screen.COLORS["cyan"])

                self.dealer.hit()
                self.screen.print_string(self.dealer.print_hand(), waittime=2)

                if self.dealer.busted():
                    self.screen.print_string("The dealer is busted!\n\n", self.screen.COLORS["red"])

    def clearing(self):
        if any([p.playing for p in self.players]):
            for player in self.players:
                if player.playing:
                    self.screen.print_string(player.final_check(self.dealer.get_score()), self.screen.COLORS["red"])
                    self.screen.print_string(player.print_token(), self.screen.COLORS["yellow"])

    def round_over(self):
        self.screen.print_string("\n\nRound over! Press ENTER to continue to next round!\n\n\n\n\n",
                                 self.screen.COLORS["cyan"])
        self.screen.wait_for_enter()

    def game(self):
        self.new_game()
        self.place_bets()
        self.get_initial_two_cards()
        self.play()
        self.dealer_round()
        self.clearing()
        self.round_over()

    def keep_gaming(self):
        while any([p.tokens > 0 for p in self.players]):
            self.game()
            self.screen.clear_screen()
        self.screen.print_string("Game Over!\n", self.screen.COLORS["red"])

