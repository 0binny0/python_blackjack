

from classes import Player, Dealer
from exceptions import BetError
from functools import reduce
from copy import deepcopy

def game(player, dealer):
    if player.hands:
        player.hands = []
        dealer.hand = None
    try:
        bet = player.bet()
    except BetError as e:
        print(e)
    else:
        player_hand, dealer_hand = dealer.deal(initial_hand=True)
        player.collect_hand(player_hand)
        dealer.hand = dealer_hand
        i = 0
        while i < len(player.hands):
            player_move = player.check_hand(player.hands[i])
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
                for i in range(2):
                    player.collect_hand(Hand([
                        player_cards[i], dealt_cards[i]
                    ]))
            elif player_move == "HIT":
                card = dealer.deal(player_move)
                player.hands[0].append(card)
            else:
                player.hands[i].bust = True
                i += 1
        final_player_hands = list(filter(
            lambda hand: not hand.bust, player.hands
        ))
        if not final_player_hands:
            winner = dealer
        else:
            dealer_hand = dealer.check_hand()
            if dealer_hand.value > 21:
                player.chips += bet * len(final_player_hands)
            else:
                i = 0
                while i < len(final_player_hands):
                    player_hand = final_player_hands[i]
                    if player_hand < dealer_hand:
                        player.hands.pop(0)
                    i += 1
                if player.hands:
                    winner = player
                    winner.chips += (player.placed_bet * len(player.hands))
                else:
                    winner = dealer
            collected_game_cards = (
                [hand.cards for hand in player.hands] + [dealer.hand.cards]
            )
            dealer.cards += collected_game_cards
            player.placed_bet = 0
        return winner

# def main():
#     player = Player()
#     dealer = Dealer()
#     while True:
#         winner = game(player, dealer)
#         print(f"** Winner: {winner}  **\nWinning hand(s):\n")
#         if winner is player:
#             hands = reduce(
#                 lambda string, hand: string += f"""
#                 ===============
#                 {hand}
#                 ===============
#                 """, winner.hands, ""
#             )
#         else:
#             hands = f"""
#                 ===============
#                 {winner.hand}
#                 ===============
#             """
#         print(hands)
#         while True:
#             play_again = input(
#                 "Would you like to play another round of Blackjack?\n>>> "
#             ).upper()
#             if play_again not in ["Y", "N"]:
#                 print("To continue (or not) press Y(es) or N(o)...")
#             else:
#                 if play_again == "N":
#                     print("Goodbye!")


if __name__ == "__main__":
    main()
