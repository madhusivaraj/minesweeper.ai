
#########################################################
def ukn_list(clues, environment, mine_or_safe):
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

####################################################################
def validation(path, clue_minus_flags): # look around each clue_minus_flags, see if has appropriate num of mines placed
    for i in range(len(clue_minus_flags)): # for each clue
        counter = 0
        for j in range(len(path)): # for each item in path
            if path[j][2] == i: # if that item belongs to clue i
                counter += 1 # tally it
        if counter != clue_minus_flags[i]: # if mines for clue i isn't the right number
            return 0 # it's not a valid path
    return 1 # if not problems, it is a valid path

########################################################################################################################
# "DRIVER SCRIPT"
environment = [[1, -1, 2],[0, 0, -1],[0, 0, 0]]
clues ={(0, 0): 1, (0, 2): 2} # index = vert, horiz
mine_or_safe = {(0,0):0, (0,2):0, (0,1):-2}

#######################################################################################################################
######################################################################################################################
dim = len(environment)
[ukn_list, clue0mines, clue_minus_flags] = ukn_list(clues,environment,mine_or_safe) # fcn(clues,enviro) to list ukns as (x, y, i), where i (FROM 0) is index of ukn in clue list

ukn_per_clue = []# list, num ukn cells around each clue. clue indicated by list index
for i in range(len(clues)):
    ukn_per_clue_count = 0
    for j in range(len(ukn_list)):
        if ukn_list[j][2] == i:
            ukn_per_clue_count += 1
        ukn_per_clue.append(ukn_per_clue_count) # creates ukn_per_clue

#num_clues = len(clues)# number of clues in clue dict
num_clues = 0 # number of clues represented in ukn_list
clue_num_prev = -1
for i in range(len(ukn_list)):
    if ukn_list[i][2] != clue_num_prev:
        num_clues += 1
        clue_num_prev = ukn_list[i][2]

fg = []# fringe; start w list of all ukns around first clue (ukns w index i=0)
fringed = [] # list of items added to fringe
fg_parents = [] # parents of items added to fringe
for i in range(len(clue_minus_flags)): # determine 1st clue that is not locked
    if clue_minus_flags[i] != 0:
        first_good_clue = i
for i in range(len(ukn_list)):
    if ukn_list[i][2] == first_good_clue:
        fg.append(ukn_list[i])
        fringed.append(ukn_list[i])
        fg_parents.append(()) # for first ones put in list, parents are empty

all_valids = []

while len(fg) != 0: # Depth First Search
    print('len fg',len(fg))
    st = fg[len(fg)-1] # state = newest item in fg
    fg.pop(len(fg)-1) # removes new st from fg

    # Build current path (mine config).
    path = []
    path.append(st) # first item in path is last mine placed
    print('st',st)
    print('path1',path)
    from_1st = 0
    while from_1st < clue0mines: # while last item in path is not the first mine placed
        if st[2] == 0: # if current mine was around 1st clue
            from_1st += 1
        for i in range(len(fringed)):
            if fringed[i] == st:
                st_pos = i
                break
        st_parent = fg_parents[st_pos]
        path.append(st_parent)
        st = st_parent
    #path.pop(len(path)-1) # removes empty item at end
    path.reverse() # reverses orde

    if st[2] == num_clues: # If working from final clue, check config validity.
        if len(path) == sum(clue_minus_flags): # run to see if placed enough mines
            if validation(path, clue_minus_flags) == 1: # run validation fcn on the config to see if valid; 1 is valid, 0 not
                all_valids.append(path) # save this config to list of valid configs

    # For all, update lists and put children in fringe.
        # find valid ch, put ch end of fg, put ch end of fringed, put st end of fg_parents
        # look thru path until find clue that isnt full. pull ukns not in path yet, AND NOT locked, add to fg
        # when adding to fringe, ask: what can the next step possibly be?
            # will be open spot on current clue, or open spot on next clue
    for i in range(num_clues): # for each clue in ordered list of clues
        print('this i',i)

        placed_count = 0
        flag = 0
        locked_clues = [] # list of clues around which no more mines can be placed

        for j in range(len(path)): # look thru path, find which clue path ended on
            if path[j][2] == i: # if item in path belongs to clue i
                print('path item',path[j][2])
                placed_count += 1 # indicates that one mine has been placed for i

            print('placed_count',placed_count)
            print('clue minus flags i',clue_minus_flags[i])
            if placed_count == clue_minus_flags[i]: # clue_minus_flags is value of clue minus flags around it
                flag = 1 # clue i is full
                locked_clues.append(i)  # adds clue i to list of locked clues
                print('know lock?')
                break

        if flag == 0: # clue i was not full, so find open spots on clue i
            print('heeeeeeeeeeeeeeeeey')
            fringeable = []
            for j in range(len(ukn_list)): # looks thru all cells where mine can be placed
                if ukn_list[j][2] == i: # if that ukn is around clue i
                    #print(i)
                    #print(ukn_list[j])
                    fringeable.append(ukn_list[j]) # adds it to list of possible to add to fg
            unavailable = [] # list of cells that can't be added to fringe
            for j in range(len(locked_clues)): # for each locked clue
                for k in range(len(ukn_list)): # for each ukn cell
                    if ukn_list[k][2] == locked_clues[j]: # if the ukn cell is around a locked clue
                        unavailable.append(ukn_list[k]) # add to list of unavailable
            for j in range(len(fringeable)): # look through fringeable
                if fringeable[j] in unavailable: # it that cell is in list of unavailables
                    del(fringeable[j]) # remove it from list
        break # exit the loop of clues, i
    print('fringeable',fringeable)
    for i in range(len(fringeable)):
        fg.append(fringeable[i]) # add fringeable cells to fringe
        fringed.append(fringeable[i]) # cells that are added to fringe are added to list of fringed
    for i in range(len(fringeable)): # add st to fg_parents len(fringeable) times
        fg_parents.append(st)



#############################################################################################################
##############################################################################################################
# Driver script.
#environment = [[1, -1, 2],[0, 0, -1],[0, 0, 0]]
#clues ={(0, 0): 1, (0, 2): 2} # index = vert, horiz
#mine_or_safe = {(0,0):0, (0,2):0, (0,1):-2}
#print(ukn_list(clues,environment,mine_or_safe))

print('all valids' ,all_valids)