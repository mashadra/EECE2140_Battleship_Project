import random
import model.EECE2140_Player as pl
import model.EECE2140_Point as p

class ComputerPlayer(pl.Player):

    def __init__(self, 
                gamecontroller,
                ship_names: list[str] = ["Carrier", "Battleship", "Destroyer", "Submarine", "Patrol Boat"],
                ship_lens: list[int] = [5, 4, 3, 3, 2],
                board_size: int = 10,
                name: str = "",):
        super().__init__(gamecontroller, ship_names, ship_lens, board_size, name)
        self.computer_on_path = ("", 0, p.Point(None, None), p.Point(None, None))

    def set_player(self, size: int, name: str = "Computer"):
        """sets up a new computer player

        Args:
            size (int): size of the board
            name (str): the name of the computer player. Defaults to "COmputer".
        """

        # initializes variables from parameters
        self.board_size = size
        self.name = name

        # calling another function to make ships
        self.make_new_ships()

    def make_new_ships(self):
        """makes new ships for a computer user
        """

        # clears current dictionary with ships
        self.ships = {}

        # makes an empty list to hold points take as each ship is made
        taken = []

        # calls another function to add each ship individually and then add the points of that ship to the taken points
        for num in range(len(self.ship_names)):
            taken += self.add_computer_ship(self.ship_names[num], self.ship_lens[num], taken)
            print(f"{self.ship_names[num]}: {self.ships[self.ship_names[num]].print_points()}")
    
    def add_computer_ship(self, name: str, leng: int, taken: list[p.Point]) -> list[p.Point]:
        """adds a single ship for a computer user

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

        # randomly generating points until they input one that is valid (has valid directions and is within the confines of the board)
        while ((not p1.is_valid(self.board_size, taken))) or len(valid_directions) == 0:
            x = chr(random.randint(ord("A"), ord("A")+self.board_size))
            y = random.randint(1, self.board_size)
            point = [x, y]
            p1 = p.Point(point[0], point[1], name)
            valid_directions = self.get_valid_dirs(point, leng, taken)
        
        # randomly choosing a directionf rom the list of valid ones
        direction = valid_directions[random.randint(0, len(valid_directions)-1)]

        # calling another function to add the needed points to the ship
        points = self.place_ship_from_end_and_direction(point, direction, leng, name)
        
        # returning the points contained in the ship
        return points

    def make_guess(self, other):
        """makes a computer guess

        Args:
            other (Player): the other player
        """

        # makes the while loop condition false
        not_sat = True

        # generates points to guess until the point created is valid
        while not_sat:

            # if nothing has been guesed before, guess random
            if(len(self.prev_guesses) == 0):
                guess = (chr(random.randint(ord('A'), ord('A')+self.board_size)), random.randint(1, self.board_size))
                g = p.Point(guess[0], int(guess[1]))

            # if something has been guessed before, check if the previous guess(es) has hit a ship
            elif(self.on_path()):

                # knowing there is only one item in the list and it was a hit, guess knowing you've hit one point on a ship
                if(self.computer_on_path[1] == 1):
                    g = self.computer_guess_given_1hit(self.computer_on_path[3])
                
                # knowing that more than 1 point has been hit on the same ship
                else:
                    g = self.computer_guess_given_2hits(self.computer_on_path[2], self.computer_on_path[3])
                    if not g.is_valid(self.board_size, self.prev_guesses):
                        # flipping direction if end it hit but ship is not sunk
                        g = self.computer_guess_given_2hits(self.computer_on_path[3], self.computer_on_path[2])
                        g1 = self.computer_guess_given_2hits(self.computer_on_path[2], g)
                        while not g.is_valid(self.board_size, self.prev_guesses):
                            g2 = self.computer_guess_given_2hits(g, g1)
                            g = g1
                            g1 = g2

            # guessing random otherwise
            else:
                guess = (chr(random.randint(ord('A'), ord('A')+self.board_size)), random.randint(1, self.board_size))
                g = p.Point(guess[0], int(guess[1]))

            # checking if the guess is valid
            if(g.is_valid(self.board_size, self.prev_guesses)):
                not_sat = False

        # adding rh guess to previous guesses
        self.prev_guesses.append(g)

        # checking if the guess was a hit
        self.check_hit(other, g, computer=True)

        
    def computer_guess_given_1hit(self, last_point: p.Point) -> p.Point:
        """computer guessing a point knowing the previous move hit one point

        Args:
            last_point (p.Point): the previous point hit

        Returns:
            p.Point: _description_
        """
        
        # randomly choses a neighoring squares to guess
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        dir = random.randint(0, 3)
        new_p = last_point.get_modified_point(directions[dir][0], directions[dir][1])
        return new_p

    def computer_guess_given_2hits(self, last_point: p.Point, before_last_point: p.Point) -> p.Point:
        """computer guessing a point knowing 2 of its prior moves hit points

        Args:
            last_point (p.Point): the most recent hit
            before_last_point (p.Point): the orginial (older) hit

        Returns:
            p.Point: _description_
        """

        # finds a modified point and gets the direction accordingly
        dir = last_point.find_direction(before_last_point)
        if dir == "right":
            return last_point.get_modified_point(1, 0)
        elif dir == "left":
            return last_point.get_modified_point(-1, 0)
        elif dir == "up":
            return last_point.get_modified_point(0, 1)
        else: # dir == "Down"
            return last_point.get_modified_point(0, -1)

    def on_path(self) -> bool:
        """checks if the computer is on a trail from a previous hit

        Returns:
            bool: True if it is on a trail
        """

        if self.computer_on_path[0] != "":
                return True
        return False

    def update_path(self, name: str = "", guesses: int = 0, p1: p.Point = p.Point(None, None), p2: p.Point = p.Point(None, None)):
        """updates the computer's current path by checking for overflow and adding new values

        Args:
            name (str, optional): ship that is being pursued name. Defaults to "".
            guesses (int, optional): number of hits on this ship. Defaults to 0.
            p1 (p.Point, optional): older of the 2 most recent hits on this ship. Defaults to p.Point(None, None).
            p2 (p.Point, optional): more recent of 2 most recent hits on this ship. Defaults to p.Point(None, None).
        """

        # updating path with given values
        self.computer_on_path = (name, guesses, p1, p2)
        if self.computer_on_path[0] != "":

            # resetting the path if the counter of hits is as long as the ship (the ship has sunk)
            if self.computer_on_path[1] == self.ship_lens[self.ship_names.index(self.computer_on_path[0])]:
                self.computer_on_path = ("", 0, p.Point(None, None), p.Point(None, None))