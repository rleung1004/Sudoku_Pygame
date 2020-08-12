def valid(board: list, num: int, pos: tuple) -> bool:
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


def solve(board: list) -> bool:
    """
    Solve the given Sudoku board.

    :param board: a list containing list of integers
    :return: a boolean true or false
    """
    empty = find_empty(board)
    if not empty:
        return True
    else:
        row, col = empty

    for i in range(1, 10):
        if valid(board, i, empty):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False


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
    print_board(game_board)
    solve(game_board)
    print()
    print_board(game_board)


if __name__ == "__main__":
    main()
