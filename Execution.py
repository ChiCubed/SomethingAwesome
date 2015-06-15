"""
Game about Computers.

Player art:
http://opengameart.org/content/side-scroller-sprite-base-animation
"""

import pygame
import sys

from Game import Game
from Level import Level
from Player import Player
from Platform import *
from helpers import *

def main():
    game = Game()
    game.runGame()

if __name__ == '__main__':
    main()
