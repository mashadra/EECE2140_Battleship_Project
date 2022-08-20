import model.EECE2140_Player as pl
import model.EECE2140_Point as p

class HumanPlayer(pl.Player):

    def __init__(self, 
                gamecontroller,
                ship_names: list[str] = ["Carrier", "Battleship", "Destroyer", "Submarine", "Patrol Boat"],
                ship_lens: list[int] = [5, 4, 3, 3, 2],
                board_size: int = 10,
                name: str = "",):
        super().__init__(gamecontroller, ship_names, ship_lens, board_size, name)

    def set_player(self, size: int, name: str):
        """sets up a new human player

        Args:
            size (int): size of the board
            name (str): the name of the player
        """

        # initializes variables from parameters
        self.board_size = size
        self.name = name

        # calling another function to make ships
        self.make_new_ships()

    
    def make_new_ships(self):
        """makes new ships for a human user
        """

        # clears current dictionary with ships
        self.ships = {}

        # makes an empty list to hold points take as each ship is made
        taken = []

        # calls another function to add each ship individually and then add the points of that ship to the taken points
        for num in range(len(self.ship_names)):
            self.gamecontroller.show_ship_placing(self.ship_names[num], self.ship_lens[num])
            taken += self.add_ship(self.ship_names[num], self.ship_lens[num], taken)

    def add_ship(self, name: str, leng: int, taken: list[p.Point]) -> list[p.Point]:
        """adds a single ship for a human user

        Args:
            name (str): name of the ship
            leng (int): length of the ship
            taken (list[p.Point]): list of points that other ships are already placed over

        Returns:
            list[p.Point]: a list of points that this ship contains
        """

        # making an empty list to hold points for the ship
        points = []

        # making a dummy point and empty list of valid directions that will not allow the while loop to end
        valid_directions = []
        p1 = p.Point("a", -1)

        # collecting points from a user until they input one that is valid (has valid directions and is within the confines of the board)
        while (not p1.is_valid(self.board_size, taken)) or len(valid_directions) == 0:
            point = self.gamecontroller.get_coord()
            point[1] = int(point[1])
            p1 = p.Point(point[0], point[1], name)
            valid_directions = self.get_valid_dirs(point, leng, taken)
        points.append(p1)
        v = ", ".join(valid_directions)
        direction = ""
        
        # collecting a direction from the user until it is one in the list of valid directions
        while direction not in valid_directions:
            direction =  self.gamecontroller.get_dir(v)

        # calling another function to add the needed points to the ship
        points += self.place_ship_from_end_and_direction(point, direction, leng, name)

        # returning the points contained in the ship
        return points

    def make_guess(self, other):
        """has a human player make a guess

        Args:
            other (Player): the other player
        """

        # keeps asking for a coordinate until a valid one is given (not previously guessed or outside of bounds)
        satisfied = False
        while not satisfied or len(guess) != 2:
            guess =  self.gamecontroller.get_coord()
            g = p.Point(guess[0], int(guess[1]))
            if g.is_valid(self.board_size, self.prev_guesses):
                satisfied = True

        # adds the valid guess to the list of previous guesses
        self.prev_guesses.append(g)

        # checks if the guess has hit or sunk any of the other user's ships
        self.check_hit(other, g)