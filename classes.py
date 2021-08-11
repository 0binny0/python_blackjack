
from exceptions import BetError

import re
from functools import reduce
from textwrap import dedent

class Card:

    def __init__(self, suit, value):
        self.suit = suit
        if value not in ['Jack', 'Queen', 'King', 'Ace']:
            self.pip = value
        else:
            setattr(self, 'face_card', value)
            self.pip = 11 if self.face_card == "Ace" else 10

    def __str__(self):
        if hasattr(self, 'face_card'):
            return f"{self.face_card} of {self.suit}"
        return f"{self.pip} of {self.suit}"

    def __repr__(self):
        if hasattr(self, 'face_card'):
            return f"{self.__class__.__name__}({self.suit}, {self.face_card})"
        return f"{self.__class__.__name__}({self.suit}, {self.pip})"

    def __eq__(self, other):
        return self.pip == other.pip


class Hand:

    def __init__(self, cards):
        self.cards = cards
        self.bust = False
        self.soft = False
        self.split = False
        self.double_down = False

    @property
    def value(self):
        _value = sum(card.pip for card in self.cards)
        if _value > 21:
            total_aces = filter(
                lambda i: (
                    hasattr(self.cards[i], 'face_card')
                    and self.cards[i].face_card == "Ace"
                ), range(len(self.cards)))
            for ace_index in total_aces:
                self.cards[ace_index].pip = 1
                _value = sum(card.pip for card in self.cards)
                if _value < 21:
                    return _value
        return _value

    def __str__(self):
        return reduce(lambda y, z: f"{y}\n{z}", self.cards)

    def __repr__(self):
        cls = f"{self.__class__.__name__}(["
        cls += ", ".join(
            f"Card({card.suit}, {card.face_card})"
            if hasattr(card, 'face_card')
            else f"Card({card.suit}, {card.pip})"
            for card in self.cards
        )
        return f"{cls}])"

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __len__(self):
        return len(self.cards)


class Player:

    def __init__(self):
        self.hands = []
        self.chips = 50
        self.placed_bet = 0

    def bet(self):
        if self.chips < 10 and not self.hands:
            raise BetError(
                "Player cannot meet minimum bet requirement...GAME OVER"
            )
        elif self.chips >= 10 and not self.hands:
            while True:
                placed_bet = input(
                    "Minimum bet required to play round is 10 chips\n>>> "
                )
                matched_bet = re.match(r"^\d{2}(?!\D+)$", placed_bet)
                if matched_bet:
                    placed_bet = int(matched_bet.group())
                    if placed_bet >= 10 and placed_bet <= self.chips:
                        self.chips -= placed_bet
                        self.placed_bet = placed_bet
                        return self.placed_bet
                print("Invalid bet by player...")
                continue
        second_bet = self.chips - self.placed_bet
        if second_bet < 0:
            raise BetError(
                "Bet placed is greater than chip stack...bet not allowed"
            )
        self.chips -= self.placed_bet
        self.placed_bet *= 2
        return self.placed_bet

    def check_hand(self, hand):
        if all(card.pip != 11 for card in hand.cards) and hand.value > 21:
            return "BUST"
        while True:
            print(dedent('''
                BLACKJACK OPTIONS:
                    * Hit - Request another card from the dealer
                    * Stand - Play your hand against the dealer as is
                    * Split - Split your hand if your cards are of the same pip/face card
                    * Double Down - Request another card and play your and against the dealer as is
            '''))
            while True:
                player_move = input(
                    "How would you like to play your hand...\n>>> "
                )
                matched_move = re.match(
                    r"HIT|SPLIT|STAND|DOUBLE DOWN", player_move
                )
                if matched_move:
                    if player_move == "SPLIT":
                        if len(self.hands) == 1:
                            if hand.cards[0] == hand.cards[1]:
                                try:
                                    self.bet()
                                    return player_move
                                except BetError as e:
                                    print(e)
                                    break
                            else:
                                print("Cards can only be split if they are of the same pip/face card")
                                break
                        else:
                            print("Only your initial hand can be split... move not allowed")
                            break
                    elif player_move == "DOUBLE DOWN":
                        if len(hand) == 2 and not hand.double_down:
                            try:
                                self.bet()
                                hand.double_down = True
                                return player_move
                            except BetError as e:
                                print(e)
                                break
                    else:
                        return player_move
