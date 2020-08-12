import pygame
import sudoku


pygame.font.init()


class Grid:
    board = [
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

    def __init__(self, rows: int, cols: int, width: int, height: int, board: list, win):
        """
        Construct a grid for sudoku.

        :param rows: an integer indicating how many rows the grid will have
        :param cols: an integer indicating how many columns the grid will have
        :param width: an integer indicating the width of the model
        :param height: an integer indicating the height of the model
        :param board: a list containing a list of integers that represent a valid Sudoku board
        :param win: a pygame display object
        """
        self.rows = rows
        self.cols = cols
        self.board = board
        self.boxes = [[Box(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        self.win = win


    def update_model(self):
        """ Update the Grid into new state """
        self.model = [[self.boxes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val: int) -> bool:
        """
        Place a number into a box

        :param val: an integer 1 to 9
        :return: a boolean True or False if guess is correct or not
        """
        row, col = self.selected
        if self.boxes[row][col].value == 0:
            self.boxes[row][col].set(val)
            self.update_model()

            if sudoku.valid(self.model, val, (row, col)) and sudoku.solve(self.model):
                return True
            else:
                self.boxes[row][col].set(0)
                self.boxes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        """
        Sketch a placeholder onto a box

        :param val: an integer 1 to 9
        """
        row, col = self.selected
        self.boxes[row][col].set_temp(val)

    def draw(self):
        """ Draw the grid lines and boxes onto canvas """
        # Draw grid lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            # In every three box, a thick line needs to been drawn to create the a section
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1

            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw boxes
        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].draw(self.win)

    def select(self, row, col):
        """
        Select a box in the grid

        :param row: an integer that represents the row coordinate
        :param col: an integer that represents the column coordinate
        """

        # Reset all other boxes as not selected
        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].selected = False

        self.boxes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        """ Clear selected box of the grid """
        row, col = self.selected
        if self.boxes[row][col].value == 0:
            self.boxes[row][col].set_temp(0)

    def click(self, pos: tuple):
        """ Return the position of clicked box """


    def is_finished(self) -> bool:
        """
        Check if Sudoku board is completed

        :return: a boolean true or false
        """

        for i in range(self.rows):
            for j in range(self.cols):
                if self.boxes[i][j].value == 0:
                    return False
        return True

class Box:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        """ Draw the number into box if there is a number """
        fnt = pygame.font.SysFont("arial", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2) - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        """ Set value """

    def set_temp(self, val):
        """ Set temp value (empty box) """


def main():


if __name__ == "__main__":
    main()