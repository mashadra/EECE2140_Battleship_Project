import model.EECE2140_Player as pl
import model.EECE2140_HumanPlayer as hp
import model.EECE2140_ComputerPlayer as cp
import controller.EECE2140_GameController as gc

class Scoreboard:
    """represents a score board which holds main fucntionality and players
    """

    def __init__(self, gamecontroller, leader: str = "No one", players: list[pl.Player] = [], size: int = 10):
        """_summary_

        Args:
            gamecontroller (gc.GameController): the gamecontroller used
            leader (str, optional): who has sunkt he most ships. Defaults to "No one".
            players (list[pl.Player], optional): players. Defaults to [].
            size (int, optional): size of the board. Defaults to 10.
        """

        self.leader = leader
        self.players = players
        self.size = size
        self.gamecontroller = gamecontroller

    def begin_game_with_comp(self):
        """begins a game by showing messages and setting up 1 human player and 1 computer player
        """

        self.gamecontroller.show_setup_message(1)
        self.add_player(self.gamecontroller.get_name())
        self.add_computer_player()
    
    def add_player(self, name: str):
        """adds a player

        Args:
            name (str): the player's name
        """

        # has the player get set up through outher functions
        player = hp.HumanPlayer(self.gamecontroller)
        player.set_player(self.size, name)
        self.players.append(player)

    def add_computer_player(self):
        """add a computer player
        """

        # has the computer player get set up through outher functions
        player = cp.ComputerPlayer(self.gamecontroller)
        player.set_player(self.size, "Computer")
        self.players.append(player)

    def check_gameover(self) -> bool:
        """checks if either player has all 5 ships sunk

        Returns:
            bool: True if game is over
        """

        if self.players[0].is_fully_sunk():
            self.leader = self.players[1].get_name()
            return True
        if self.players[1].is_fully_sunk():
            self.leader = self.players[0].get_name()
            return True
        return False

    def play_turn(self, turn_num: int):
        """plays a single turn

        Args:
            turn_num (int): the number turn it's one
        """

        # on even turns (turns start with 0) human plays
        base = turn_num%2
        base2 = (turn_num+1)%2
        if self.players[base].get_name() != "Computer":
            self.gamecontroller.show_player_turn(self.players[base].get_name(), str(self), self.players[base].get_hits(), self.players[base].get_misses(), self.players[base2].get_hits(), self.players[base2].get_misses())
        self.players[base].make_guess(self.players[base2])
        self.update_winner()

    def update_winner(self):
        """updates the leader to reflect who has sunk the most boats
        """

        player0_sunk = self.players[0].number_of_sunk() 
        player1_sunk = self.players[1].number_of_sunk() 
        if player0_sunk > player1_sunk:
            self.leader = self.players[1].get_name()
        elif player0_sunk < player1_sunk:
            self.leader = self.players[0].get_name()
        else:
            self.leader = "No one"

    def __str__(self) -> str:
        """string prepresntation of the current score

        Returns:
            str: string representation of the score
        """

        s0 = ", ".join(self.players[0].get_sunk_ships())
        if s0 == "":
            s0 = "nothing"
        s1 = ", ".join(self.players[1].get_sunk_ships())
        if s1 == "":
            s1 = "nothing"
        return(f"{self.leader} is winning\n{self.players[0].get_name()}'s {s0} is/are sunk\n{self.players[1].get_name()}'s {s1} is/are sunk")

    def get_size(self) -> int:
        """getter for size

        Returns:
            int: self.size
        """

        return self.size