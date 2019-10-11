import random

def base_agent(environment, total_mines):
    mine_or_safe = {} #0 if cell is safe, -1 if bomb, -2 if flagged
    num_safe= {} #number of safe cells identified around each cell
    num_mines={} # number of mines identified around each cell
    num_hidden_squares={} # number of untraversed cells around each cell
    discovered={} #List of cells that have been explored/are known already so we don't have to explore them
    safes=[] # List of untraversed safe cells that the program should check. 
    size=len(environment)*len(environment)
    cells_accounted=0
    mines_flagged=0
    while cells_accounted!=size:
        if len(safes)>0:
            (x,y)=safes[0]
            discovered[(x,y)]=0
            safes.pop(0)
            cells_accounted+=1
            
        else:
            (x,y)=(random.randint(0,len(environment)-1),random.randint(0,len(environment)-1))
            while (x,y) in discovered:
                (x,y)=(random.randint(0,len(environment)-1),random.randint(0,len(environment)-1))
            cells_accounted+=1

        if (environment[x][y]==-1):
            mine_or_safe[(x,y)]=-1
            discovered[(x,y)]=-1
        else:
            safe_num=0
            mines_num=0
            hidden_num=0
            mine_or_safe[(x,y)]=0
            discovered[(x,y)]=0
            curr_hidden=[]

            if ((x-1)>=0):
                    if (x-1,y) in mine_or_safe  and mine_or_safe[(x-1,y)]==0:
                        safe_num+=1
                    elif (x-1,y) in mine_or_safe  and mine_or_safe[(x-1,y)]==-1:
                        mines_num+=1
                    else:
                        hidden_num+=1
                        curr_hidden.append((x-1,y))
            if ((x+1)<len(environment)):
                    if (x+1,y) in mine_or_safe  and mine_or_safe[(x+1,y)]==0:
                        safe_num+=1
                    elif (x+1,y) in mine_or_safe  and mine_or_safe[(x+1,y)]==-1:
                        mines_num+=1
                    else:
                        hidden_num+=1
                        curr_hidden.append((x+1,y))
            if ((y-1)>=0):
                    if (x,y-1) in mine_or_safe and mine_or_safe[(x,y-1)]==0:
                        safe_num+=1
                    elif (x,y-1) in mine_or_safe  and mine_or_safe[(x,y-1)]==-1:
                        mines_num+=1
                    else:
                        hidden_num+=1
                        curr_hidden.append((x,y-1))
            if ((y+1)<len(environment)):
                    if (x,y+1) in mine_or_safe  and mine_or_safe[(x,y+1)]==0:
                        safe_num+=1
                    elif (x,y+1) in mine_or_safe  and mine_or_safe[(x,y+1)]==-1:
                        mines_num+=1
                    else:
                        hidden_num+=1
                        curr_hidden.append((x,y+1))
            if ((x-1)>=0 and (y-1)>=0):
                    if (x-1,y-1) in mine_or_safe  and mine_or_safe[(x-1,y-1)]==0:
                        safe_num+=1
                    elif (x-1,y-1) in mine_or_safe  and mine_or_safe[(x-1,y-1)]==-1:
                        mines_num+=1
                    else:
                        hidden_num+=1
                        curr_hidden.append((x-1,y-1))
            if ((x-1)>=0 and (y+1)<len(environment)):
                    if (x-1,y+1) in mine_or_safe  and mine_or_safe[(x-1,y+1)]==0:
                        safe_num+=1
                    elif (x-1,y+1) in mine_or_safe  and mine_or_safe[(x-1,y+1)]==-1:
                        mines_num+=1
                    else:
                        hidden_num+=1
                        curr_hidden.append((x-1,y+1))
            if ((x+1)<len(environment) and (y+1)<len(environment)):
                    if (x+1,y+1) in mine_or_safe  and mine_or_safe[(x+1,y+1)]==0:
                        safe_num+=1
                    elif (x+1,y+1) in mine_or_safe  and mine_or_safe[(x+1,y+1)]==-1:
                        mines_num+=1
                    else:
                        hidden_num+=1
                        curr_hidden.append((x+1,y+1))
            if ((x+1)<len(environment) and (y-1)>=0):
                    if (x+1,y-1) in mine_or_safe  and mine_or_safe[(x+1,y-1)]==0:
                        safe_num+=1
                    elif (x+1,y-1) in mine_or_safe  and mine_or_safe[(x+1,y-1)]==-1:
                        mines_num+=1
                    else:
                        hidden_num+=1
                        curr_hidden.append((x+1,y-1))

           
            num_safe[(x,y)]=safe_num
            num_mines[(x,y)]=mines_num
            num_hidden_squares[(x,y)]=hidden_num

            if environment[x][y]-num_mines[(x,y)]==num_hidden_squares[(x,y)]:#Checks if every hidden neighbor of current cell is a mine, and if so will add all hidden neighbors to safe_or_mine list as flagged since we don't want to select these spaces
                for (a,b) in curr_hidden:
                    mine_or_safe[(a,b)]=-2
                    discovered[(a,b)]=-2
                    cells_accounted+=1
                    mines_flagged+=1

            if 8-environment[x][y]-num_safe[(x,y)]==num_hidden_squares[(x,y)]:
                for (a,b) in curr_hidden:
                    mine_or_safe[(a,b)]=0
                    safes.append((a,b))


    print(mines_flagged, "mines found out of" ,total_mines, "total mines." )

        

        

            

        

                



