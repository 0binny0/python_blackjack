
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
                self.assertEqual(card.pip_value, 10)

    def test_ace_face_card_value(self):
        suit, value = self.ace_card
        card = classes.Card(suit, value)
        self.assertIsInstance(card, classes.Card)
        self.assertEqual(card.pip_value, 11)

    def test_face_card_string(self):
        self.assertEqual(str(self.face_card), "Ace of Hearts")

    def test_face_card_repr_string(self):
        self.assertEqual(repr(self.face_card), "Card(Hearts, Ace)")


if __name__ == "__main__":
    main()
