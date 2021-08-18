
import os
from time import sleep


def cls():
    sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')


def show_player_stats(func):
    def wrapper_show_player_stats(player, dealer, *args, **kwargs):
        return func(*args, **kwargs)
    return wrapper_show_player_stats
