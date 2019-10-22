import random
import math

def print_dictionary(dic): # function to print dictionaries in readable way
    d = round(math.sqrt(len(dic)))
    lis = []
    for i in range(d):
        lis.append([])
        for j in range(d):
            lis[i].append(9)
    for i in range(d):
        for j in range(d):
            lis[i][j] = dic[(i,j)]
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in lis]))

def environment(d, n): # This function generates the environment from a dimension (d) and number of mines (n).
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
    return map

def base_agent_3(environment, total_mines):
    mine_or_safe = {}  # 0 if cell is safe, -1 if mine, -2 if flagged
    num_safe = {}  # number of safe cells identified around each cell
    num_mines = {}  # number of mines identified around each cell
    num_hidden_squares = {}  # number of untraversed cells around each cell
    safes = []  # List of untraversed safe cells that the program should check.
    d = len(environment)
    size = d**2
    cells_accounted = 0
    mines_flagged = 0

    while len(mine_or_safe) != size: # while some cells haven't yet been investigated or flagged
#####################################################################################################################
# Choose a new cell to investigate:
        if len(safes) > 0: # if there are some known safes
            (x, y) = safes[0] # coordinates = first in safes list
            safes.pop(0) # removed that coord from safes list
            cells_accounted += 1 # chooses known safe; accounted for because now it's been investigated
        else: # if no known safes
            (x, y) = (random.randint(0, d - 1), random.randint(0, d - 1)) # rand coords
            while (x, y) in mine_or_safe: # while it's already been seen
                (x, y) = (random.randint(0, d - 1), random.randint(0, d - 1)) # new rand
            cells_accounted += 1 # chooses random; accounted for because now it's been investigated

###################################################################################################################
# If it's a mine, note it:
        if (environment[x][y] == -1): # if it's a mine
            mine_or_safe[(x, y)] = -1 # record on final map

###################################################################################################################
# If it's a clue, note the knowledge of the cells surrounding current cell:
        else: # if it's a clue
            safe_num = 0 # tally of known safe cells around current cell
            mines_num = 0 # tally of known mines around current cell
            hidden_num = 0 # tally of hidden cells around current cell
            mine_or_safe[(x, y)] = 0
            curr_hidden = [] # creates empty list curr_hidden

            for i in [-1, 0, 1]: # left, center, right
                for j in [-1, 0, 1]: # down, center, up
                    if x + i >= 0 and x + i < d and y + j >= 0 and y + j < d:  # if is within bounds
                        if i == 0 and j == 0: # special condition: if looking at current cell (center, center)
                            continue # skip it
                        if (x + i, y + j) in mine_or_safe and mine_or_safe[(x + i, y + j)] == 0: # if seen and safe
                            safe_num += 1
                        elif (x + i, y + j) in mine_or_safe and mine_or_safe[(x + i, y + j)] == -1: # if seen and mine
                            mines_num += 1
                        elif (x + i, y + j) in mine_or_safe and mine_or_safe[(x + i, y + j)] == -2:  # if flagged
                            mines_num += 1
                        else: # if not seen yet
                            hidden_num += 1
                            curr_hidden.append((x + i, y + j)) # adds coordinates to curr_hidden
            num_safe[(x, y)] = safe_num # puts sum in num_safe
            num_mines[(x, y)] = mines_num # puts sum in num_mines
            num_hidden_squares[(x, y)] = hidden_num # puts sum in num_hidden_squares

#################################################################################################################
# Perform logical inference and record derived knowledge:
            # Infers positions of mines
            if environment[x][y] - num_mines[(x, y)] == num_hidden_squares[(x, y)]: # if clue - known mines around cell == num hidden around cell
                for (a, b) in curr_hidden: # for all hidden cells around current cell
                    mine_or_safe[(a, b)] = -2 # mark it as mine
                    cells_accounted += 1 # accounted for because it's flagged and will never be investigated
                    mines_flagged += 1 # must be flagging some mines twice

            # Infers positions of safe cells
            if 8 - environment[x][y] - num_safe[(x, y)] == num_hidden_squares[(x, y)]:
                for (a, b) in curr_hidden:
                    mine_or_safe[(a, b)] = 0
                    safes.append((a, b))

##################################################################################################################
# Finish, score, and print
    correct = 0
    wrong = 0
    for i in range(d):
        for j in range(d):
            if mine_or_safe[(i, j)] == -2 and environment[i][j] == -1: # if flagged and is actually mine
                correct += 1
            elif mine_or_safe[(i, j)] == -2 and environment[i][j] != -1: # if flagged but isn't actually mine
                wrong += 1
    score = (correct - wrong) / total_mines

    print(mines_flagged, "flags placed.")
    print(correct, "mines correctly flagged out of", total_mines, "total mines.")
    print("Score:", score)
    print_dictionary(mine_or_safe)

######################################################################################################################
######################################################################################################################

# Driver script
d = 12 # map dimension
total_mines = 30 # total number of mines in the environment
environment = environment(d, total_mines) # creates environment
score = base_agent_3(environment, total_mines) # plays minesweeper; prints mine_or_safe dictionary (final board state)