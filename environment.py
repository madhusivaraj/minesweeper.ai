import numpy as np
import random


class Minesweeper:
    dimension=8
    density=0.2
    map = generate_board()


    def __init__(self, dims=dimension,
                 mine_density=density):

        self.dims = dims
        self.mines = int(dims * dims * mine_density)
        self.mines_hit = np.zeros((self.dims, self.dims), dtype=bool)
        self.flag = np.zeros((self.dims, self.dims), dtype=object)

    def generate_board(self):  # mines are 0
        board = np.zeros([self.dims, self.dims], dtype=int)
        for i in range(self.mines):
            while 1:
                row = random.randint(0, self.dims - 1)
                col = random.randint(0, self.dims - 1)
                if board[row, col] != 1:
                    board[row, col] = 1
                    break
        return board

    board = generate_board(self)

    def check_neighbors(board, row, col):
        mines = 0
        if int(row - 1) >= 0:  # check the north neighbor
            if board[int(row - 1)][int(col)] == 1:
                mines += 1
        if int(row + 1) <= dimension - 1:  # check the south neighbor
            if board[int(row + 1)][int(col)] == 1:
                mines += 1
        if int(col - 1) >= 0:  # check the west neighbor
            if board[int(row)][int(col - 1)] == 1:
                mines += 1
        if int(col + 1) <= 6:  # check the east neighbor
            if board[int(row)][int(col + 1)] == 1:
                mines += 1
        if int(row - 1) >= 0 and int(col - 1) >= 0:  # check the northwest neighbor
            if board[int(row - 1)][int(col - 1)] == 1:
                mines += 1
        if int(row - 1) >= 0 and int(col + 1) <= 6:  # check the northeast neighbor
            if board[int(row - 1)][int(col + 1)] == 1:
                mines += 1
        if int(row + 1) <= 7 and int(col - 1) >= 0:  # check the southwest neighbor
            if board[int(row + 1)][int(col - 1)] == 1:
                mines += 1
        if int(row + 1) <= 7 and int(col + 1) <= 6:  # check the southeast neighbor
            if board[int(row + 1)][int(col + 1)] == 1:
                mines += 1
        return mines

    print(check_neighbors(board, 2, 2))
