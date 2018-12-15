import random
from copy import deepcopy


class Deck:
    def __init__(self, n):
        self.fulldeck = self.one_deck() * n
        self.deck = deepcopy(self.fulldeck)
        self.shuffle()

    def get_deck(self):
        return self.deck

    def shuffle(self):
        random.shuffle(self.deck)

    # pop the first num cards
    def deal(self, num):
        if num < 0:
            raise ValueError('Number of cards has to be positive')
        if num > len(self.deck):
            self.deck = deepcopy(self.fulldeck)
            self.shuffle()
        dealt = self.deck[:num]
        self.deck = self.deck[num + 1:]
        return dealt

    # just a deck of cards
    @staticmethod
    def one_deck():
        deck = []
        for suit in ["Hearts", "Spades", "Clubs", "Diamonds"]:
            for i in range(1, 14):
                deck.append(Card(suit, i))
        return deck


class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def equals(self, card):
        return self.number == card.get_number()

    def get_number(self):
        return self.number

    def get_score(self):
        return self.number if self.number < 11 else 10

    # print card in string format i.e. "2 of Spades"
    def print_card_text(self):
        d = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}
        card = d.setdefault(self.number, str(self.number))
        return card + " of " + self.suit

    # print card in compact format i.e. "♠2"
    def print_card(self):
        symbol = {
            'Spades': '♠',
            'Diamonds': '♦',
            'Hearts': '♥',
            'Clubs': '♣'}
        d = {1: "A", 11: "J", 12: "Q", 13: "K"}
        card = symbol[self.suit] + d.setdefault(self.number, str(self.number))
        return card

    # print card in a custom ascii format
    def print_card_full(self):
        c = self.print_card()
        line3 = "| " + c + " |"
        if self.number == 10:
            line3 = "| " + c + "|"
        card = [" ____ ", "|    |", line3, "|    |", " ---- "]
        return card

    @staticmethod
    # a custom ascii pattern for a card back
    def print_card_back():
        back = [" ____ ", "|####|", "|####|", "|####|", " ---- "]
        return back

    @staticmethod
    # pring a list of cards side by side
    def print_list_of_full_cards(cardslist):
        lines = ["" for x in range(5)]
        for i in range(5):
            for card in cardslist:
                lines[i] += card.print_card_full()[i] + " "
        return lines


