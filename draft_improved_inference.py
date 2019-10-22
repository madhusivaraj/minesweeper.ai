
#########################################################
def ukn_list(clues, environment, mine_or_safe):
    dim = len(environment)
    clue_list = []
    ukn_list = []
    for i in range(dim): # i and j loop thru enviro, to find clues in it
        for j in range(dim):
            if (i, j) in clues:
                clue_list.append((i, j)) # adds coords to list of clue coords
    for i in range(len(clue_list)): # goes thru clue list
        #looks around each clue. if is ukn (not mine, flagged, or other clue), add to list (x, y, i)
        for q in [-1, 0, 1]: # left, center, right
            for p in [-1, 0, 1]: # down, center, up
                if clue_list[i][0]+q >= 0 and clue_list[i][0]+q < dim and clue_list[i][1]+p >= 0 and clue_list[i][1]+p < dim: # if in bounds
                    if q == 0 and p == 0: # if it's center
                        continue # ignore
                    if (clue_list[i][0]+q, clue_list[i][1]+p) not in mine_or_safe:
                        ukn_list.append((clue_list[i][0]+q, clue_list[i][1]+p, i))
    return ukn_list

#######################################################
dim = len(environment)
ukn_list = ukn_list(clues,environment,mine_or_safe) # fcn(clues,enviro) to list ukns as (x, y, i), where i FROM 0 is index of ukn in clue list
ukn_per_clue = []# list, num ukn cells around each clue. clue indicated by list index
clue1mines = 0 # num of mines around 1st clue in list
for i in range(len(clues)):
    ukn_per_clue_count = 0
    for j in range(len(ukn_list)):
        if ukn_list[j][2] == i:
            ukn_per_clue_count += 1
        ukn_per_clue.append(ukn_per_clue_count) # creates ukn_per_clue

num_clues = len(clues)# number of clues in clue dict

fg = [(0,1,0),(1,1,0),(1,0,0)]# fringe; start w list of all ukns around first clue (ukns w index i=1)
fringed = [(0,1,0),(1,1,0),(1,0,0)]# fg
fg_parents = [(),(),()]# fg; for first ones put in list, parents are empty
all_valids = []

while len(fg) != 0:
    st = fg[len(fg)-1] # state = newest item in fg
    fg.pop(len(fg)-1) # removes new st from fg

    # Build current path (mine config).
    path = [st] # first item in path is last mine placed
    from_1st = 0
    while from_1st < clue1mines: # while last item in path is not the first mine placed
        if st[2] == 0: # if current mine was around 1st clue
            from_1st += 1
        for i in range(len(fringed)):
            if fringed[i] == st:
                st_pos = i
                break
        st_parent = fg_parents[st_pos]
        path.append(st_parent)
        st = st_parent
    path.pop(len(path)-1) # removes empty item at end
    path.reverse() # reverses order
    print('config is',path)
    #if st[2] == num_clues: # If working from final clue, check config validity.
     #   if completeness() == 1: # run to see if placed enough mines
      #      if validation() == 1: # run validation fcn on the config to see if valid; 1 is valid, 0 not
       #         all_valids.append(path) # save this config to list of valid configs

    # For all, update lists and put children in fringe.
        # find valid ch, put ch end of fg, put ch end of fringed, put st end of fg_parents
        # look thru path until find clue that isnt full. pull ukns not in path yet, AND NOT locked, add to fg
        # when adding to fringe, ask: what can the next step possibly be?
            # will be open spot on current clue, or open spot on next clue
    for i in range(len(num_clues)): # for each clue in ordered list of clues
        placed_count = 0
        flag = 0
        locked_clues = [] # list of clues around which no more mines can be placed
        for j in range(len(path)): # look thru path, find which clue it's currently on
            if path[j][2] == i: # if item in path belongs to clue i
                placed_count += 1 # indicates that one mine has been placed for i
            if placed_count == # == value of clue minus flags around it
                flag = 1 # clue i is full
                locked_clues.append(i)  # adds clue i to list of locked clues
                break
        if flag == 0: # clue i was not full, so find open spots on clue i
            fringeable = []
            for j in range(len(ukn_list)): # looks thru all cells where mine can be placed
                if ukn_list[j][2] == i: # if that ukn is around clue i
                    fringeable.append(ukn_list[j][2]) # adds it to list of possible to add to fg
            unavailable = [] # list of cells that can't be added to fringe
            for j in range(len(locked_clues)): # for each locked clue
                for k in range(len(ukn_list)): # for each ukn cell
                    if ukn_list[k][2] == locked_clues[j]: # if the ukn cell is around a locked clue
                        unavailable.append(ukn_list[k][2]) # add to list of unavailable
            for j in range(len(fringeable)): # look through fringeable
                if fringeable[j] in unavailable: # it that cell is in list of unavailables
                    del(fringeable[j]) # remove it from list
        break # exit the loop of clues, i
    fg.append(fringeable) # add fringeable cells to fringe
    fringed.append(fringeable) # cells that are added to fringe are added to list of fringed
    for i in range(len(fringeable)): # add st to fg_parents len(fringeable) times
        fg_parents.append(st)


#############################################################################################################
##############################################################################################################
# Driver script.
environment = [[1, -1, 2],[0, 0, -1],[0, 0, 0]]
clues ={(0, 0): 1, (0, 2): 2} # index = vert, horiz
#mine_or_safe = {(0,0):0, (0,2):0, (0,1):-2}
print(ukn_list(clues,environment,mine_or_safe))
