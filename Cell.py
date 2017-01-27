""" This is used by the solver to hold information gathered about a
    specific cell in the playing field to help determine if it is a
    safe move or a mine
"""


class Cell:
    def __init__(self, value):
        self.x = None
        self.y = None
        self.val = value
        self.cov_neighbors = 0
        self.nearby_mines = 0
        self.weight = 0              # Holds probability weight for risky moves
        self.is_mine = -1            # -1 = unknown, 0 = not mine, 1 = is mine

    def set_val(self, value):
        self.val = value
        # Reset weight and is_mine state in the process
        self.weight = 0
        self.is_mine = -1
