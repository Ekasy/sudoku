import pygame
from datetime import datetime

from sudoku_solver.backtracking import solve, sudoku


class Cell:
    rows = 9
    cols = 9
    default = 0

    def __init__(self, _value, _row, _col, _size):
        self.value = _value
        self.row = _row
        self.col = _col
        self.size = _size
        self.selected = False
        self.editable = True if _value == 0 else False

    def set(self, _value):
        self.value = _value

    def set_default(self):
        self.value = self.default

    def draw(self, model):
        font = pygame.font.SysFont('ComicSans', 30)
        step = self.size / self.rows
        x = self.col * step
        y = self.row * step

        if self.selected:
            pygame.draw.rect(model, (255, 255, 140), (x, y, step, step))
        elif self.value == 0:
            pygame.draw.rect(model, (255, 255, 250), (x, y, step, step))
        elif not self.selected:
            text = font.render(str(self.value), 1, (0, 0, 0))
            model.blit(text, (x + step / 2 - text.get_width() / 2, (y + step / 2 - text.get_width() / 2)))


class Board:
    rows = 9
    cols = 9

    def __init__(self, _board, _size):
        self.board = _board
        self.size = _size
        self.cells = [[Cell(_board[i][j], i, j, _size) for j in range(self.cols)] for i in range(self.rows)]
        self.selected = None
        self.answer = solve(_board)[1]
        self.buf = 0

    def set_buf(self, _value):
        self.buf = _value
        row, col = self.selected
        self.cells[row][col].value = _value

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False
        self.selected = None

        if self.cells[row][col].editable:
            self.cells[row][col].selected = True
            self.selected = (row, col)

    def clear(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False
        self.selected = None

    def click(self, pos):
        if pos[0] >= self.size and pos[1] >= self.size:
            return None
        step = self.size / self.rows
        row = pos[0] // step
        col = pos[1] // step
        return (int(col), int(row))

    def draw(self, sc):
        step = self.size / self.rows
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(sc)

        for i in range(self.rows + 1):
            if i % 3 == 0:
                w = 3
            else:
                w = 1
            pygame.draw.line(sc, (0, 0, 0), [0, i * step], [self.size, i * step], w)
            pygame.draw.line(sc, (0, 0, 0), [i * step, 0], [i * step, self.size, ], w)

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.answer[i][j] != self.cells[i][j].value:
                    return False
        return True


class Game:
    @staticmethod
    def run(_sudoku, _size):
        pygame.font.init()
        grid = Board(_sudoku, _size)
        height = _size + 40
        width = _size
        sc = pygame.display.set_mode((width, height))
        sc.fill((255, 255, 255))
        pygame.display.set_caption('Sudoku')
        start = datetime.now()
        key = None
        run = True
        while run:
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
                    if event.key == pygame.K_DELETE:
                        if grid.selected:
                            grid.set_buf(0)
                            grid.clear()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked = grid.click(pos)
                    if clicked:
                        grid.select(clicked[0], clicked[1])
                        key = None

            if key is not None and grid.selected:
                grid.set_buf(key)
                grid.clear()

            if grid.is_finished():
                print('You solve!')
                run = False

            Game.draw_game(sc, grid, height, start)
            pygame.display.update()

    @staticmethod
    def draw_game(sc, grid, height, start):
        sc.fill((255, 255, 255))
        font = pygame.font.SysFont('ComicSans', 30)
        # time = (datetime.now() - start).seconds
        # text = font.render('Time: {}:{}'.format(time, time), 1, (0, 0, 0))
        text = font.render('Time: {}'.format(Game.__convert_time(start)), 1, (0, 0, 0))
        sc.blit(text, (10, height - 30))

        grid.draw(sc)

    @staticmethod
    def __convert_time(start):
        seconds = (datetime.now() - start).seconds
        minutes = seconds // 60
        if seconds >= 60:
            seconds %= 60
        return '{}:{}'.format(str(minutes), str(seconds))


Game.run(sudoku, 360)
