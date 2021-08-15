
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

import classes
import main

class TestBlackjackGamePlayerStandWin(TestCase):
    '''Verify that a player is rewarded double the amount of
    chips based on their placed bet if their hand beats
    the dealer\'s hand.'''

    def setUp(self):
        self.player = classes.Player()
        self.player.placed_bet = 20
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
        self.assertTrue(winner is self.player)
        self.assertEqual(winner.hands[0].value, 20)
        self.assertEqual(winner.chips, 70)


class TestBlackjackGamePlayerStandLose(TestCase):
    '''Verify that a player loses chips when they stand on a hand
    and the hand value is less than the dealer hand.'''

    def setUp(self):
        self.player = classes.Player()
        self.player.chips -= 20
        self.player.placed_bet = 20
        self.dealer = classes.Dealer()
        hands = [classes.Hand([
            classes.Card("Spades", 4), classes.Card("Diamonds", 10)
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
        self.assertIsInstance(winner, classes.Dealer)
        self.assertTrue(winner is self.dealer)
        self.assertEqual(winner.hand.value, 18)
        self.assertEqual(self.player.chips, 30)


class TestBlackjackGamePlayerDoubleDownLose(TestCase):
    '''Verify that a player loses a game of Blackjack when they double down
    on their hand and is still less than the dealer\'s hand.'''

    def setUp(self):
        self.player = classes.Player()
        self.player.chips = 30
        self.player.placed_bet = 20
        self.dealer = classes.Dealer()
        hands = [classes.Hand([
            classes.Card("Spades", 3), classes.Card("Diamonds", 8)
        ]), classes.Hand([
            classes.Card("Hearts", 9), classes.Card("Hearts", 9)
        ])]
        player_patch1 = patch.object(self.player, 'bet', return_value=20)
        dealer_patch1 = patch.object(
            self.dealer, 'deal', side_effect=[
                hands, classes.Card("Hearts", 5)
            ]
        )
        mock_player_bet = player_patch1.start()
        mock_dealer_deal = dealer_patch1.start()
        self.addCleanup(player_patch1.stop)
        self.addCleanup(dealer_patch1.stop)

    @patch("classes.print")
    @patch('classes.input', return_value="DOUBLE DOWN")
    def test_player_hand_beats_dealer_hand(self, mock_player_move, mock_print):
        winner = main.game(self.player, self.dealer)
        self.assertIsInstance(winner, classes.Dealer)
        self.assertTrue(winner is self.dealer)
        self.assertEqual(winner.hand.value, 18)
        self.assertEqual(self.player.chips, 30)


class TestBlackjackGamePlayerDoubleDownWin(TestCase):
    '''Verify that a player loses a game of Blackjack when they double down
    on their hand and is still less than the dealer\'s hand.'''

    def setUp(self):
        self.player = classes.Player()
        self.player.chips = 30
        self.player.placed_bet = 40
        self.dealer = classes.Dealer()
        hands = [classes.Hand([
            classes.Card("Spades", 10), classes.Card("Diamonds", 8)
        ]), classes.Hand([
            classes.Card("Hearts", 9), classes.Card("Hearts", 9)
        ])]
        player_patch1 = patch.object(self.player, 'bet', side_effect=[
            20, 20
        ])
        dealer_patch1 = patch.object(
            self.dealer, 'deal', side_effect=[
                hands, classes.Card("Hearts", 2)
            ]
        )
        mock_player_bet = player_patch1.start()
        mock_dealer_deal = dealer_patch1.start()
        self.addCleanup(player_patch1.stop)
        self.addCleanup(dealer_patch1.stop)

    @patch("classes.print")
    @patch('classes.input', return_value="DOUBLE DOWN")
    def test_player_hand_beats_dealer_hand(self, mock_player_move, mock_print):
        winner = main.game(self.player, self.dealer)
        self.assertIsInstance(winner, classes.Player)
        self.assertTrue(winner is self.player)
        self.assertEqual(winner.hands[0].value, 20)
        self.assertEqual(self.player.chips, 70)
