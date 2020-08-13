import pygame
import sudoku
import time


pygame.font.init()


class Grid:
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
        """ Update the boxes into new state """
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
        square = self.width / 9
        for i in range(self.rows + 1):
            # In every three box, a thick line needs to been drawn to create the a section
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1

            pygame.draw.line(self.win, (0, 0, 0), (0, i * square), (self.width, i * square), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * square, 0), (i * square, self.height), thick)

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

    def click(self, pos):
        """
        Translate mouse coordinates into Sudoku grid coordinates

        :param pos: mouse position given by pygame.mouse
        :return: a tuple containing coordinates referring to rows and columns
        """
        if pos[0] < self.width and pos[1] < self.height:
            square = self.width / 9
            col = pos[0] // square
            row = pos[1] // square
            return int(row), int(col)

    def solve_gui(self):
        self.update_model()
        empty = sudoku.find_empty(self.model)
        if not empty:
            return True
        else:
            row, col = empty

        for i in range(1, 10):
            if sudoku.valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.boxes[row][col].set(i)
                self.boxes[row][col].draw_solution(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.boxes[row][col].set(0)
                self.update_model()
                self.boxes[row][col].draw_solution(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False

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

        square = self.width / 9
        x = self.col * square
        y = self.row * square

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (square / 2 - text.get_width() / 2), y + (square / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, square, square), 3)

    def draw_solution(self, win, correct=True):
        fnt = pygame.font.SysFont("arial", 40)

        square = self.width / 9
        x = self.col * square
        y = self.row * square

        pygame.draw.rect(win, (255, 255, 255), (x, y, square, square), 0)
        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (square / 2 - text.get_width() / 2), y + (square / 2 - text.get_height() / 2)))

        if correct:
            pygame.draw.rect(win, (0, 255, 0), (x, y, square, square), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, square, square), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, play_time, strikes):
    """
    Redraw window after every event has happened.

    :param win: pygame display object
    :param board: a Grid object
    :param play_time: a time object
    :param strikes: an integer count that keeps track of current strikes
    """
    win.fill((255, 255, 255))
    fnt = pygame.font.SysFont("arial", 40)
    text = fnt.render("Time: " + str(play_time), 1, (0, 0, 0))
    win.blit(text, (540 - 160, 560))

    # Draw strikes
    text = fnt.render("Strikes: " + str(strikes), 1, (255, 0, 0))
    win.blit(text, (10, 560))
    board.draw()


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
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
    game_board = Grid(9, 9, 540, 540, board, win)
    key = None
    run = True
    start = time.time()
    strikes = 0

    while run:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    game_board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = game_board.selected
                    if game_board.boxes[i][j].temp != 0:
                        if game_board.place(game_board.boxes[i][j].temp):
                            print("SUCCESS")
                        else:
                            print("WRONG")
                            strikes += 1
                        key = None

                        if game_board.is_finished():
                            print("GAME OVER")
                            run = False
                if event.key == pygame.K_SPACE:
                    game_board.solve_gui()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = game_board.click(pos)

                if clicked:
                    game_board.select(clicked[0], clicked[1])
                    key = None

            if game_board.selected and key:
                game_board.sketch(key)

            redraw_window(win, game_board, play_time, strikes)
            pygame.display.update()


if __name__ == "__main__":
    main()