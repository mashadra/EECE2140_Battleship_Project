import tkinter as tk

class Board:
    """represents the image of the board with all the squares
    """

    def __init__(self, size: int, sq_wid: int):
        """initializes a board

        Args:
            size (int): side length
            sq_wid (int): width of each square
        """

        self.game_window = tk.Tk()
        self.game_window.title("Battleship Board")
        self.sq_wid = sq_wid
        self.size = size

        for i in range(size):
            for j in range(size):
                tk.Canvas(self.game_window, width = sq_wid, height = sq_wid, bg = 'white', highlightthickness=1, highlightbackground="black").grid(row = i, column = j)


    def update_board(self, player, hit_spaces: list = [], guessed_spaces: list = []):    
        """updates the board image to make hits red, missed guesses grey, and the rest white

        Args:
            player (str): name of the player
            hit_spaces (list, optional): the spaces to turn red because they have been hit. Defaults to [].
            guessed_spaces (list, optional): the spaces to turn grey because they have been a miss. Defaults to [].
        """


        self.game_window.title(f"Battleship Board: {player}'s guesses")  
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) in hit_spaces:
                    color = "red"
                elif (i, j) in guessed_spaces:
                    color = "grey"
                else:
                    color = "white"
                tk.Canvas(self.game_window, width = self.sq_wid, height = self.sq_wid, bg = color, highlightthickness=1, highlightbackground="black").grid(row = i, column = j)