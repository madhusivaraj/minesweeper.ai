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
    m_placed = 0 # count of mines placed so far in environment
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

def ukn_list(clues, environment, mine_or_safe): # Creates several objects needed for improved inference
    dim = len(environment)
    clue_list = []
    ukn_list = []
    clue_minus_flags = []
    for i in range(dim): # i and j loop thru enviro, to find clues in it
        for j in range(dim):
            if (i, j) in clues:
                clue_list.append((i, j)) # adds coords to list of clue coords
    for i in range(len(clue_list)): # for each clue in list
        clue_minus_flags.append(environment[clue_list[i][0]][clue_list[i][1]]) # adds clue value to clue_minus_flags list
    for i in range(len(clue_list)): # goes thru clue list
        #looks around each clue. if is ukn (not mine, flagged, or other clue), add to list (x, y, i)
        for q in [-1, 0, 1]: # left, center, right
            for p in [-1, 0, 1]: # down, center, up
                if clue_list[i][0]+q >= 0 and clue_list[i][0]+q < dim and clue_list[i][1]+p >= 0 and clue_list[i][1]+p < dim: # if in bounds
                    if q == 0 and p == 0: # if it's center
                        continue # ignore
                    if (clue_list[i][0]+q, clue_list[i][1]+p) not in mine_or_safe: # not mine, flag, or known safe
                        ukn_list.append((clue_list[i][0]+q, clue_list[i][1]+p, i))
                    elif mine_or_safe[(clue_list[i][0]+q, clue_list[i][1]+p)] == -2: # if it's flagged
                        clue_minus_flags[i] -= 1
    clue0mines = ukn_list[0][2] # num mines around clue 1 is it's clue value
    return [ukn_list, clue0mines, clue_minus_flags]

def validation(path, clue_minus_flags): # Determines whether a given possible mine configuration is consistent with known clues
    for i in range(len(clue_minus_flags)): # look around each clue_minus_flags, see if has appropriate num of mines placed
        counter = 0
        for j in range(len(path)): # for each item in path
            if path[j][2] == i: # if that item belongs to clue i
                counter += 1 # tally it
        if counter != clue_minus_flags[i]: # if mines for clue i isn't the right number
            return 0 # it's not a valid path
    return 1 # if no problems, it is a valid path

def assign_probabilities(all_valids, environment, mine_or_safe): # Uses all valid possible configurations of mines to assign probabilities to uknown cells
    dim = len(environment)
    probs = []
    for i in range(dim): # creates empty environment-sized list full of zeros
        probs.append([])
        for j in range(dim):
            probs[i].append(0)
    for i in range(len(all_valids)): # for each path in all_valids
        for j in range(len(all_valids[i])): # for each cell in that path
            x = all_valids[i][j][0] # x coord of cell
            y = all_valids[i][j][1] # y coord of cell
            probs[x][y] += 1 # add an instance of a mine to that cell
    num_configs = len(all_valids) # total number of valid configurations
    for i in range(dim):
        for j in range(dim):
            probs[i][j] = probs[i][j]/num_configs # divide number of instances of mines by number of configurations
    for i in range(dim):
        for j in range(dim):
            if (i,j) not in mine_or_safe:
                if probs[i][j] == 0:
                    probs[i][j] = 0.5 # assign all other cells half probability
    return probs

def improved_agent(environment, total_mines):
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
            min_p = 1
            min_coords = (0,0)
            for i in range(d):
                for j in range(d):
                    if probs[i][j] <= min_p:
                        min_p = probs[i][j]
                        min_coords = (i, j)
            (x, y) = min_coords
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

            # Advanced inference strategy
            dim = len(environment)
            [ukn_list, clue0mines, clue_minus_flags] = ukn_list(clues, environment, mine_or_safe)  # fcn(clues,enviro) to list ukns as (x, y, i), where i (FROM 0) is index of ukn in clue list

            ukn_per_clue = []  # list, num ukn cells around each clue. clue indicated by list index
            for i in range(len(clues)):
                ukn_per_clue_count = 0
                for j in range(len(ukn_list)):
                    if ukn_list[j][2] == i:
                        ukn_per_clue_count += 1
                    ukn_per_clue.append(ukn_per_clue_count)  # creates ukn_per_clue

            num_clues = 0  # number of clues represented in ukn_list
            clue_num_prev = -1
            for i in range(len(ukn_list)):
                if ukn_list[i][2] != clue_num_prev:
                    num_clues += 1
                    clue_num_prev = ukn_list[i][2]

            fg = []  # fringe; start w list of all ukns around first clue (ukns w index i=0)
            fringed = []  # list of items added to fringe
            fg_parents = []  # parents of items added to fringe
            for i in range(len(clue_minus_flags)):  # determine 1st clue that is not locked
                if clue_minus_flags[i] != 0:
                    first_good_clue = i
            for i in range(len(ukn_list)):
                if ukn_list[i][2] == first_good_clue:
                    fg.append(ukn_list[i])
                    fringed.append(ukn_list[i])
                    fg_parents.append(())  # for first ones put in list, parents are empty

            all_valids = []
            fringeable = []

            while len(fg) != 0:  # Depth First Search
                st = fg[len(fg) - 1]  # state = newest item in fg
                fg.pop(len(fg) - 1)  # removes new st from fg

                # Build current path (mine config).
                path = []
                path.append(st)  # first item in path is last mine placed
                from_1st = 0
                while from_1st < clue0mines:  # while last item in path is not the first mine placed
                    if st[2] == 0:  # if current mine was around 1st clue
                        from_1st += 1
                    for i in range(len(fringed)):
                        if fringed[i] == st:
                            st_pos = i
                            break
                    st_parent = fg_parents[st_pos]
                    path.append(st_parent)
                    st = st_parent
                path.reverse()  # reverses order

                if st[2] == num_clues - 1:  # If working from final clue, check config validity.
                    if len(path) == sum(clue_minus_flags):  # run to see if placed enough mines
                        if validation(path,
                                      clue_minus_flags) == 1:  # run validation fcn on the config to see if valid; 1 is valid, 0 not
                            all_valids.append(path)  # save this config to list of valid configs

                # For all, update lists and put children in fringe.
                locked_clues = []
                for i in range(num_clues):  # for each clue in ordered list of clues
                    placed_count = 0
                    flag = 0
                    for j in range(len(path)):  # look thru path, find which clue path ended on
                        if path[j][2] == i:  # if item in path belongs to clue i
                            placed_count += 1  # indicates that one mine has been placed for i

                        if placed_count == clue_minus_flags[
                            i]:  # clue_minus_flags is value of clue minus flags around it
                            flag = 1  # clue i is full
                            locked_clues.append(i)  # adds clue i to list of locked clues
                            break

                    if flag == 0:  # clue i was not full, so find open spots on clue i
                        fringeable = []
                        for j in range(len(ukn_list)):  # looks thru all cells where mine can be placed
                            if ukn_list[j][2] == i:  # if that ukn is around clue i
                                fringeable.append(ukn_list[j])  # adds it to list of possible to add to fg
                        unavailable = []  # list of cells that can't be added to fringe
                        for j in range(len(locked_clues)):  # for each locked clue
                            for k in range(len(ukn_list)):  # for each ukn cell
                                if ukn_list[k][2] == locked_clues[j]:  # if the ukn cell is around a locked clue
                                    unavailable.append(ukn_list[k])  # add to list of unavailable
                        for j in range(len(fringeable)):  # look through fringeable
                            if fringeable[j] in unavailable:  # it that cell is in list of unavailables
                                del (fringeable[j])  # remove it from list
                        break  # exit the loop of clues, i
                for i in range(len(fringeable)):
                    fg.append(fringeable[i])  # add fringeable cells to fringe
                    fringed.append(fringeable[i])  # cells that are added to fringe are added to list of fringed
                for i in range(len(fringeable)):  # add st to fg_parents len(fringeable) times
                    fg_parents.append(st)
            probs = assign_probabilities(all_valids, environment, mine_or_safe)

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
total_mines = 4 # total number of mines in the environment
environment = environment(d, total_mines) # creates environment
score = improved_agent(environment, total_mines) # plays minesweeper; prints mine_or_safe dictionary (final board state)