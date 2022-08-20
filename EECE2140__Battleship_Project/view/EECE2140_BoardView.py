from tkinter import *
import controller.EECE2140_GameController as gc

class BoardView:
    """represents the board view
    """

    def __init__(self, scoreboard, tki):
        """initalizes the board view

        Args:
            scoreboard (ScoreBoard): the score board
            tki (TKInterface): the tkinter interface
        """

        self.scoreboard = scoreboard
        self.tki = tki

    def display_board(self, player, hit_spaces: list = [], guessed_spaces: list = []):
        """displays a board

        Args:
            player (Player): which player's board is being displayed
            hit_spaces (list, optional): spaces hit by that player. Defaults to [].
            guessed_spaces (list, optional): spaces guessed byt a miss by that player. Defaults to [].
        """

        self.tki.printScore(self.scoreboard)
        self.tki.set_up_board(player, hit_spaces, guessed_spaces)