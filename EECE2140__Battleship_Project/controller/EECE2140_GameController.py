import model.EECE2140_Scoreboard as s
import view.EECE2140_PlayerView as pv
import view.EECE2140_BoardView as bv
import view.EECE2140_tkinterface as tk

class GameController:
    """Represents a game controller which connects the user input/output interface with the functionality of classes
    """

    def __init__(self):
        """Initalizes a game controller with the top of the functional class hierarchy and all of the input/output interfaces
        """

        self.scoreboard = s.Scoreboard(self)
        self.tki = tk.TKInterface(self.scoreboard.get_size())
        self.board = bv.BoardView(self.scoreboard, self.tki)
        self.playerview = pv.PlayerView(self.tki)

    def play(self):
        """Runs a whole game
        """

        # beginning game
        self.scoreboard.begin_game_with_comp()
        count = 0
        
        # playing until someone wins
        while not self.scoreboard.check_gameover():
            self.scoreboard.play_turn(count)
            count += 1
        self.tki.end_game()

    def show_setup_message(self, num: int):
        """Has the player interface show a setup message

        Args:
            num (int): the player who is being set up (1 or 2)
        """

        self.playerview.show_setup_message(num)

    def get_name(self) -> str:
        """Gets a player's name using the player I/O interface

        Returns:
            str: the name given in the player I/O interface
        """

        return self.playerview.get_name()

    def show_ship_placing(self, name: str, leng: int):
        """shows a message for placing the ship

        Args:
            name (str): the name of the ship being placed
            leng (int): the length of the ship being placed
        """

        self.playerview.show_ship_placing(name, leng)

    def get_coord(self) -> tuple:
        """gets a coordinate from the user

        Returns:
            tuple: the point inputted in (x, y) format
        """

        return self.playerview.get_coord()

    def get_dir(self, valid_directions: str) -> str:
        """gets a direction from the user

        Args:
            valid_directions (str): a list of directions the user can choose from (can include "right", "left", "up", and/or, "down")

        Returns:
            string: the direction inputted
        """

        return self.playerview.get_dir(valid_directions)

    def show_player_turn(self, name, message, hit_points: list = [], guessed_points: list = [], comp_hit_spaces: list = [], comp_guessed_spaces: list = []):
        """shows a player what to do throughout their turn

        Args:
            name (str): the name of the player whose turn it is
            message (str): a string representation of the current score
            hit_points (list, optional): points that the current player has correctly guessed. Defaults to [].
            guessed_points (list, optional): points that the current player has guess but not hit anything with. Defaults to [].
        """

        self.tki.set_up_board(name, message, hit_points, guessed_points, comp_hit_spaces, comp_guessed_spaces)
        self.playerview.show_player_turn(name)

    def tell_ship_sunk(self, name: str, computer: bool = False):
        """tells if a ship is sunk

        Args:
            name (str): name of the ship
            computer (bool, optional): True if the computer has sunk the ship. Defaults to False.
        """

        self.playerview.tell_ship_sunk(name, computer)

    def tell_ship_hit(self, name: str, computer: bool = False):
        """tells if a ship is hit

        Args:
            name (str): name of the ship
            computer (bool, optional): True if the computer has hit the ship. Defaults to False.
        """

        self.playerview.tell_ship_hit(name, computer)

    def tell_miss(self, computer: bool = False):
        """tells if a ship is missed

        Args:
            name (str): name of the ship
            computer (bool, optional): True if the computer has missed the ship. Defaults to False.
        """

        self.playerview.tell_miss(computer)