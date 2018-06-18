from __future__ import print_function
from copy import deepcopy

def print_utilities(utils):
    for i in range(n):
        for j in range(m):
            print ("%.3f" %utils[(i,j)], end=" ")
        print ("\n")

def get_actions(state):
    if state in end_states or state in walls:
        return []
    return [(4,0), (0,8), (-4,0), (0,-8)]

def transition(state,action):
    if (state[0]+action[0],state[1]+action[1]) not in walls:
        more_prob = (1, (state[0]+action[0],state[1]+action[1]))
    else:
        more_prob = (1, (state[0],state[1]))

    return more_prob

def value_iteration():
    utilities = {}
    states = []
    for i in range(n):
        for j in range(m):
            temp = (i,j)
            states.append(temp)
            utilities[temp] = 0

    for i in range(max(m,n)):
        temp = (i,-1)
        utilities[temp] = 0
        temp = (n,i)
        utilities[temp] = 0
        temp = (-1,i)
        utilities[temp] = 0
        temp = (i,m)
        utilities[temp] = 0

    while 1:
        is_change = 0
        temp_utilities = deepcopy(utilities)
        for state in states:
            maxm = -100000.0
            if get_actions(state) != []:
                for action in get_actions(state):
                    trans = transition(state,action)
                    sum_ut = 0.0
                    sum_ut += trans[0] * temp_utilities[trans[1]]
                    if maxm < sum_ut:
                        maxm = sum_ut

            if get_actions(state) == []:
                maxm = 0

            utilities[state] = grid[state[0]][state[1]] + maxm
            if abs(utilities[state] - temp_utilities[state]) > abs(0.01*utilities[state]):
                is_change = 1

        print_utilities(utilities)
        print("\n")
        if not is_change:
            return utilities

# GET INPUT FROM USER
dimensions = raw_input("");
dimensions = dimensions.split(" ")
n = int(dimensions[0])
m = int(dimensions[1])

grid = []
for i in range(n):
    row = []
    row_inp = raw_input("")
    row_inp = row_inp.split(" ")
    for j in range(m):
        row.append(float(row_inp[j]))
    grid.append(row)
#print grid

terminal_walls = raw_input("");
terminal_walls = terminal_walls.split(" ")
e = int(terminal_walls[0])
w = int(terminal_walls[1])

end_states = []
for i in range(e):
    end_st = raw_input("")
    end_st = end_st.split(" ")
    end_states.append((int(end_st[0]),int(end_st[1])))
#print end_states

walls = []
for i in range(w):
    wall = raw_input("")
    wall = wall.split(" ")
    walls.append((int(wall[0]),int(wall[1])))
#print walls
for i in range(n):
    walls.append((i,-1))
    walls.append((i,m))
for i in range(m):
    walls.append((-1,i))
    walls.append((n,i))

strt = raw_input("")
strt = strt.split(" ")
start_state = (int(strt[0]),int(strt[1]))
#print start_state

step_reward = float(raw_input(""))
#print step_reward
for i in range(n):
    for j in range(m):
        if (i,j) not in end_states and (i,j) not in walls:
            grid[i][j] = grid[i][j] + step_reward


utils = value_iteration()
