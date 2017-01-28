import unittest
import Board
import Minefield
import Solver

class BoardSetUp(unittest.TestCase):
    def setUp(self):
        self.board = Board.Board(10, 10, 10)

class TestBoardMethods(BoardSetUp):
    def test_is_cell_covered(self):
        self.assertTrue(self.board.is_cell_covered(0, 0))

suite = unittest.TestLoader().loadTestsFromTestCase(TestBoardMethods)
unittest.TextTestRunner(verbosity=2).run(suite)