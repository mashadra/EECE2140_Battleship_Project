class PlayerView:
    """represents a player's view
    """

    def __init__(self, tki):
        """initializes a player vies

        Args:
            tki (TKInterface): the tkinter interface used
        """

        self.current_input = ""
        self.current_long = ""
        self.tki = tki
        self.var = self.tki.var
    
    def get_name(self) -> str:
        """gets a name from a user

        Returns:
            str: the name inputted
        """

        self.tki.printInstructions("Please input name", True, self.current_long) 
        self.tki.printButton.wait_variable(self.var)
        self.current_input = self.tki.get_imp()
        return self.current_input

    def show_setup_message(self, num: int):
        """shows a set up message

        Args:
            num (int): number of the player being set up
        """

        self.current_long = f"Setting up Player {num}"

    def show_ship_placing(self, name: str, leng: int):
        """shows which ship is being placed

        Args:
            name (str): ship name
            leng (int): ship length
        """

        self.current_long = f"You are now placing the {name}. It is {leng} long"

    def show_player_turn(self, name: str):
        """shows whose turn it is

        Args:
            name (str): name of whoever's turn it is
        """

        self.current_long = f"{name}'s turn"

    def get_coord(self) -> list:
        """gets a coordinate from a user

        Returns:
            list: the point in [x coordinate, y coordinate] form
        """

        self.tki.printInstructions("Please input the x and y coordinate seperated by a space (ex: A 1)", True,self.current_long) 
        self.tki.printButton.wait_variable(self.var)
        self.current_input = self.tki.get_imp().split(" ")
        return self.current_input

    def get_dir(self, valid_directions: str) -> str:
        """gets a direction from the user

        Args:
            valid_directions (str): a string with all valid directions

        Returns:
            str: the input direction
        """

        self.tki.printInstructions(f"Please input the direction you would like it to go ({valid_directions})", self.current_long) 
        self.tki.printButton.wait_variable(self.var)
        self.current_input =self.tki.get_imp()
        return self.current_input

    def tell_ship_sunk(self, name: str, computer: bool = False):
        """telling a ship is sunk

        Args:
            name (str): name of the ship that was sunk
            computer (bool, optional): True if computer was the player. Defaults to False.
        """

        if computer:
            self.current_long = "Computer's turn"
            self.tki.printResponse(f"Computer has sunk the {name}")
            self.tki.printButton.wait_variable(self.var)
            self.tki.printResponse("")
        else:
            self.tki.printResponse(f"You have sunk the {name}")
            self.tki.printButton.wait_variable(self.var)

    def tell_ship_hit(self, name: str, computer: bool = False):
        """telling a ship is hit

        Args:
            name (str): name of the ship that was sunk
            computer (bool, optional): True if computer was the player. Defaults to False.
        """

        if computer:
            self.current_long = "Computer's turn"
            self.tki.printInstructions("Press button to continue", True, self.current_long) 
            self.tki.printResponse(f"Computer has hit the {name}")
            self.tki.printButton.wait_variable(self.var)
            self.tki.printResponse("")
        else:
            self.tki.printResponse(f"You have hit the {name}")
            self.tki.printButton.wait_variable(self.var)
    
    def tell_miss(self, computer: bool = False):
        """telling a guess was a miss

        Args:
            computer (bool, optional): True if computer was the player. Defaults to False.
        """

        if computer:
            self.current_long = "Computer's turn"
            self.tki.printInstructions("Press button to continue", True, self.current_long) 
            self.tki.printResponse(f"Computer has not hit a ship")
            self.tki.printButton.wait_variable(self.var)
            self.tki.printResponse("")
        else:
            self.tki.printInstructions("Press button to continue", True, self.current_long) 
            self.tki.printResponse(f"You have not hit a ship")
            self.tki.printButton.wait_variable(self.var)