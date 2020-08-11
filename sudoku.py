# mock game board
game_board = [
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


def print_board(board: list):
    """
    Print a sudoku board.

    :param board: a list containing list of integers
    """
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(board[i])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])

            else:
                print(str(board[i][j]) + " ", end="")


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


def main():
    print_board(game_board)
    print(find_empty(game_board))


if __name__ == "__main__":
    main()