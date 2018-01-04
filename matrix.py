import numpy as np


class TetrisMatrixGame(object):
    def __init__(self, *args, **kwargs):
        self.shape = kwargs.get("shape", (23, 10))
        self.matrix = np.zeros(self.shape, dtype=np.int)

    def validate_add_matrix(self, block, rownum=0, colnum=0):
        height_matrix = len(block.shape)

        if (colnum + block.widht() - 1) > self.shape[1] - 1:
            return False

        if (rownum + block.height()) > self.shape[0] - 1:
            return False

        extract_matrix = self.matrix[rownum:rownum + block.height(), colnum: colnum + block.widht()]

        for rindex, row in enumerate(block.matrix):
            for cindex, cell in enumerate(np.squeeze(np.asarray(row))):
                if cell == 0:
                    continue

                if extract_matrix[rindex][cindex] != 0:
                    return False

        return True

    def add_block(self, block, rownum, colnum):
        extract_matrix = self.matrix[rownum:rownum + block.height(), colnum: colnum + block.widht()]
        self.matrix[rownum:rownum + block.height(), colnum: colnum + block.widht()] = extract_matrix + block.matrix

    def get_copy_with_block(self, block, rownum, colnum):
        copy_matrix = self.matrix.copy()
        extract_matrix = copy_matrix[rownum:rownum + block.height(), colnum: colnum + block.widht()]
        copy_matrix[rownum:rownum + block.height(), colnum: colnum + block.widht()] = extract_matrix + block.matrix

        return copy_matrix

    def _print(self):
        print self.matrix

    def get_col_range_in_base_block_insertion(self, pivot, shape, colnum, higer_row):
        if colnum == 0:
            return (0, shape[1])

class Orientation(object):
    vertical = 0
    horizontal = 1


class TetrisBlock(object):
    type_block = None
    shape = ()
    matrix = None
    dimensions = 1
    orientation = Orientation.vertical

    def __init__(self, *args, **kwargs):
        self.dimensions = len(self.shape)
        self._build_block()

    def __str__(self):
        return self.type_block

    def _get_shape(self):
        return self.shape

    def widht(self):
        if len(self.shape) == 1:
            return self.shape[0]

        return self.shape[1]

    def height(self):
        if len(self.shape) == 1:
            return 1

        return self.shape[0]

    def rotate(self):
        self.matrix = np.rot90(self.matrix)
        self.shape = self.matrix.shape

    def _print(self):
        print self.matrix

    def _get_pivot(self):
        if self.matrix is None:
            raise NotImplementedError("No se implemento el metodo")

        if self.dimensions == 1:
            return tuple(0) if self.orientation == Orientation.horizontal else tuple(len(self.matrix) - 1)

        height, widht = self.shape
        for col in range(0, widht):
            if self.matrix[height - 1, col] == 1:
                return (height - 1, col)

    def _build_block(self):
        raise NotImplementedError("No se implemento el metodo")


class SquareBlock(TetrisBlock):
    def __init__(self, *args, **kwargs):
        self.shape = (2, 2)
        self.type_block = "Square"

        super(SquareBlock, self).__init__(*args, **kwargs)

    def _build_block(self):
        self.matrix = np.matrix([
            [1, 1],
            [1, 1]
        ])


class TeBlock(TetrisBlock):
    def __init__(self, *args, **kwargs):
        self.shape = (2, 3)
        self.type_block = "Te"

        super(TeBlock, self).__init__(*args, **kwargs)

    def _build_block(self):
        self.matrix = np.matrix([
            [1, 1, 1],
            [0, 1, 0]
        ])


class ZetaBlock(TetrisBlock):
    def __init__(self, *args, **kwargs):
        self.shape = (2, 3)
        self.type_block = "Zeta"

        super(ZetaBlock, self).__init__(*args, **kwargs)

    def _build_block(self):
        self.matrix = np.matrix([
            [0, 1, 1],
            [1, 1, 0]
        ])


class JayBlock(TetrisBlock):
    def __init__(self, *args, **kwargs):
        self.shape = (2, 3)
        self.type_block = "J"

        super(JayBlock, self).__init__(*args, **kwargs)

    def _build_block(self):
        self.matrix = np.matrix([
            [1, 1, 1],
            [1, 0, 0]
        ])
