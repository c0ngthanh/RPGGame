# -*- coding: utf-8 -*-

"""
Whack a Mole
~~~~~~~~~~~~~~~~~~~
A simple Whack a Mole game written with PyGame
:copyright: (c) 2018 Matt Cowley (IPv4)
"""

from filegame import Game

g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
