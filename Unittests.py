import unittest
import Board
import Minefield
import Solver


class BoardSetUp(unittest.TestCase):
    def setUp(self):
        self.board = Board.Board(2, 2, 2)


class TestBoardMethods(BoardSetUp):
    def test_is_cell_covered_covered(self):
        self.assertTrue(self.board.is_cell_covered(0, 0))

    def test_is_cell_covered_empty(self):
        self.board.boardgame = {i: 0 for i in xrange(2 * 2)}
        self.assertFalse(self.board.is_cell_covered(0, 0))

    def test_is_cell_covered_mine(self):
        self.board.boardgame = {i: -1 for i in xrange(2 * 2)}
        self.assertFalse(self.board.is_cell_covered(0, 0))

    def test_get_position_val_covered(self):
        self.assertTrue(self.board.get_position_val(0, 0))

suite = unittest.TestLoader().loadTestsFromTestCase(TestBoardMethods)
unittest.TextTestRunner(verbosity=2).run(suite)
