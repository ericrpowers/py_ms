import Minefield
from sys import stdout


class Board:
    __cover_symbol, __empty_symbol, __mine_symbol = ('X', '.', '*')
    __col_len, __row_len, __m_count, __row, __column = (-1,) * 5
    __boardgame, __minefield = (None,) * 2

    def __init__(self, x_size, y_size, mine_count):
        self.__col_len = x_size
        self.__row_len = y_size
        self.__m_count = mine_count
        # Only setup the board to avoid losing on the first turn
        self.__start_board()

    def __start_board(self):
        self.__boardgame = [9 for i in xrange(self.__col_len * self.__row_len)]

    def get_board_values(self):
        return self.__boardgame

    def is_cell_covered(self, y, x):
        return self.__boardgame[(self.__col_len * x) + y] == 9

    def show_board(self):
        # TODO: Cleanup layout to make things prettier
        print("%11s" % "Rows")
        for x in xrange(self.__row_len, 0, -1):
            stdout.write("%9s" % x + " ")
            stdout.flush()

            for y in xrange(1, self.__col_len + 1):
                r_line = "   "
                val = self.__boardgame[(self.__col_len * (x - 1)) + (y - 1)]
                if val == -1:
                    r_line += self.__mine_symbol
                elif val == 0:
                    r_line += self.__empty_symbol
                elif val == 9:
                    r_line += self.__cover_symbol
                else:
                    r_line += str(val)
                stdout.write(r_line)
                stdout.flush()
            print

        c_line = "\n             1"
        for i in xrange(2, self.__col_len + 1):
            c_line += "   %d" % i if i < 10 else "  %d" % i
        print(c_line)
        print(("%" + str(len(c_line) / 2 + 7) + "s") % "Columns")

    def set_position(self):
        while True:
            itr = 0
            self.__row = -1
            self.__column = -1
            # Do not leave this region until two valid inputs are given
            while (self.__row < 0 or self.__row > self.__row_len - 1) if itr == 0 else\
                    (self.__column < 0 or self.__column > self.__col_len - 1):
                if itr == 0:
                    answer = raw_input("Row: ")
                else:
                    answer = raw_input("Column: ")

                try:
                    if itr == 0:
                        self.__row = int(answer) - 1
                    else:
                        self.__column = int(answer) - 1
                except ValueError:
                    print("Choose a number between 1 and %d" % (self.__row_len if itr == 0 else self.__col_len))
                    continue

                if (self.__row < 0 or self.__row > self.__row_len - 1) if itr == 0 else\
                        (self.__column < 0 or self.__column > self.__col_len - 1):
                    print("Choose a number between 1 and %d" % (self.__row_len if itr == 0 else self.__col_len))
                else:
                    itr += 1

            if not self.is_cell_covered(self.__column, self.__row):
                print("Field already shown")
            else:
                break

        # Return true if a mine is hit
        return self.get_position_val(self.__column, self.__row) == self.__minefield.get_mine_val()

    def get_position_val(self, y, x):
        # Setup the minefield if it down not exist
        self.__column = y
        self.__row = x
        if self.__minefield is None:
            self.__minefield = Minefield.Minefield(self.__col_len, self.__row_len, self.__m_count, x, y)

        return self.__minefield.get_cell_val((self.__col_len * x) + y)

    def is_final_move(self, is_mine):
        # If user did not hit a mine, uncover the empty region
        if not is_mine:
            self.__open_neighbors()
            is_mine = self.win()

        return is_mine

    """ When revealing the playing field, need to take into account the boundaries
        of the playing field and if the position is an empty cell (aka 0). If it is
        an empty cell, recursively continue to expand range until the entire empty
        region is exposed. """
    def __open_neighbors(self):
        for i in xrange(-1, 2):
            for j in xrange(-1, 2):
                if (self.__row + i) < 0 or (self.__row + i) >= self.__row_len or (self.__column + j) < 0 or\
                                (self.__column + j) >= self.__col_len:
                    continue
                if self.__minefield.get_cell_val((self.__col_len * (self.__row + i)) + (self.__column + j))\
                        == self.__minefield.get_mine_val():
                    continue
                val = self.__minefield.get_cell_val((self.__col_len * (self.__row + i)) + (self.__column + j))
                if not self.is_cell_covered(self.__column + j, self.__row + i):
                    continue

                self.__boardgame[(self.__col_len * (self.__row + i)) + (self.__column + j)] = val
                if val == 0 and not ((self.__row + i) == self.__row and (self.__column + j) == self.__column):
                    self.__row += i
                    self.__column += j
                    self.__open_neighbors()
                    self.__column -= j
                    self.__row -= i

    """ Once the number of covered cells equal the number of mines,
        the game is over. """
    def win(self):
        count = 0
        for x in xrange(self.__row_len):
            for y in xrange(self.__col_len):
                if self.is_cell_covered(y, x):
                    count += 1

        return count == self.__m_count

    def show_mines(self):
        for x in xrange(self.__row_len):
            for y in xrange(self.__col_len):
                if self.__minefield.get_cell_val((self.__col_len * x) + y) == self.__minefield.get_mine_val():
                    self.__boardgame[(self.__col_len * x) + y] = self.__mine_symbol

        self.show_board()
