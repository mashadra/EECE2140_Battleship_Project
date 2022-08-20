class Point:

    def __init__(self, x: chr, y: int, sunk: bool = False, ship: str = None):
        """initalizes a point

        Args:
            x (chr): the x-coordinate
            y (int): the y-coordinate
            sunk (bool, optional): if the point is sunk. Defaults to False.
            ship (str, optional): the ship (if any) that th epoint belongs to. Defaults to None.
        """

        self.x = x
        self.y = y
        self.sunk = sunk
        self.ship = ship

    def __str__(self):
        """a string to represent a point

        Returns:
            str: string to represent the point
        """

        return f"x: {self.x} ... y: {self.y} .. sunk: {self.sunk}"

    def __eq__(self, other) -> bool:
        """checking if another object equals this point

        Args:
            other (any): other object

        Returns:
            bool: True if it is a poitn in the same location
        """

        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def is_sunk(self) -> bool:
        """getter for self.sunk

        Returns:
            bool: self.sunk
        """

        return self.sunk

    def is_valid(self, size: int, taken_spaces: list = []) -> bool:
        """checks if a point is within the frame of the board and that it is not taken already

        Args:
            size (int): size of the board
            taken_spaces (list, optional): _description_. Defaults to [].

        Returns:
            bool: True if the point is valid
        """

        return ord("A") <= ord(self.x) and ord(self.x) <= ord("A")+size and 1 <= self.y and self.y <= size and self not in taken_spaces

    def is_hit(self, point) -> bool:
        """sees if a point would hit this one

        Args:
            point (Point): the point trying to hit this one

        Returns:
            bool: True if the input point equals this point
        """

        if point == self:
            return True
        return False

    def get_modified_point(self, x_shift: int, y_shift: int):
        """shifts a point by a given amount

        Args:
            x_shift (int): shift in x direction
            y_shift (int): shift in y direction

        Returns:
            Point: a point shifted by the given amount from the current
        """

        return Point(chr(ord(self.x)+x_shift), self.y+y_shift)

    def get_ship(self) -> str:
        """getter for self.ship

        Returns:
            str: self.ship
        """

        return self.ship

    def find_direction(self, prev_point) -> str:
        """tells what direction the difference between 2 points represenents

        Args:
            prev_point (Point): the point before this one

        Returns:
            str: "right", "left", "up", or "down" for direction
        """

        if ord(self.x) - ord(prev_point.x) == 1:
            return "right"
        if ord(self.x) - ord(prev_point.x) == -1:
            return "left"
        if (self.y) - (prev_point.y) == 1:
            return "up"
        else:
            return "down"

    def sink_point(self):
        """makes self.sink True
        """

        self.sunk = True

    def get_tuple_point(self) -> tuple:
        """returns the point in (x, y format)

        Returns:
            tuple: (x coordinate, y coordinate)
        """

        return (ord(self.x)-ord("A"), self.y-1)