import tkinter as tk
import view.EECE2140_Board as b

class TKInterface:
    """represents a tkinter interface
    """

    def __init__(self, size: int):
        """initializes a tkinter interface

        Args:
            size (int): size of one side of the board
        """

        self.SQ_WID = 20

        # Top level window
        self.frame = tk.Tk()
        self.frame.title("Battleship Game")
        self.frame.geometry('400x450')

        # Instruction Label Creation
        self.long_instr = tk.Label(self.frame, text = "")
        self.long_instr.pack()

        # Instruction Label Creation
        self.instr = tk.Label(self.frame, text = "")
        self.instr.pack()

        # TextBox Creation
        self.inputtxt = tk.Text(self.frame,
                        height = 1,
                        width = 20)
        
        self.inputtxt.pack()

        # Response Label Creation
        self.response = tk.Label(self.frame, text = "")
        self.response.pack()

        self.var = tk.IntVar()

        # Button Creation
        self.printButton = tk.Button(self.frame,
                                text = "Continue", 
                                command = lambda: self.clearInp())
        self.printButton.pack()

        # Score Label Creation
        self.score = tk.Label(self.frame, text = "")
        self.score.pack()

        # making 2 boards to show guesses
        self.board = b.Board(size, self.SQ_WID)
        self.other_board = b.Board(size, self.SQ_WID)

    def printInstructions(self, message: str, is_long=False, current_long=""):
        """prints to the instruction label

        Args:
            message (str): message for the main instruction
            is_long (bool, optional): True if a second text box for the instruction is needed. Defaults to False.
            current_long (str, optional): The extra instruction that will be added in the secind text box. Defaults to "".
        """

        if is_long:
            self.long_instr.config(text = current_long)
            self.long_instr.pack()
        self.instr.config(text = message)
        self.instr.pack()

    def printResponse(self, message: str):
        """prints to the response label

        Args:
            message (str): the message to print
        """

        self.response.config(text = message)
        self.response.pack()

    def clearInp(self):
        """clears the input textbox
        """

        self.inp = self.inputtxt.get(1.0, "end-1c")
        self.inputtxt.delete('1.0', tk.END)
        self.var.set(1)
        self.var.set(0)

    def get_imp(self):
        """gets the input from the input textbox

        Returns:
            _type_: _description_
        """

        return self.inp

    def printScore(self, message: str):
        """prints to the score label

        Args:
            message (str): the scoreboard represented as a string
        """

        self.score.config(text = message)
        self.score.pack()

    def set_up_board(self, player: str, message: str, hit_spaces: list[tuple], guessed_spaces : list[tuple], comp_hit_spaces: list[tuple], comp_guessed_spaces: list[tuple]):
        """sets up the 2 boards to show guesses

        Args:
            player (str): name of the human player
            message (str): the message to print to the score
            hit_spaces (list[tuple]): spaces the human player has hit
            guessed_spaces (list[tuple]): spaces the human player has missed
            comp_hit_spaces (list[tuple]): spaces the computer player has hit
            comp_guessed_spaces (list[tuple]): spaces the coomputer player has missed
        """

        self.printScore(message)
        self.board.update_board(player, hit_spaces, guessed_spaces)
        self.other_board.update_board("Computer", comp_hit_spaces, comp_guessed_spaces)

    def end_game(self):
        """shows the game is over
        """

        self.printInstructions("Game over")
        self.board.update_board("", [], [])