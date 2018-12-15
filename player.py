from deck import Card


class PlayerBase:
    def __init__(self, name):
        self.deck = None
        self.hand = []
        self.name = name

    def get_initial_two(self):
        self.hand += self.deck.deal(2)

    def hit(self):
        self.hand += self.deck.deal(1)

    def blackjack(self):
        return self.get_score() == 21 and len(self.hand) == 2

    def busted(self):
        return self.get_score() > 21

    def get_score(self):
        return self.get_score_helper(self.hand)

    @staticmethod
    def get_score_helper(hand):
        s = 0
        num_ace = 0
        for card in hand:
            s += card.get_score()
            if card.get_score() == 1:
                num_ace += 1
        while s <= 11 and num_ace > 0:
            s += 10
            num_ace -= 1
        return s

    def print_hand(self):
        return self.print_hand_helper(self.name, self.hand, "hand", self.get_score())

    @staticmethod
    def print_hand_helper(name, hand, handname, score):
        s = name + "'s " + handname + " is now:\n"
        lines = Card.print_list_of_full_cards(hand)
        for line in lines:
            s += line + "\n"
        s += "The score of this hand is " + str(score) + "\n\n"
        return s


class Dealer(PlayerBase):

    def __init__(self):
        PlayerBase.__init__(self, "The dealer")

    def start_game(self, deck):
        self.deck = deck
        self.hand = []

    def hand_reveal(self):
        return PlayerBase.print_hand(self)

    def print_hand(self):
        if len(self.hand) == 2 and not self.blackjack():
            s = "The dealer's hand is now:\n"
            lines = [self.hand[0].print_card_full()[i] + " " + Card.print_card_back()[i] for i in range(5)]
            for line in lines:
                s += line + "\n"
            s += "\n"
            return s
        else:
            return PlayerBase.print_hand(self)


class Player(PlayerBase):

    def __init__(self, name):
        PlayerBase.__init__(self, name)
        self.tokens = 1000
        self.betting = 0
        self.hand2 = []
        self.standing = False
        self.playing = True

    def start_game(self, deck):
        self.standing = False
        self.playing = True
        self.deck = deck
        self.hand = []
        self.hand2 = []
        if self.tokens <= 0:
            self.playing = False

    def place_bet(self, bet):
        self.betting = bet
        self.tokens -= bet

    def stand(self):
        self.standing = True

    def double_down(self):
        self.tokens -= self.betting
        self.betting *= 2
        self.hit()
        self.stand()
        self.print_bet()

    def split(self):
        self.tokens -= self.betting
        self.betting *= 2
        self.hand2 = self.hand[:1]
        self.hand = self.hand[1:]
        self.hit()
        self.hand2 += self.deck.deal(1)
        self.stand()
        self.print_hand2()

    def valid_actions(self):
        if self.standing:
            return {}
        actions = {"hit": self.hit, "stand": self.stand}
        if self.tokens > self.betting:
            actions["double down"] = self.double_down
        if len(self.hand) == 2 and self.hand[0].equals(self.hand[1]):
            actions["split"] = self.split
        return actions

    def take_action(self, action):
        actions = self.valid_actions()
        if action in actions:
            actions[action]()

    def print_bet(self):
        return self.name + " is currently betting " + str(self.betting) + "\n\n"

    def print_token(self):
        return self.name + " now has " + str(self.tokens) + " dollars\n"

    def print_hand2(self):
        return self.print_hand_helper(self.name, self.hand2, "second hand", self.get_score_helper(self.hand2))

    def blackjack_clearing(self):
        self.tokens += int(self.betting * 2.5)
        self.playing = False

    def final_check(self, dealer_score):
        s = ""
        if len(self.hand2) == 0:
            if dealer_score > 21 or self.get_score() > dealer_score:
                s = self.name + " wins!"
                self.tokens += self.betting * 2
            elif self.get_score() == dealer_score:
                s = self.name + " gets a draw!"
                self.tokens += self.betting
            else:
                s = self.name + " loses!"
        else:
            if dealer_score > 21 or self.get_score() > dealer_score:
                s += self.name + "'s first hand wins!\n"
                self.tokens += self.betting
            elif self.get_score() == dealer_score:
                s += self.name + "'s first hand gets a draw!\n"
                self.tokens += self.betting / 2
            else:
                s += self.name + "'s first hand loses!\n"
            if dealer_score > 21 or self.get_score_helper(self.hand2) > dealer_score:
                s += self.name + "'s second hand wins!"
                self.tokens += self.betting
            elif self.get_score() == dealer_score:
                s += self.name + "'s second hand gets a draw!"
                self.tokens += self.betting / 2
            else:
                s += self.name + "'s second hand loses!"
        return s + "\n"



