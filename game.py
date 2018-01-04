import random
from matrix import (TetrisMatrixGame, SquareBlock, TeBlock, ZetaBlock, JayBlock)
from grapx import MatrixTetris, BlockGraph


class GameTetris(object):
    def  __init__(self, *args, **kwargs):
        self.matrix_game = TetrisMatrixGame()
        self.shape = self.matrix_game.shape
        self.points = 0
        self.lines = 0
        self.level = 1
        self.time = 0
        self.started = False

        self.blocks = (
            SquareBlock,
            TeBlock,
            ZetaBlock,
            JayBlock
        )

    def restart(self):
        self.points = 0
        self.points = 0
        self.lines = 0
        self.level = 1
        self.time = 0
        self.colstart = 5
        self.col = None

    def get_random_matrix_block(self):
        class_block = random.choice(self.blocks)
        return class_block()

    def validate_add_block(self, actual_block, rownum, colnum):
        return self.matrix_game.validate_add_matrix(actual_block, rownum=rownum, colnum=colnum)

    def add_block(self, actual_block, rownum, colnum):
        self.matrix_game.add_block(actual_block, rownum, colnum)


if __name__ == "__main__":
    matrix_game = GameTetris()
    game_graph = MatrixTetris(matrix_game=matrix_game)
    game_graph.start()
