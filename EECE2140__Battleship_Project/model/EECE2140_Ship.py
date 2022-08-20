import model.EECE2140_Point as p

class Ship:
    """represents a ship
    """

    def __init__(self, points: list = [p.Point], sunk: bool = False):
        """initailizes a ship

        Args:
            points (list[p.Point], optional): points in the ship. Defaults to [].
            sunk (bool, optional): is the ship sunk. Defaults to False.
        """

        self.points = points
        self.sunk = sunk

    def is_sunk(self):
        """getter for self.sunk

        Returns:
            bool: self.sunk
        """

        return self.sunk

    def update_sunk(self) -> bool:
        """checks if the ship is sunk and updates it if it is

        Returns:
            bool: True if the ship is sunk
        """

        for point in self.points:
            if not point.is_sunk():
                self.sunk = False
                return False  
        self.sunk = True
        return True

    def add_point(self, x: chr, y: int, name: str, sunk: bool = False):
        """adding a point to the ship

        Args:
            x (chr): x coordinate
            y (int): y coordinate
            name (str): name of the ship
            sunk (bool, optional): if hte point is sunk. Defaults to False.
        """
    
        self.points.append(p.Point(x, y, sunk, name))

    def check_hit(self, other_point: p.Point) -> bool:
        """checks if a guess hits this ship by going though all th epoints in the ship

        Args:
            other_point (p.Point): _description_

        Returns:
            bool: True if the point hits this ship
        """

        for point in self.points:

            if point.is_hit(other_point):

                # sinking point if it's hit
                point.sink_point()
                return True

        return False

    def print_points(self) -> str:
        """making all points in a ship into a string

        Returns:
            str: string representation of all points in this ship
        """

        i = 0
        end = ""
        for point in self.points:
            end += (f"P{i}={point}, ")
            i += 1
        return end