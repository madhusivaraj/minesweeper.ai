import numpy as np
import random


class Minesweeper:
    dimension=8
    density=0.2

    def __init__(self, dims=dimension,
                 mine_density=density):

        self.dims = dims
        self.mines = int(dims * dims * mine_density)
        self.mines_hit = np.zeros((self.dims, self.dims), dtype=bool)
        self.flag = np.zeros((self.dims, self.dims), dtype=object)


    def generate_board(self):
        board = np.zeros([self.dims,self.dims],dtype=int)
        for i in range(self.mines):
            while 1:
                row = random.randint(0, self.dims-1)
                col = random.randint(0, self.dims-1)
                if board[row, col] != 1:
                    board[row, col] = 1
                    break
        return board

    def clue_number(board):
        return 2
        def find_mine_neighbors(board, row, cell):
            return 2

print(Minesweeper.generate_board(Minesweeper()))
