from abc import abstractmethod
import random
import controller.EECE2140_GameController as gc
import model.EECE2140_Point as p
import model.EECE2140_Ship as s

class Player:
    """represents a player (can be computer or human)
    """

    def __init__(self, 
                gamecontroller,
                ship_names: list[str] = ["Carrier", "Battleship", "Destroyer", "Submarine", "Patrol Boat"],
                ship_lens: list[int] = [5, 4, 3, 3, 2],
                board_size: int = 10,
                name: str = "",
                ):
        """Initializes a player

        Args:
            game_controller: the game controller
            ship_names (list[str], optional): a list of strings which represents the ship names. Defaults to ["Carrier", "Battleship", "Destroyer", "Submarine", "Patrol Boat"].
            ship_lens (list[int], optional): a list of ints that represents the length of the ships. Defaults to [5, 4, 3, 3, 2].
            board_size (int, optional): the size of the board. Defaults to 10.
            name (str, optional): name of the user. Defaults to "".
        """

        self.ships = {"Carrier": s.Ship(), "Battleship": s.Ship(), "Destroyer": s.Ship(), "Submarine": s.Ship(), "Patrol Boat": s.Ship()}
        self.ship_names = ship_names
        self.ship_lens = ship_lens
        self.prev_guesses = []
        self.board_size = board_size
        self.name = name
        self.hits = []
        self.misses = []
        self.gamecontroller = gamecontroller

    @abstractmethod
    def set_player(self, size: int, name: str):
        """sets up a new player

        Args:
            size (int): size of the board
            name (str): the name of the player
        """

        pass

    def get_name(self) -> str:
        """retrieves the name

        Returns:
            str: the name of the player
        """

        return self.name

    @abstractmethod
    def make_new_ships(self):
        """makes new ships for a user
        """

        pass

    @abstractmethod
    def add_ship(self, name: str, leng: int, taken: list[p.Point]) -> list[p.Point]:
        """adds a single ship for a user

        Args:
            name (str): name of the ship
            leng (int): length of the ship
            taken (list[p.Point]): list of points that other ships are already placed over

        Returns:
            list[p.Point]: a list of points that this ship contains
        """

        pass

    def get_valid_dirs(self, point: list, leng: int, taken: list) -> list[str]:
        """making a list of valid directions to place a ship in given an endpoint and already taken spaces

        Args:
            point (list): the x and y coordinate if the point in (x, y) format
            leng (int): the length of the ship being placed
            taken (list): the already taken points

        Returns:
            list[str]: a list of valid directions
        """

        # making a list with all possible valid directions
        valid_directions = ["right", "left", "up", "down"]

        # for each point in the length of the ship, checking if placing the ship there is valid knowing the bounds and taken points
        # the try/excepts are there to ensure that if something is already removed from a list, the program won't break
        for i in range(leng):
            if not p.Point(chr(ord(point[0])+i), point[1]).is_valid(self.board_size, taken):
                try:
                    valid_directions.remove("down")
                except:
                    pass
            if not p.Point(chr(ord(point[0])-i), point[1]).is_valid(self.board_size, taken):
                try:
                    valid_directions.remove("up")
                except:
                    pass
            if not p.Point(point[0], point[1]+i).is_valid(self.board_size, taken):
                try:
                    valid_directions.remove("right")
                except:
                    pass
            if not p.Point(point[0], point[1]-i).is_valid(self.board_size, taken):
                try:
                    valid_directions.remove("left")
                except:
                    pass
        
        # returning the list with the remaining valid directions
        return valid_directions
    
    def place_ship_from_end_and_direction(self, point: list, direction: str, leng: int, name: str) -> list[p.Point]:
        """places a ship knowing the end point and the direction it should go in

        Args:
            point (list): the x and y coordinate if the point in (x, y) format for the end point of the ship
            direction (str): "right", "left", "up", or "down" to represent the direction the ship is being placed in
            leng (int): the length of the ship being placed
            name (str): name of the ship being placed

        Returns:
            list[p.Point]: _description_
        """

        # starting with an empty set of points and no modifier amounts
        row_add = 0
        col_add = 0
        points = []

        # depending on direction, makes a modifier for each point in the ship
        if direction == "right":
            row_add = 1
        elif direction == "left":
            row_add = -1
        elif direction == "up":
            col_add = -1
        else:
            col_add = 1

        # goes throught the length of the ship and adds the points to a list by using the modifier to make a new slightly altered point
        for num in range(0, leng):
            points.append(p.Point(chr(ord(point[0])+num*col_add), point[1]+num*row_add, False, name))
        
        # making a new ship with the given name and created points
        self.ships.update({name: s.Ship(points)})

        # returns the points contained in the ship
        return points

    def get_sunk_ships(self) -> list[str]:
        """gets the names of all of the ships that are sunk

        Returns:
            list[str]: the names of all of this user's ships that are sunk
        """

        # starting with an empty list and counter at 0
        sunk_ships = []
        counter = 0

        # goes through each ship and adds its name to the list if it is fully sunk
        for ship in self.ships.values():
            if ship.is_sunk():
                sunk_ships.append(self.ship_names[counter])
            counter += 1
        
        # returns the list of sunk ships
        return sunk_ships

    @abstractmethod
    def make_guess(self, other):
        """has a human player make a guess

        Args:
            other (Player): the other player
        """

        pass
        
    def check_hit(self, other, guess: p.Point, computer: bool = False):
        """checks if a guess has hit or sunk one of the other player's ship

        Args:
            other (Player): the other player
            guess (p.Point): the guess
            computer (bool, optional): if the current player is the computer. Defaults to False.
        """

        # initalizing a counter to 0 and the hit to false
        counter = 0
        hit = False

        # going through each of the other player's ships
        for ship in other.ships.values():

            # checking if the ship has been hit or sunk by the guess
            if ship.check_hit(guess):

                # if the point is hit, showing that the player is on path, sinking that point, and adding it to a list of hit points
                hit = True
                if self.name == "Computer":
                    self.update_path(other.ship_names[counter], self.computer_on_path[1]+1, self.computer_on_path[3], guess)
                guess.sink_point()
                self.hits.append(guess.get_tuple_point())

                # telling a user if the have hit or sunk a ship
                if ship.update_sunk():
                     self.gamecontroller.tell_ship_sunk(other.ship_names[counter], computer=computer)
                else:
                     self.gamecontroller.tell_ship_hit(other.ship_names[counter], computer=computer)
            counter += 1
        
        # of the point is not hit, adding it to a list of guessed points that were not hits
        if hit == False:
            self.misses.append(guess.get_tuple_point())
            self.gamecontroller.tell_miss(computer=computer)
    
    def get_hits(self) -> list[tuple]:
        """returning a list of previous hits

        Returns:
            list[tuple]: a list of the points hit with previous guesses with each point represented in (x, y) format
        """

        return self.hits

    def get_misses(self) -> list[tuple]:
        """returning a list of previous misses

        Returns:
            list[tuple]: a list of the points missed with previous guesses with each point represented in (x, y) format
        """

        return self.misses

    def is_fully_sunk(self) -> bool:
        """checks if all of a user's ships are sunk

        Returns:
            bool: True if all of the user's ships are sunk
        """

        # checks if each ship is sunk and returns false if the ship is not sunk
        for ship in self.ships.values():
            if not ship.is_sunk():
                return False
        return True

    def number_of_sunk(self) -> int:
        """tells total number of ships sunk

        Returns:
            int: the count of ships sunk
        """

        num = 0
        for ship in self.ships.values():
            if ship.is_sunk():
                num += 1
        return num