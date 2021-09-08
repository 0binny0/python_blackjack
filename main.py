from functools import reduce
from time import sleep
from sys import exit

from classes import Player, Dealer, Hand
from exceptions import BetError
from helpers import cls


def game(player, dealer):
    try:
        bet = player.bet()
    except BetError as e:
        raise
    else:
        player_hand, dealer_hand = dealer.deal(initial_hand=True)
        player.collect_hand(player_hand)
        dealer.hand = dealer_hand
        i = 0
        while i < len(player.hands):
            player_move = player.check_hand(player.hands[i], dealer.hand)
            if player_move == "STAND":
                i += 1
            elif player_move == "DOUBLE DOWN":
                card = dealer.deal(player_move)
                player.hands[i].cards.append(card)
                if player.hands[i].value > 21:
                    player.hands[i].bust = True
                i += 1
            elif player_move == "SPLIT":
                player_cards = player.hands.pop().cards
                dealt_cards = dealer.deal(player_move)
                for x in range(2):
                    hand = Hand([player_cards[x], dealt_cards[x]])
                    hand.split = True
                    player.collect_hand(hand)
            elif player_move == "HIT":
                card = dealer.deal(player_move)
                player.hands[i].cards.append(card)
            else:
                player.hands[i].bust = True
                i += 1
        final_player_hands = list(filter(
            lambda hand: not hand.bust, player.hands
        ))
        if not final_player_hands:
            dealer.winner = True
            # winner = dealer
        else:
            low_dealer_hand = any(
                dealer.hand < hand for hand in final_player_hands)
            if low_dealer_hand:
                if dealer.hand.value < 17:
                    while dealer.hand.value < 17:
                            dealer_hand = dealer.check_hand()
                            if dealer_hand.value > 21:
                                for hand in player.hands:
                                    hand.win = True
                                player.winner = True
                                # winner = player
                                if player_move in ['DOUBLE DOWN', "SPLIT"]:
                                    player.chips += (2 * (bet * 2))
                                else:
                                    player.chips += (2 * bet)
                                return player, dealer
                                # return winner
            i = 0
            while i < len(final_player_hands):
                player_hand = final_player_hands[i]
                if player_hand >= dealer_hand:
                    player.hands[i].win = True
                i += 1
            won_hands = [hand for hand in player.hands if hand.win]
            if won_hands:
                player.winner = True
                # winner = player
                if player_move in ['DOUBLE DOWN', "SPLIT"]:
                    player.chips += (2 * (bet * 2))
                else:
                    player.chips += (2 * bet)
            else:
                dealer.winner = True
                # winner = dealer
    collected_game_cards = (
        [hand.cards for hand in player.hands] + [dealer.hand.cards]
    )
    dealer.cards += collected_game_cards
    player.placed_bet = 0
    # import pdb; pdb.set_trace()
    return player, dealer


def main():
    cls()
    player = Player()
    dealer = Dealer()
    print("""Welcome to the blackjack table...\n""")
    while True:
        try:
            player, dealer = game(player, dealer)
        except BetError as e:
            print(f"\nPlayer has no remaining chips:\n{e}")
            exit()
            cls()
        cls()
        winner = [
            game_player for game_player in [player, dealer]
            if game_player.winner
        ][0]
        if player.winner:
            print(f"** Winner: {player} **\nPlayed hand(s):")
            hands = reduce(
                lambda string, hand: string + f"""
                {"Player Winning Hand:" if hand.win else "Player Losing Hand:"} {hand.value}
                >>> {hand}
                """ + "\n", player.hands, ""
            )
            hands += f"""
                Dealer Hand:
                >>> {dealer.hand}
            """
        else:
            print(f"** Winner: {dealer} **\nPlayed hand(s):")
            hands = f"""
                Winning Dealer Hand:
                >>> {dealer.hand}

            """
            hands += "\tLosing Player Hand(s)"
            hands += reduce(
                lambda string, hand: string + f"""
                >>> {hand}
                """ + "\n", player.hands, ""
            )
        print(hands)
        while True:
            play_again = input(
                "Would you like to play another round of Blackjack?\n>>> "
            ).upper()
            if play_again not in ["Y", "N"]:
                print("To continue (or not) press Y(es) or N(o)...")
                sleep(1)
            else:
                if play_again == "N":
                    print("Goodbye!")
                    sleep(1)
                    exit()
                player.winner = False
                dealer.winner = False
                player.hands = []
                dealer.hand = None
                break

if __name__ == "__main__":
    main()
