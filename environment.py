import numpy as np
import random


class Minesweeper:
    dimension=8
    density=0.2
    mines = int(dimension * dimension * density)

    board = np.zeros([dimension, dimension], dtype=int)
    for i in range(mines):
        while 1:
            row = random.randint(0, dimension - 1)
            col = random.randint(0, dimension - 1)
            if board[row, col] != 1:
                board[row, col] = 1
                break
    print(board)
   # board = generate_board(self)

    def check_neighbors(board, row, col):
        mines = 0
        if int(row - 1) >= 0:  # check the north neighbor
            if board[int(row - 1)][int(col)] == 1:
                mines += 1
        if int(row + 1) <= len(board) - 1:  # check the south neighbor
            if board[int(row + 1)][int(col)] == 1:
                mines += 1
        if int(col - 1) >= 0:  # check the west neighbor
            if board[int(row)][int(col - 1)] == 1:
                mines += 1
        if int(col + 1) <= len(board)-1:  # check the east neighbor
            if board[int(row)][int(col + 1)] == 1:
                mines += 1
        if int(row - 1) >= 0 and int(col - 1) >= 0:  # check the northwest neighbor
            if board[int(row - 1)][int(col - 1)] == 1:
                mines += 1
        if int(row - 1) >= 0 and int(col + 1) <= len(board)-1:  # check the northeast neighbor
            if board[int(row - 1)][int(col + 1)] == 1:
                mines += 1
        if int(row + 1) <= len(board)-1 and int(col - 1) >= 0:  # check the southwest neighbor
            if board[int(row + 1)][int(col - 1)] == 1:
                mines += 1
        if int(row + 1) <= len(board)-1 and int(col + 1) <= len(board)-1:  # check the southeast neighbor
            if board[int(row + 1)][int(col + 1)] == 1:
                mines += 1
        return mines

    print("mines: ", check_neighbors(board, 7, 7))
