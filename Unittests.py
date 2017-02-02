import unittest
import Board
import Minefield


class BoardSetUp(unittest.TestCase):
    def setUp(self):
        self.board = Board.Board(2, 2, 2)

    def tearDown(self):
        self.board = None


class TestBoardMethods(BoardSetUp):
    # is_cell_covered
    def test_is_cell_covered_covered(self):
        self.assertTrue(self.board.is_cell_covered(0, 0))

    def test_is_cell_covered_empty(self):
        self.board._Board__boardgame = {i: 0 for i in xrange(2 * 2)}
        self.assertFalse(self.board.is_cell_covered(0, 0))

    def test_is_cell_covered_mine(self):
        self.board._Board__boardgame = {i: -1 for i in xrange(2 * 2)}
        self.assertFalse(self.board.is_cell_covered(0, 0))

    # get_position_val
    def test_get_position_val_none_nearby(self):
        self.board = Board.Board(2, 2, 0)
        self.assertEqual(self.board.get_position_val(0, 0), 0)

    def test_get_position_val_2_nearby_mines(self):
        self.assertEqual(self.board.get_position_val(0, 0), 2)

    def test_get_position_val_mine(self):
        self.board = Board.Board(2, 2, 3)
        self.board.get_position_val(0, 0)
        self.assertEqual(self.board.get_position_val(1, 0), -1)

    def test_get_position_val_all_mines(self):
        self.board = Board.Board(2, 2, 4)
        with self.assertRaises(ValueError):
            self.board.get_position_val(0, 0)

    # is_final_move
    def test_is_final_move_true(self):
        self.board.get_position_val(0, 0)
        self.assertTrue(self.board.is_final_move(False))

    def test_is_final_move_false(self):
        self.board = Board.Board(4, 4, 8)
        self.board.get_position_val(0, 0)
        self.assertFalse(self.board.is_final_move(False))

    # win
    def test_win_false(self):
        self.assertFalse(self.board.win())

    def test_win_true(self):
        self.board.get_position_val(0, 0)
        self.board._Board__open_neighbors()
        self.assertTrue(self.board.win())


class MinefieldSetUp(unittest.TestCase):
    def setUp(self):
        self.minefield = Minefield.Minefield(2, 2, 2, 0, 0)

    def tearDown(self):
        self.minefield = None


class TestMinefieldMethods(MinefieldSetUp):
    # get_mine_val
    def test_get_mine_val(self):
        self.assertEqual(self.minefield.get_mine_val(), -1)

    # get_cell_val
    def test_get_cell_val_2_nearby_mines(self):
        self.assertEqual(self.minefield.get_cell_val(0), 2)

    def test_get_cell_val_empty(self):
        self.minefield = Minefield.Minefield(2, 2, 0, 0, 0)
        self.assertEqual(self.minefield.get_cell_val(0), 0)

    def test_get_cell_val_mine(self):
        self.minefield = Minefield.Minefield(2, 2, 3, 0, 0)
        self.assertEqual(self.minefield.get_cell_val(1), -1)


suites = [TestBoardMethods,
          TestMinefieldMethods,
          ]
for suite in suites:
    running_suite = unittest.TestLoader().loadTestsFromTestCase(suite)
    unittest.TextTestRunner(verbosity=2).run(running_suite)
