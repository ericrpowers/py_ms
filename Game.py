import Board
import Solver


class Game:
    board = None
    turn = 0

    def __init__(self):
        answer = ""

        # Check if user or the solver will play
        while not (answer == "u" or answer == "b"):
            answer = raw_input("Will the user or the bot play?(u/b) ").replace("\\s+", "").lower()

        if answer == "u":
            self.user()
        else:
            Solver.Solver()

    def user(self):
        # Initialize size and mines to use in loop
        x_size, y_size, mines = (0,)*3

        for i in xrange(3):
            tmp = -1
            f_pass = True
            answer = ""
            while tmp < 5 or (tmp > 20 if i <= 1 else tmp > (x_size * y_size) / 3):
                if f_pass is True:
                    if i == 0:
                        answer = raw_input("Size of X-axis (5 - 20): ")
                    elif i == 1:
                        answer = raw_input("Size of Y-axis (5 - 20): ")
                    else:
                        # Let's avoid too many mines and restrict it to max ~1/3rd of entire board
                        answer = raw_input("Number of mines (5 - %d): " % ((x_size * y_size) / 3))
                    f_pass = False

                # Look for an integer within the user input else ignore
                try:
                    tmp = int(answer)
                except ValueError:
                    answer = ""

                if tmp < 5 or (tmp > 20 if i <= 1 else tmp > (x_size * y_size) / 3):
                    answer = raw_input("Choose a number between 5 and %d: " % (20 if i <= 1 else (x_size * y_size) / 3))

            if i == 0:
                x_size = tmp
            elif i == 1:
                y_size = tmp
            else:
                mines = tmp

        answer = "y"
        while answer == "y":
            board = Board.Board(x_size, y_size, mines)
            self.turn = 0
            self.play(board)

            answer = ""
            while not (answer == "y" or answer == "n"):
                answer = raw_input("Want to play again?(y/n) ").replace("\\s+", "").lower()

    def play(self, board):
        while True:
            self.turn += 1
            print("\nTurn %d" % self.turn)
            board.show_board()
            if board.is_final_move(board.set_position()):
                break

        if board.win():
            print("Congrats, you found all the mines in %d turns." % self.turn)
        else:
            print("You hit a mine! Try again.")

        board.show_mines()
