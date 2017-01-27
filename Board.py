import Minefield
from sys import stdout


class Board:
    cover_symbol, empty_symbol, mine_symbol = ('X', '.', '*')
    col_len, row_len, m_count, row, column = (-1,) * 5
    boardgame, minefield = (None,) * 2

    def __init__(self, x_size, y_size, mine_count):
        self.col_len = x_size
        self.row_len = y_size
        self.m_count = mine_count
        # Only setup the board to avoid losing on the first turn
        self.start_board()

    def start_board(self):
        self.boardgame = {i: 9 for i in xrange(self.col_len * self.row_len)}

    def get_board_values(self):
        return self.boardgame

    def is_cell_covered(self, y, x):
        return self.boardgame[(self.col_len * x) + y] == 9

    def show_board(self):
        # TODO: Cleanup layout to make things prettier
        print("%11s" % "Rows")
        for x in xrange(self.row_len, 0, -1):
            stdout.write("%9s" % x + " ")
            stdout.flush()

            for y in xrange(1, self.col_len + 1):
                r_line = "   "
                val = self.boardgame[(self.col_len * (x - 1)) + (y - 1)]
                if val == -1:
                    r_line += self.mine_symbol
                elif val == 0:
                    r_line += self.empty_symbol
                elif val == 9:
                    r_line += self.cover_symbol
                else:
                    r_line += str(val)
                stdout.write(r_line)
                stdout.flush()
            print

        c_line = "\n             1"
        for i in xrange(2, self.col_len + 1):
            c_line += "   %d" % i if i < 10 else "  %d" % i
        print(c_line)
        print(("%" + str(len(c_line) / 2 + 7) + "s") % "Columns")

    def set_position(self):
        while True:
            itr = 0
            self.row = -1
            self.column = -1
            # Do not leave this region until two valid inputs are given
            while (self.row < 0 or self.row > self.row_len - 1) if itr == 0 else\
                    (self.column < 0 or self.column > self.col_len - 1):
                if itr == 0:
                    answer = raw_input("Row: ")
                else:
                    answer = raw_input("Column: ")

                try:
                    if itr == 0:
                        self.row = int(answer) - 1
                    else:
                        self.column = int(answer) - 1
                except ValueError:
                    print("Choose a number between 1 and %d" % (self.row_len if itr == 0 else self.col_len))
                    continue

                if (self.row < 0 or self.row > self.row_len - 1) if itr == 0 else\
                        (self.column < 0 or self.column > self.col_len - 1):
                    print("Choose a number between 1 and %d" % (self.row_len if itr == 0 else self.col_len))
                else:
                    itr += 1

            if not self.is_cell_covered(self.column, self.row):
                print("Field already shown")
            else:
                break

        # Return true if a mine is hit
        return self.get_position_val(self.column, self.row) == self.minefield.get_mine_val()

    def get_position_val(self, y, x):
        # Setup the minefield if it down not exist
        self.column = y
        self.row = x
        if self.minefield is None:
            self.minefield = Minefield.Minefield(self.col_len, self.row_len, self.m_count, x, y)

        return self.minefield.get_cell_val((self.col_len * x) + y)

    def is_final_move(self, is_mine):
        # If user did not hit a mine, uncover the empty region
        if not is_mine:
            self.open_neighbors()
            is_mine = self.win()

        return is_mine

    """ When revealing the playing field, need to take into account the boundaries
        of the playing field and if the position is an empty cell (aka 0). If it is
        an empty cell, recursively continue to expand range until the entire empty
        region is exposed. """
    def open_neighbors(self):
        for i in xrange(-1, 2):
            for j in xrange(-1, 2):
                if (self.row + i) < 0 or (self.row + i) >= self.row_len or (self.column + j) < 0 or\
                                (self.column + j) >= self.col_len:
                    continue
                if self.minefield.get_cell_val((self.col_len * (self.row + i)) + (self.column + j))\
                        == self.minefield.get_mine_val():
                    continue
                val = self.minefield.get_cell_val((self.col_len * (self.row + i)) + (self.column + j))
                if not self.is_cell_covered(self.column + j, self.row + i):
                    continue

                self.boardgame[(self.col_len * (self.row + i)) + (self.column + j)] = val
                if val == 0 and not ((self.row + i) == self.row and (self.column + j) == self.column):
                    self.row += i
                    self.column += j
                    self.open_neighbors()
                    self.column -= j
                    self.row -= i

    """ Once the number of covered cells equal the number of mines,
        the game is over. """
    def win(self):
        count = 0
        for x in xrange(self.row_len):
            for y in xrange(self.col_len):
                if self.is_cell_covered(y, x):
                    count += 1

        return count == self.m_count

    def show_mines(self):
        for x in xrange(self.row_len):
            for y in xrange(self.col_len):
                if self.minefield.get_cell_val((self.col_len * x) + y) == self.minefield.get_mine_val():
                    self.boardgame[(self.col_len * x) + y] = self.mine_symbol

        self.show_board()
