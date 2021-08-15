
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

import classes
import main

class TestBlackjackGamePlayerStand(TestCase):
    '''Verify that a player is rewarded double the amount of
    chips based on their placed bet if their hand beats
    the dealer\'s hand.'''

    def setUp(self):
        self.player = classes.Player()
        self.dealer = classes.Dealer()
        hands = [classes.Hand([
            classes.Card("Spades", "King"), classes.Card("Diamonds", "Queen")
        ]), classes.Hand([
            classes.Card("Hearts", 9), classes.Card("Hearts", 9)
        ])]
        player_patch1 = patch.object(self.player, 'bet', return_value=20)
        dealer_patch1 = patch.object(
            self.dealer, 'deal', return_value=hands
        )
        mock_player_bet = player_patch1.start()
        mock_dealer_deal = dealer_patch1.start()
        self.addCleanup(player_patch1.stop)
        self.addCleanup(dealer_patch1.stop)

    @patch("classes.print")
    @patch('classes.input', return_value="STAND")
    def test_player_hand_beats_dealer_hand(self, mock_player_move, mock_print):
        winner = main.game(self.player, self.dealer)
        self.assertIsInstance(winner, classes.Player)
        self.assertEqual(winner.hands[0].value, 20)
        self.assertEqual(winner.chips, 70)
