import sys
import pygame
import numpy as np
from matrix import (TetrisMatrixGame, SquareBlock, TeBlock, ZetaBlock, JayBlock)


class MatrixTetris(object):
    def __init__(self, *args, **kwargs):
        self.matrix_game = kwargs.get('matrix_game')
        self.speed = 5
        self.size_screen = 800, 900
        self.screen = None
        self.added_blocks = []
        self.current_block = None
        self.next_block = None
        self.col_block = 4
        self.row_block = 0

        self.widht_block = 40
        self.start_x = 205
        self.start_y = 0
        self.block_snapshot = None

        self.points = 0
        self.lines = 0
        self.level = 1
        self.time = 0
        self.started = False

        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)

    def set_screen(self):
        self.font = pygame.font.SysFont("monospace", 28)
        self.title = pygame.font.SysFont("monospace", 35)
        self.screen = pygame.display.set_mode(self.size_screen)

    def draw(self):
        x, y = self.start_x, self.start_y

        self.screen.fill(self.black)

        pygame.draw.line(self.screen, self.white, [200, 0], [200, 900], 10)
        pygame.draw.line(self.screen, self.white, [620, 0], [620, 900], 10)

        points = self.font.render("Points: {0}".format(self.points), True, self.white)
        lines = self.font.render("Lines: {0}".format(self.lines), True, self.white)
        level = self.font.render("Level: {0}".format(self.level), True, self.white)
        next_block = self.title.render("Next Block", True, self.white)

        self.screen.blit(points, [10, 10])
        self.screen.blit(lines, [10, 40])
        self.screen.blit(level, [10, 70])
        self.screen.blit(next_block, [20, 210])

        self.draw_next_block()

        actual_matrix = self.matrix_game.matrix_game.get_copy_with_block(self.current_block, self.row_block, self.col_block)

        for rindex, row in enumerate(actual_matrix):
            y = self.start_y + (self.widht_block * rindex) + rindex

            for cindex, cell in enumerate(np.squeeze(np.asarray(row))):
                x = self.start_x + (self.widht_block * cindex) + cindex
                if cell == 0:
                    continue

                rect = pygame.rect.Rect([x, y, self.widht_block, self.widht_block])
                pygame.draw.rect(self.screen, self.green, rect)

    def start(self):
        self.started = True

        pygame.init()
        pygame.font.init()

        clock = pygame.time.Clock()
        self.set_screen()

        self.current_block = self.matrix_game.get_random_matrix_block()
        self.next_block = self.matrix_game.get_random_matrix_block()

        while self.started:
            clock.tick(self.speed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.block_snapshot = self.row_block, self.col_block

            self.draw()

            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                if self.col_block > 0:
                    if self.matrix_game.validate_add_block(self.current_block, self.row_block + 1, self.col_block - 1):
                        self.col_block -= 1

            if key[pygame.K_RIGHT]:
                if self.matrix_game.shape[1] - 1 > (self.col_block + self.current_block.widht() - 1):
                    if self.matrix_game.validate_add_block(self.current_block, self.row_block + 1, self.col_block + 1):
                        self.col_block += 1
            
            if key[pygame.K_SPACE]:
                 self.current_block.rotate()

                 if self.row_block > 0:
                     self.row_block -= 1

                 clock.tick(self.speed)
                 continue

            self.row_block += 1
            if not self.matrix_game.validate_add_block(self.current_block, self.row_block, self.col_block):
                if self.row_block in (0, 1 ,2):
                    game_over = self.title.render("Game Over", True, self.white)
                    self.screen.blit(game_over, [220, 410])
                    self.started = False
                    clock.tick(0.5)

                else:
                    self.matrix_game.add_block(self.current_block, self.block_snapshot[0], self.block_snapshot[1])
                    self.current_block = self.next_block
                    self.next_block = self.matrix_game.get_random_matrix_block()

                    self.col_block = 5
                    self.row_block = 0


            pygame.display.update()
            clock.tick(self.speed)

    def draw_next_block(self):
        next_block = BlockGraph(matrix_figure=self.next_block)
        next_block.draw(self.screen, x=40, y=260)

class BlockGraph(object):
    def __init__(self, *args, **kwargs):
        self.matrix_figure = kwargs.get('matrix_figure')
        self.x = 210
        self.y = 0
        self.piled = False
        self.width = kwargs.get('width', 40)
        self.green = (0, 255, 0)

    def draw(self, screen, x=None, y=None):
        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        for rindex, row in enumerate(self.matrix_figure.matrix):
            for cindex, cell in enumerate(np.squeeze(np.asarray(row))):
                if cell == 0:
                    continue

                rect = pygame.rect.Rect([self.get_next_x(cindex), self.get_next_y(rindex), self.width, self.width])
                pygame.draw.rect(screen, self.green, rect)

    def get_next_x(self, c_index):
        space = c_index + 1
        return self.x + (c_index * self.width) + space

    def get_next_y(self, r_index):
        space = r_index + 1
        return self.y + (r_index * self.width) + space
