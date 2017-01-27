from random import randint


class Minefield:
    mine_val = -1
    minefield = None

    def __init__(self, col_length, row_length, mine_count, row, column):
        self.minefield = {i: 0 for i in xrange(col_length * row_length)}
        self.place_mines(col_length, row_length, mine_count, row, column)
        self.fill_hints(col_length, row_length)

    def get_mine_val(self):
        return self.mine_val

    def get_cell_val(self, pos):
        return self.minefield[pos]

    # Avoid entries with mines and the first selected position
    def place_mines(self, col_length, row_length, mine_count, row, column):
        for i in xrange(mine_count):
            x = randint(0, row_length - 1)
            y = randint(0, col_length - 1)
            while self.minefield[(col_length * x) + y] == self.mine_val or (x == row and y == column):
                x = randint(0, row_length - 1)
                y = randint(0, col_length - 1)

            self.minefield[(col_length * x) + y] = self.mine_val

    """ To fill in the hints, need to look at every empty cell and count the
        number of adjacent mines into that cell. Make sure to avoid going outside
        the boundaries of the playing field. """
    def fill_hints(self, col_length, row_length):
        for row in xrange(row_length):
            for column in xrange(col_length):
                for i in xrange(-1, 2):
                    for j in xrange(-1, 2):
                        if 0 <= (row + i) < row_length and 0 <= (column + j) < col_length:
                            if self.minefield[(col_length * row) + column] != self.mine_val:
                                if self.minefield[(col_length * (row + i)) + (column + j)] == self.mine_val:
                                    self.minefield[(col_length * row) + column] += 1
