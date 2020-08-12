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

    def __init__(self, rows: int, cols: int, width: int, height: int):
        """
        Construct a grid for sudoku.

        :param rows: an integer indicating how many rows the grid will have
        :param cols: an integer indicating how many columns the grid will have
        :param width: an integer indicating the width of the model
        :param height: an integer indicating the height of the model
        """
        self.rows = rows
        self.cols = cols
        self.boxes = [[Box(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None


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
        """ Sketch a placeholder onto a box """
        row, col = self.selected
        self.boxes[row][col].set_temp(val)

    def draw(self, win):
        """ Draw the grid lines and boxes onto canvas """

    def select(self, row, col):
        """ Select a box in the grid """


    def clear(self):
        """ Clear all boxes of the grid """

    def click(self, pos):
        """ Return the position of clicked box """

    def is_finished(self):
        """ Check if Sudoku board is completed """


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