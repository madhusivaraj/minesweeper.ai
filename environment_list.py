# This function takes in a total number of mines (n) and a map dimension (d) and returns an environment which is a
# dXd board containing n mines in random cells, with all other cells containing clues. The environment returned
# is a list of lists, representing a dXd matrix. Mines represented by -1; clues by integers 0-8.

import random

def environment(d, n):
    map = []
    for i in range(d): # loops make a dXd map full of 0's
        map.append([])
        for j in range(d):
            map[i].append(0)
    m_placed = 0 # count of mines placed
    while m_placed < n: # while loop places n mines
        x = random.randint(0, d - 1)
        y = random.randint(0, d - 1)
        if map[x][y] != -1:
            map[x][y] = -1
            m_placed += 1
    c_placed = 0 # count of clues placed
    for q in range(d): # p and q are x,y coords in enviro
        for p in range(d):
            m_count = 0 # count of mines around a cell
            if map[q][p] == -1: # is mine; ignore
                continue
            else: # is not mine; generate and place clue
                for i in [-1, 0, 1]:  # left, center, right
                    for j in [-1, 0, 1]:  # down, center, up
                        if q + i >= 0 and q + i < d and p + j >= 0 and p + j < d:  # if is within bounds
                            if i == 0 and j == 0:  # special condition: if looking at current cell (center, center)
                                continue  # skip it
                            if map[q + i][p + j] == -1:  # if is mine
                                m_count += 1
            map[q][p] = m_count
            c_placed += 1
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in map]))
    return map

# Driver script
d = 8
n = 30
environment(d, n)



