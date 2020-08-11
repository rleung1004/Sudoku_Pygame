from unittest import TestCase
from unittest import mock
import sudoku
import io


class TestSudoku(TestCase):
    def setUp(self) -> None:
        """ Set up test objects """
        self.board = [
            [7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]
        ]

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_board(self, mock_stdout):
        """ Test print board """
        sudoku.print_board(self.board)

        expected = "7 8 0  | 4 0 0  | 1 2 0\n" \
                   "6 0 0  | 0 7 5  | 0 0 9\n" \
                   "0 0 0  | 6 0 1  | 0 7 8\n" \
                   "- - - - - - - - - - - - - \n" \
                   "0 0 7  | 0 4 0  | 2 6 0\n" \
                   "0 0 1  | 0 5 0  | 9 3 0\n" \
                   "9 0 4  | 0 6 0  | 0 0 5\n" \
                   "- - - - - - - - - - - - - \n" \
                   "0 7 0  | 3 0 0  | 0 1 2\n" \
                   "1 2 0  | 0 0 7  | 4 0 0\n" \
                   "0 4 9  | 2 0 6  | 0 0 7\n"

        self.assertEqual(expected, mock_stdout.getvalue(), "The board prints at a proper Sudoku board format.")

    def test_find_empty(self):
        """ Test find next empty """
        actual = sudoku.find_empty(self.board)

        expected = (0, 2)

        self.assertEqual(expected, actual, "This should return the next empty slot on a Sudoku board.")
