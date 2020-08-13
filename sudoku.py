import random
import copy


class Sudoku:
    """ Generate and solve Sudoku puzzles using backtracking algorithm """

    def __init__(self):
        self.counter = 0
        self.board = [[0 for i in range(9)] for j in range(9)]
        self.generate_puzzle()

    def print_board(self):
        """ Print the sudoku board """
        for i in range(len(self.board)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - - ")

            for j in range(len(self.board[i])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")

                if j == 8:
                    print(self.board[i][j])

                else:
                    print(str(self.board[i][j]) + " ", end="")

    def generate_puzzle(self):
        """ Generate a Sudoku puzzle using backtracking algorithm """
        self.generate_solution(self.board)
        self.remove_numbers_from_board()
        return

    def solve_puzzle(self, board):
        """ solve the sudoku puzzle with backtracking """
        for i in range(81):
            row = i // 9
            col = i % 9
            # find next empty cell
            if board[row][col] == 0:
                for number in range(1, 10):
                    # check that the number hasn't been used in the row/col/subgrid
                    if valid(board, number, (row, col)):
                        board[row][col] = number
                        if not find_empty(board):
                            self.counter += 1
                            break
                        else:
                            if self.solve_puzzle(board):
                                return True
                break
        board[row][col] = 0
        return False

    def generate_solution(self, board):
        """generates a full solution with backtracking"""
        number_list = [i for i in range(1, 10)]
        empty = find_empty(board)
        if not empty:
            return True
        else:
            row, col = empty

        random.shuffle(number_list)
        for number in number_list:
            if valid(board, number, (row, col)):
                board[row][col] = number
                if not find_empty(board):
                    return True
                else:
                    if self.generate_solution(board):
                        # if the grid is full
                        return True
            board[row][col] = 0

        return False

    def remove_numbers_from_board(self):
        # get all non-empty squares from solution board
        non_empty_squares = get_non_empty_squares(self.board)
        non_empty_squares_count = len(non_empty_squares)
        rounds = 3

        while rounds > 0 and non_empty_squares_count >= 17:
            row, col = non_empty_squares.pop()
            non_empty_squares_count -= 1
            # store current value in case removing this creates multiple solutions
            removed_square = self.board[row][col]
            self.board[row][col] = 0
            # make a copy of board to solve it
            board_copy = copy.deepcopy(self.board)
            # initialize solution counter to zero
            self.counter = 0
            self.solve_puzzle(board_copy)
            # if there is more than one solution, put the previous removed square back into grid
            if self.counter != 1:
                self.board[row][col] = removed_square
                non_empty_squares_count += 1
                rounds -= 1
        return


def valid(board: list, num: int, pos: tuple) -> bool:
    """
    Check if the number put into given position of a Sudoku puzzle is valid or not.

    :param board: a list containing a list of integers
    :param num: an integer 1 to 9
    :param pos: a tuple containing coordinates (row, col)
    :return: a boolean True or False
    """
    # Check rows
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check each section
    section_x = pos[1] // 3
    section_y = pos[0] // 3

    for i in range(section_y * 3, section_y * 3 + 3):
        for j in range(section_x * 3, section_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True


def find_empty(board) -> tuple:
    """
    Return the next empty coordinate.

    :param board: a list containing list of integers
    :return: a tuple containing coordinates (row, col)
    """
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                # return row, col
                return i, j

    return None


def get_non_empty_squares(board):
    non_empty_squares = list()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 0:
                non_empty_squares.append((i, j))
    random.shuffle(non_empty_squares)
    return non_empty_squares


def main():
    sudoku = Sudoku()
    sudoku.print_board()


if __name__ == "__main__":
    main()
