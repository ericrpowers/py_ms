""" This will house the strategy/logic needed to solve
    Minesweeper automatically. The current thought process
    is the following:
    1) Identify all safe moves and mines based on immediate neighbors
    2) Identify all safe moves based on known mines
    3) Identify all safe moves by using neighbors' info
    4) Identify least risky move
    5) Blind click if no other options are found
"""
from datetime import datetime
import Board
import Cell


class Solver:
    """ The preset size of the board will be 10x10
        The preset number of the mines will be 10
    """
    x_size, y_size, mines = (10, 10, 10)
    num_of_games, wins, safe_moves = (0,) * 3
    num_of_turns = 1
    board, saved_board, cl = (None,) * 3

    def __init__(self):
        iterations = 10000
        start_time = datetime.now()

        while iterations != 0:
            self.num_of_games += 1
            self.board = Board.Board(self.x_size, self.y_size, self.mines)
            self.saved_board = None
            coord_array = self.select_next_cell()
            while not self.board.is_final_move(self.board.get_position_val(coord_array[0], coord_array[1]) == -1):
                self.num_of_turns += 1
                # self.board.show_board()
                coord_array = self.select_next_cell()

            if self.board.win():
                self.wins += 1
            # else:
            #     self.board.show_board()
            #     raise RuntimeError("Debug: Lost game")
            iterations -= 1
        elapsed_time = (datetime.now() - start_time).total_seconds()

        # Now to print out the statistics
        print "%20s %10s" % ("Total games", self.num_of_games)
        print "%20s %10s" % ("Total wins", self.wins)
        print "%20s %10s" % ("Total time taken (s)", elapsed_time)
        print "%20s %10s" % ("Win Percentage (%)", self.wins / (self.num_of_games * 1.00) * 100)
        print "%20s %10s" % ("Average # of turns", self.num_of_turns / (self.num_of_games * 1.00))

    """ First move needs to be handled, and then
        can move on to safe moves and finally
        risky moves """
    def select_next_cell(self):
        if self.saved_board is None:
            self.safe_moves = 0
            self.saved_board = []

            # First round just click in the center, since we know we cannot lose
            return [self.x_size / 2, self.y_size / 2]

        if self.safe_moves == 0:
            self.saved_board = self.board.get_board_values()
            self.cl = [Cell.Cell(self.saved_board[i]) for i in
                       xrange(self.x_size * self.y_size)]
            self.check_neighbors()
            self.find_safe_moves()

        # If no safe moves are identified, find least risky move
        if self.safe_moves == 0:
            coord = self.select_risky_move()
            # print "Debug: Risky move - Column " + str(coord[0] + 1) + " Row " + str(coord[1] + 1)
            return coord
        else:
            self.safe_moves -= 1
            return self.select_safe_move()

    """ To determine safe moves, there is a need
        to examine the landscape and determine
        where the known mines are, so that we
        can exhaust all safe moves in each pass """
    def check_neighbors(self):
        for y in xrange(self.y_size):
            for x in xrange(self.x_size):
                if self.cl[(self.x_size * y) + x].val == 0:
                    continue
                elif self.cl[(self.x_size * y) + x].val == 9:
                    continue
                self.cl[(self.x_size * y) + x].cov_neighbors = 0
                self.cl[(self.x_size * y) + x].nearby_mines = 0

                # Count the number of covered neighbors
                for yy in xrange(y - 1, y + 2):
                    if yy < 0 or yy >= self.y_size:
                        continue
                    for xx in xrange(x - 1, x + 2):
                        if xx < 0 or xx >= self.x_size or (yy == y and xx == x):
                            continue
                        elif self.cl[(self.x_size * yy) + xx].val == 9:
                            self.cl[(self.x_size * y) + x].cov_neighbors += 1
                            self.cl[(self.x_size * yy) + xx].weight += self.cl[(self.x_size * y) + x].val

                # If the neighbors equal the value, all neighbors are mines
                if self.cl[(self.x_size * y) + x].val == self.cl[(self.x_size * y) + x].cov_neighbors:
                    for yy in xrange(y - 1, y + 2):
                        if yy < 0 or yy >= self.y_size:
                            continue
                        for xx in xrange(x - 1, x + 2):
                            if xx < 0 or xx >= self.x_size or (yy == y and xx == x):
                                continue
                            elif self.cl[(self.x_size * yy) + xx].val == 9:
                                self.cl[(self.x_size * yy) + xx].is_mine = 1

                # Keep count of identified nearby mines
                for yy in xrange(y - 1, y + 2):
                    if yy < 0 or yy >= self.y_size:
                        continue
                    for xx in xrange(x - 1, x + 2):
                        if xx < 0 or xx >= self.x_size or (yy == y and xx == x):
                            continue
                        elif self.cl[(self.x_size * yy) + xx].is_mine == 1:
                            self.cl[(self.x_size * y) + x].nearby_mines += 1

                # See if we can already identify safe moves
                if self.cl[(self.x_size * y) + x].val == self.cl[(self.x_size * y) + x].nearby_mines:
                    for yy in xrange(y - 1, y + 2):
                        if yy < 0 or yy >= self.y_size:
                            continue
                        for xx in xrange(x - 1, x + 2):
                            if xx < 0 or xx >= self.x_size or (yy == y and xx == x):
                                continue
                            elif self.cl[(self.x_size * yy) + xx].val == 9 and \
                                    self.cl[(self.x_size * yy) + xx].is_mine == -1:
                                self.cl[(self.x_size * yy) + xx].is_mine = 0
                                self.safe_moves += 1

                # If more mines than value, we ran into an issue
                if self.cl[(self.x_size * y) + x].val < self.cl[(self.x_size * y) + x].nearby_mines:
                    print "ERROR - more mines (" + self.cl[(self.x_size * y) + x].nearby_mines + ") than value (" +\
                          self.cl[(self.x_size * y) + x].val + ")! Row " + str(y + 1) + " Column " + str(x + 1)
                    self.board.show_board()
                    raise RuntimeError("Found more mines than expected!")

    """ This method will handle more deductive means of finding safe
        moves and mines """
    def find_safe_moves(self):
        for y in xrange(self.y_size):
            for x in xrange(self.x_size):
                x1, x2, y1, y2 = (-1,) * 4
                if self.cl[(self.x_size * y) + x].val == 0:
                    continue
                elif self.cl[(self.x_size * y) + x].val == 9:
                    continue

                """ If we have a scenario where wh know val - 1 mines, we should be able to determine
                    the other mine and safe move based on neighboring hints """
                if self.cl[(self.x_size * y) + x].val - self.cl[(self.x_size * y) + x].nearby_mines == 1 and \
                        self.cl[(self.x_size * y) + x].cov_neighbors - self.cl[(self.x_size * y) + x].nearby_mines == 2:
                    for yy in xrange(y - 1, y + 2):
                        if yy < 0 or yy >= self.y_size:
                            continue
                        for xx in xrange(x - 1, x + 2):
                            if xx < 0 or xx >= self.x_size or (yy == y and xx == x):
                                continue
                            elif self.cl[(self.x_size * yy) + xx].val == 9 and\
                                    self.cl[(self.x_size * yy) + xx].is_mine == -1:
                                if x1 == -1:
                                    x1, y1 = xx, yy
                                else:
                                    x2, y2 = xx, yy

                    if x1 == -1 or x2 == -1:
                        continue
                    # Look below and above
                    if x1 == x2:
                        if 0 <= y - 1 < self.y_size:
                            self.deduce_mine(y - 1, x, y1, x1, y2, x2)
                        if 0 <= y + 1 < self.y_size:
                            self.deduce_mine(y + 1, x, y1, x1, y2, x2)
                    # Look left and right
                    if y1 == y2:
                        if 0 <= x - 1 < self.x_size:
                            self.deduce_mine(y, x - 1, y1, x1, y2, x2)
                        if 0 <= x + 1 < self.x_size:
                            self.deduce_mine(y, x + 1, y1, x1, y2, x2)

    """ Ideally, we should be able to figure out where more of
        the mines and safe spots are by looking at neighbors' hints """
    def deduce_mine(self, y0, x0, y1, x1, y2, x2):
        for yy in xrange(y0 - 1, y0 + 2):
            if yy < 0 or yy >= self.y_size:
                continue
            for xx in xrange(x0 - 1, x0 + 2):
                # Ignore entries we have already looking at or already identified mine state
                if xx < 0 or xx >= self.x_size or not(self.cl[(self.x_size * yy) + xx].val == 9 and
                                                              self.cl[(self.x_size * yy) + xx].is_mine == -1) or\
                        (yy == y0 and xx == x0) or (yy == y1 and xx == x1) or (yy == y2 and xx == x2):
                    continue
                if self.cl[(self.x_size * y0) + x0].val - self.cl[(self.x_size * y0) + x0].nearby_mines == 1:
                    # Return if any of the coordinates are 3 away from the cells in question
                    if yy == y1 + 3 or yy == y1 - 3 or yy == y2 + 3 or yy == y2 - 3 or xx == x1 + 3 or xx == x1 - 3 or\
                            xx == x2 + 3 or xx == x2 - 3:
                        return
                    self.cl[(self.x_size * yy) + xx].is_mine = 0
                    self.safe_moves += 1
                if self.cl[(self.x_size * y0) + x0].cov_neighbors - self.cl[(self.x_size * y0) + x0].val == 2 and\
                        self.cl[(self.x_size * yy) + xx].is_mine == 1:
                    self.cl[(self.x_size * yy) + xx].is_mine = 1
                    # Increase the nearby mine count if value is 1 - 8
                    for yyy in xrange(yy - 1, yy + 2):
                        if yyy < 0 or yyy >= self.y_size:
                            continue
                        for xxx in xrange(xx - 1, xx + 2):
                            if xxx < 0 or xxx >= self.x_size or (yyy == yy and xxx == xx):
                                continue
                            if self.cl[(self.x_size * yyy) + xxx].val > 0 or\
                                            self.cl[(self.x_size * yyy) + xxx].val < 9:
                                self.cl[(self.x_size * yyy) + xxx].nearby_mines += 1

    def select_safe_move(self):
        # All safe moves are identified with is_mine == 0
        for y in xrange(self.y_size):
            for x in xrange(self.x_size):
                if self.cl[(self.x_size * y) + x].val != 9 or\
                                self.cl[(self.x_size * y) + x].is_mine != 0:
                    continue
                self.cl[(self.x_size * y) + x].is_mine = -1
                return [x, y]

        raise RuntimeError("ERROR - Could not find a safe move!")

    # Weight the likelihood of each move and select the lowest change of failure
    def select_risky_move(self):
        prob = 99
        array = None        # least risky cell
        blind_array = None  # blind click cell
        for y in xrange(self.y_size):
            for x in xrange(self.x_size):
                if self.cl[(self.x_size * y) + x].val != 9 or\
                                self.cl[(self.x_size * y) + x].is_mine != -1:
                    continue
                c_weight = self.cl[(self.x_size * y) + x].weight
                if 0 < c_weight < prob:
                    prob = c_weight
                    array = [x, y]
                elif c_weight <= 0:
                    blind_array = [x, y]

        if array is None and blind_array is None:
            self.board.show_board()
            raise RuntimeError("ERROR - Could not find a risky move!")
        elif array is None:
            # Fall back on blind clicking as it is the only option
            array = blind_array

        return array

