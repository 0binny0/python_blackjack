
from unittest import TestCase, main
from unittest.mock import patch, Mock, MagicMock

import classes

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





if __name__ == "__main__":
    main()
