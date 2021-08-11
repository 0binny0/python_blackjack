
from unittest import TestCase, main
from unittest.mock import patch, Mock, MagicMock

import classes

import exceptions

class TestBlackjackFaceCard(TestCase):
    '''Verify that Jack, Queen, and King face cards
    are assigned a value of 10. Ace cards are assigned
    a value of 11.'''

    def setUp(self):
        self.face_cards = [
            ('Spades', 'Jack'), ('Diamond', 'Queen'), ('Clubs', 'King')
        ]
        self.ace_card = ('Spade', 'Ace')

        self.face_card = classes.Card("Hearts", "Ace")

    def test_face_card_value(self):
        for card_value in self.face_cards:
            with self.subTest(card_value=card_value):
                suit, value = card_value
                card = classes.Card(suit, value)
                self.assertIsInstance(card, classes.Card)
                self.assertEqual(card.pip, 10)

    def test_ace_face_card_value(self):
        suit, value = self.ace_card
        card = classes.Card(suit, value)
        self.assertIsInstance(card, classes.Card)
        self.assertEqual(card.pip, 11)

    def test_face_card_string(self):
        self.assertEqual(str(self.face_card), "Ace of Hearts")

    def test_face_card_repr_string(self):
        self.assertEqual(repr(self.face_card), "Card(Hearts, Ace)")


class TestBlackjackHandStrings(TestCase):
    '''Verify that a blackjack hand has a str and repr string'''

    def setUp(self):
        self.hand1 = classes.Hand(
            [classes.Card("Hearts", 'Jack'), classes.Card("Hearts", "Queen")]
        )
        self.hand2 = classes.Hand([
            classes.Card("Clubs", 2), classes.Card("Diamonds", 9),
            classes.Card("Clubs", 5)
        ])
        self.hand3 = classes.Hand([
            classes.Card("Hearts", "Jack"), classes.Card("Hearts", 4)
        ])

    def test_blackjack_hand_string(self):

        self.assertEqual(
            str(self.hand1),
            "Jack of Hearts\nQueen of Hearts"
        )
        self.assertEqual(
            str(self.hand2),
            "2 of Clubs\n9 of Diamonds\n5 of Clubs"
        )

    def test_blackjack_hand_repr_string(self):
        self.assertEqual(
            repr(self.hand2),
            "Hand([Card(Clubs, 2), Card(Diamonds, 9), Card(Clubs, 5)])"
        )
        self.assertEqual(
            repr(self.hand3),
            "Hand([Card(Hearts, Jack), Card(Hearts, 4)])"
        )


class TestBlackjackSoftHandValue(TestCase):
    '''Verify that the value of a soft blackjack hand is reduced
    to prevent the hand from exceeding 21.'''

    def setUp(self):
        self.hand1 = classes.Hand([
            classes.Card("Clubs", "Ace"), classes.Card("Diamonds", "Ace"),
            classes.Card("Hearts", "Ace"), classes.Card("Spades", "Ace"),
            classes.Card("Clubs", "Ace"), classes.Card("Diamonds", "Ace"),
            classes.Card("Hearts", "Ace"), classes.Card("Spades", "Ace"),
            classes.Card("Clubs", "Ace"), classes.Card("Diamonds", "Ace"),
            classes.Card("Hearts", "Ace"), classes.Card("Spades", "Ace"),
            classes.Card("Clubs", "Ace"), classes.Card("Diamonds", "Ace"),
            classes.Card("Hearts", "Ace"), classes.Card("Spades", "Ace"),
            classes.Card("Clubs", "Ace"), classes.Card("Diamonds", "Ace"),
            classes.Card("Hearts", "Ace"), classes.Card("Spades", "Ace"),
            classes.Card("Hearts", "Ace"), classes.Card("Spades", "Ace")
        ])

        self.hand2 = classes.Hand([
            classes.Card("Hearts", 10), classes.Card("Hearts", 6),
            classes.Card("Hearts", "Ace"), classes.Card("Clubs", "Ace")
        ])

        self.hand3 = classes.Hand([
            classes.Card("Diamonds", 'Ace'), classes.Card("Spades", 2)
        ])

        self.hand_values = [22, 18, 13]

    def test_soft_player_hands(self):
        for i, hand in enumerate([self.hand1, self.hand2, self.hand3]):
            with self.subTest(hand=hand, i=i):
                self.assertEqual(hand.value, self.hand_values[i])


class TestBlackjackHandComparisonOperators(TestCase):
    '''Verify that one blackjack hand can be compared with another
    blackjack hand.'''

    def setUp(self):
        self.hand1 = classes.Hand(
            [classes.Card("Clubs", 10), classes.Card("Hearts", 4)]
        )
        self.hand2 = classes.Hand(
            [classes.Card("Diamonds", "Ace"), classes.Card("Clubs", "Ace")]
        )

        self.hand3 = classes.Hand(
            [classes.Card("Diamonds", 9), classes.Card("Clubs", 3)]
        )

    def test_blackjack_hand_greater_than(self):
        self.assertTrue(self.hand1 > self.hand2)

    def test_blackjack_hands_equal(self):
        self.assertTrue(self.hand2 == self.hand3)

class TestPlayerBetInitialHandNoChips(TestCase):
    '''Verify that if a player has yet to be dealt a hand and
    has chips less than the minimum bet required
    that they cannot play a round of blackjack'''

    def setUp(self):
        self.player = classes.Player()
        self.player.chips = 5

    def test_player_bet_attempt_no_chips(self):
        with self.assertRaises(exceptions.BetError) as error:
            self.player.bet()
            self.assertEqual(
                error.msg,
                "Player has no chips to bet with...GAME OVER"
            )

class TestPlayerInvalidInitialBet(TestCase):
    '''Verify that a player bet placed below the minimum bet required
    or greater than their total chip stack is not allowed.'''

    def setUp(self):
        self.player = classes.Player()
        self.player.chips = 45

    @patch("classes.print")
    @patch("classes.input", side_effect=['9', '60', '15'])
    def test_player_bet(self, mock_bet, mock_msg):
        bet = self.player.bet()
        self.assertEqual(mock_bet.call_count, 3)
        self.assertEqual(bet, 15)


class TestPlayerAdditionalBet(TestCase):
    '''Verify that a player cannot bet a second bet if their
    initial bet is greater than their current chip stack.'''

    def setUp(self):
        self.player = classes.Player()
        self.player.hands = [classes.Hand([
            classes.Card("Spades", 2), classes.Card("Hearts", 'King')
        ])]
        self.player.placed_bet = 40
        self.player.chips = 25

    def test_player_bet_exceeds_chip_amount(self):
        with self.assertRaises(exceptions.BetError) as error:
            self.player.bet()
            self.assertEqual(
                error.msg,
                "Bet placed is greate than chip stack...bet disallowed"
            )


class TestPlayerMoveSplitHandPass(TestCase):
    '''Verify that a player can split their hand if their
    cards are of the same value (pip/face card), they have enough
    chips and have yet to split their hand yet.'''

    def setUp(self):
        self.player = classes.Player()
        self.player.chips = 60
        self.player.placed_bet = 30
        self.player.hands = [classes.Hand([
            classes.Card("Clubs", "Ace"), classes.Card("Diamonds", "Ace")
        ])]
        self.hand = self.player.hands[0]

    @patch("classes.print")
    @patch("classes.input", return_value="SPLIT")
    def test_player_move_split_hand(self, mock_play, mock_msg):
        move = self.player.check_hand(self.hand)
        self.assertEqual(move, "SPLIT")
        self.assertEqual(self.player.placed_bet, 60)
        self.assertEqual(self.player.chips, 30)


class TestPlayerMoveDoubleDownHand(TestCase):
    '''Verify that a player can double down on a hand if the
    hand only has two cards.'''

    def setUp(self):
        self.player = classes.Player()
        self.player.chips = 55
        self.player.placed_bet = 15
        self.player.hands = [classes.Hand([
            classes.Card("Diamonds", "King"), classes.Card("Diamonds", 3)
        ])]
        self.hand = self.player.hands[0]

    @patch("classes.print")
    @patch("classes.input", return_value="DOUBLE DOWN")
    def test_player_move_double_down(self, mock_input, mock_msg):
        move = self.player.check_hand(self.hand)
        self.assertEqual(move, "DOUBLE DOWN")
        self.assertEqual(self.player.placed_bet, 30)
        self.assertEqual(self.player.chips, 40)


class TestPlayMoveSplitHandInvalidBet(TestCase):
    '''Verify that a player must check consider a different move if they
    want to split their hand but don't have enough chips.'''

    def setUp(self):
        self.player = classes.Player()
        self.player.chips = 45
        self.player.placed_bet = 50
        self.player.hands = [classes.Hand([
            classes.Card("Clubs", 4), classes.Card("Hearts", 4)
        ])]
        self.hand = self.player.hands[0]

    @patch("classes.print")
    @patch("classes.input", side_effect=["SPLIT", "HIT"])
    def test_player_move_split_low_chips(self, mock_input, mock_msg):
        move = self.player.check_hand(self.hand)
        self.assertEqual(mock_input.call_count, 2)
        self.assertEqual(move, "HIT")
        self.assertEqual(self.player.chips, 45)
        self.assertEqual(self.player.placed_bet, 50)


class TestPlayMoveHandBust(TestCase):
    '''Verify that a player cannot make any more plays on their hand
    if the value of the hand is greater than 21.'''

    def setUp(self):
        self.player = classes.Player()
        self.player.chips = 45
        self.player.placed_bet = 50
        self.player.hands = [classes.Hand([
            classes.Card("Hearts", 10), classes.Card("Hearts", 4),
            classes.Card("Diamonds", 9)
        ])]
        self.hand = self.player.hands[0]

    @patch("classes.print")
    def test_player_move_bust(self, mock_msg):
        move = self.player.check_hand(self.hand)
        self.assertEqual(move, "BUST")


if __name__ == "__main__":
    main()
