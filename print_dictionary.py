# Takes in a dictionary (dic), such as mine_or_safe from Sai's Base_Agent. Dictionary must have key values and entries
# formatted (x, y): z, where x and y are the environment coordinates, and z is 0 for empty cell, -1 for mine, or -2
# for flagged. The dimension of the environment is d, and the number of entries in the dictionary should be d**2.

import math

def print_dictionary(dic):
    d = round(math.sqrt(len(dic))) # calculates environement dimension, d, as sqrt of dictionary length
    lis = []
    for i in range(d): # for loops create a d by d list full of 9's which will be filled int
        lis.append([])
        for j in range(d):
            lis[i].append(9)
    for i in range(d): # for loops fill in the list with dictionary entries from appropriate coordinates
        for j in range(d):
            lis[i][j] = dic[(i,j)]
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in lis]))

# Example
# Prints mine_or_safe, which is the output of one run of Base_Agent using the environment in the commented line below
# environment = [[1,-1,2,-1,-1,2,1,0],[1,1,2,2,3,-1,3,2],[0,0,0,0,1,2,-1,-1],[0,0,0,0,0,1,2,2],[0,0,0,0,1,1,1,0],[1,1,1,0,1,-1,1,0],[1,-1,2,2,2,2,1,0],[1,2,-1,2,-1,1,0,0]]
# Note: Base_Agent still doesn't quite return complete mine_or_safe maps, so I had to add one entry manually to complete it
mine_or_safe = {(6, 0): 0, (7, 3): 0, (4, 7): 0, (5, 7): 0, (6, 6): 0, (5, 6): 0, (7, 7): 0, (0, 7): 0, (0, 0): 0, (1, 6): 0, (3, 7): 0, (5, 1): 0, (2, 5): 0, (0, 3): -2, (7, 2): -1, (4, 0): 0, (1, 2): 0, (6, 7): 0, (5, 5): -1, (2, 0): 0, (7, 6): 0, (4, 4): 0, (3, 0): 0, (6, 3): 0, (1, 5): -2, (3, 6): 0, (0, 4): -1, (1, 3): 0, (3, 3): 0, (5, 3): 0, (4, 1): 0, (1, 1): 0, (6, 4): 0, (5, 4): 0, (2, 6): -1, (3, 2): 0, (5, 0): 0, (7, 1): 0, (4, 5): 0, (2, 2): 0, (2, 7): -1, (1, 4): 0, (7, 5): 0, (0, 5): 0, (2, 1): 0, (4, 2): 0, (1, 0): 0, (6, 5): 0, (3, 5): 0, (0, 1): -2, (7, 0): 0, (4, 6): 0, (3, 4): 0, (6, 1): -1, (3, 1): 0, (0, 2): 0, (7, 4): -1, (0, 6): 0, (6, 2): 0, (4, 3): 0, (1, 7): 0, (2, 3): 0, (5, 2): 0, (2, 4): 0}
print_dictionary(mine_or_safe)
