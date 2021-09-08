import re

from functools import reduce
from textwrap import dedent
from random import shuffle

from exceptions import BetError
from helpers import cls


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
        case1 = hasattr(self, 'face_card') and not hasattr(other, 'face_card')
        case2 = not hasattr(self, 'face_card') and hasattr(other, 'face_card')
        if case1 or case2:
            raise Exception(
                "Cards can only be split if they are of the same pip/face card"
            )
        face_cards = all(hasattr(card, 'face_card') for card in [self, other])
        if not face_cards:
            if self.pip != other.pip:
                raise Exception(
                    "Split Failed: Cards are not of the same pip value"
                )
            return self.pip == other.pip
        elif face_cards:
            if self.face_card != other.face_card:
                raise Exception(
                    "Split Failed: Cards are not of the same face card"
                )
            return self.face_card == other.face_card


class Hand:

    def __init__(self, cards):
        self.cards = cards
        self.win = False
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
                    (hasattr(self.cards[i], 'face_card') and
                    self.cards[i].face_card == "Ace")
                ), range(len(self.cards)))
            for ace_index in total_aces:
                self.cards[ace_index].pip = 1
                _value = sum(card.pip for card in self.cards)
                if _value < 21:
                    return _value
        return _value

    def __str__(self):
        return reduce(lambda x, y: f"{x},  {y}", self.cards)
        # return reduce(lambda y, z: f"{y}\n{z}", self.cards)

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

    def __ge__(self, other):
        return self.value >= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __len__(self):
        return len(self.cards)


class Player:

    def __init__(self):
        self.hands = []
        self.chips = 50
        self.placed_bet = 0
        self.winner = False

    def __str__(self):
        return "Player"

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
                print("\nInvalid bet by player...")
                continue
        second_bet = self.chips - self.placed_bet
        if second_bet < 0:
            raise BetError(
                "\nBet placed is greater than chip stack...bet not allowed"
            )
        self.chips -= self.placed_bet
        self.placed_bet *= 2
        return self.placed_bet

    def check_hand(self, player_hand, dealer_hand):
        cls()
        if player_hand.value > 21 and all(card.pip != 11 for card in player_hand.cards):
            return "BUST"
        while True:
            print(dedent(f'''
                BLACKJACK OPTIONS:
                    * HIT - Request another card from the dealer
                    * STAND - Play your hand against the dealer as is
                    * SPLIT - Split your hand if your cards are of the same pip/face card
                    * DOUBLE DOWN - Request another card and play your hand against the dealer as is

                Player info: Bet: {self.placed_bet} --- Chips: {self.chips}
                +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                PLAYER: {player_hand} : Hand Value ({player_hand.value})

                DEALER: {dealer_hand} : Hand Value ({dealer_hand.value})
            '''))
            while True:
                player_move = input(
                    "\nHow would you like to play your hand...\n>>> "
                ).upper()
                matched_move = re.match(
                    r"HIT|SPLIT|STAND|DOUBLE DOWN", player_move
                )
                if matched_move:
                    if player_move == "SPLIT":
                        if len(self.hands) == 1:
                            try:
                                player_hand.cards[0] == player_hand.cards[1]
                                try:
                                    self.bet()
                                    return player_move
                                except BetError as e:
                                    print(e)
                                    cls()
                                    break
                            except Exception as e:
                                print(f"\n{e}")
                                cls()
                                break
                        else:
                            print("Only your initial hand can be split... move not allowed")
                            cls()
                            break
                    elif player_move == "DOUBLE DOWN":
                        if len(player_hand) < 3 and not player_hand.double_down:
                            try:
                                self.bet()
                                player_hand.double_down = True
                                return player_move
                            except BetError as e:
                                print(e)
                                cls()
                                break
                        print("\nCannot double down on this hand...")
                        cls()
                        break
                    else:
                        return player_move
                cls()
                break

    def collect_hand(self, hand):
        self.hands.append(hand)


class Dealer:

    def __init__(self):
        self.hand = None
        self.cards = self.shuffle_cards()
        self.winner=False

    def __str__(self):
        return "Dealer"

    def shuffle_cards(self):
        cards = [
            Card(suit, value)
            for _ in range(4)
            for suit in ['Clubs', 'Diamonds', 'Spades', 'Hearts']
            for value in [
                2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace'
            ]
        ]
        shuffle(cards)
        return cards

    def deal(self, player_move=None, initial_hand=False):
        if initial_hand:
            dealt_cards = [self.cards.pop(0) for _ in range(4)]
            dealer_hand = Hand([dealt_cards[1], dealt_cards[3]])
            player_hand = Hand([dealt_cards[0], dealt_cards[2]])
            return (player_hand, dealer_hand)

        if player_move == "HIT" or player_move == "DOUBLE DOWN":
            dealt_cards = self.cards.pop(0)
        elif player_move == "SPLIT":
            dealt_cards = [self.cards.pop(0) for _ in range(2)]
        return dealt_cards

    def check_hand(self):
        card = self.deal(player_move="HIT")
        self.hand.cards.append(card)
        return self.hand
