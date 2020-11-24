from __future__ import print_function
import random
from copy import deepcopy
import decimal
import time

class Vehicle:
    def __init__(self,x,y,city):
        self.x = x
        self.y = y
        self.source = []
        self.destination = [(1,2)]
        self.present_road = ""
        self.present_junction = ""
        self.next_junction = ""
        self.reached_junction = True
        self.path_travelled = []
        self.grid = [[ 0 for x in range(0,city.junc_len)] for y in range(0,city.junc_wid)]
        self.distanceFromDestination = [[ 0 for x in range(0,city.junc_len)] for y in range(0,city.junc_wid)]
        self.utilities = {}
        self.prev_utilities = {}
        self.zero_utilities = {}
        self.states = []
        self.speed = 0
        self.gamma = 0.9

    def initialize(self,n, m):
        utilities = {}
        states = []
        for i in range(n):
            for j in range(m):
                temp = (i,j)
                states.append(temp)
                utilities[temp] = 0
                self.distanceFromDestination[i][j] = abs(self.destination[0][0]-i)*4 + abs(self.destination[0][1]-j)*8

        for i in range(max(m,n)):
            temp = (i,-1)
            utilities[temp] = 0
            temp = (n,i)
            utilities[temp] = 0
            temp = (-1,i)
            utilities[temp] = 0
            temp = (i,m)
            utilities[temp] = 0
        self.prev_utilities = utilities
        self.zero_utilities = utilities
        self.states = states

    def getZeroUtils(self, n, m):
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
        return utilities


    def moveRight(self,x,y,screen):
        if screen[x][y+1] != "X":
            screen[x][y] = " "
            screen[x][y+1] = 'O'
            self.x, self.y = x ,y+1
            return True
        return False

    def moveLeft(self,x,y,screen):
        if screen[x][y-1] != "X":
            screen[x][y] = " "
            screen[x][y-1] = 'O'
            self.x, self.y = x ,y-1
            return True
        return False

    def moveUp(self,x,y,screen):
        if screen[x-1][y] != "X":
            screen[x][y] = " "
            screen[x-1][y] = 'O'
            self.x, self.y = x-1 ,y
            return True
        return False

    def moveDown(self,x,y,screen):
        if screen[x+1][y] != "X":
            screen[x][y] = " "
            screen[x+1][y] = 'O'
            self.x, self.y = x+1 ,y
            return True
        return False

    def stayStill(self,x,y,screen):
        if screen[x][y] != "X":
            screen[x][y] = 'O'
            self.x, self.y = x ,y
            return True
        return False

    def isAccomodate(self,x,y,screen):
        if(screen[x][y] != 'X'):
            return True
        return False

    def random_motion(self,screen):
        count = 0
        while count < 10:
            direction = random.randint(1,5)
            if direction==1:
                if self.moveUp(self.x, self.y, screen):
                    break

            elif direction==2:
                if self.moveDown(self.x, self.y,screen):
                    break

            elif direction==3:
                if self.moveRight(self.x, self.y,screen):
                    break

            elif direction==4:
                if self.moveLeft(self.x, self.y,screen):
                    break
            count+=1

    def traverseToJunctionVI(self, junctions, junction, city_map):
        x_pos, y_pos = self.x, self.y
        junc_x, junc_y = junction[0]*4+2, junction[1]*8+4
        if x_pos == junc_x:
            if y_pos < junc_y:
                if self.moveRight(x_pos, y_pos,city_map):
                    y_pos += 1
                self.reached_junction = False
            elif y_pos > junc_y+1:
                if self.moveLeft(x_pos, y_pos,city_map):
                    y_pos -= 1
                self.reached_junction = False
            if y_pos == junc_y or y_pos == junc_y+1:
                self.reached_junction = True
                self.present_junction = (int(x_pos/4), int(y_pos/8))

        if y_pos == junc_y:
            if x_pos < junc_x:
                if self.moveDown(x_pos, y_pos,city_map):
                    x_pos += 1
                self.reached_junction = False
            elif x_pos > junc_x+1:
                if self.moveUp(x_pos, y_pos,city_map):
                    x_pos -= 1
                self.reached_junction = False
            if x_pos == junc_x or x_pos == junc_x +1:
                self.reached_junction = True
                self.present_junction = (int(x_pos/4), int(y_pos/8))

        if x_pos-1 == junc_x:
            if y_pos < junc_y:
                if self.moveRight(x_pos, y_pos,city_map):
                    y_pos += 1
                self.reached_junction = False
            elif y_pos > junc_y+1:
                if self.moveLeft(x_pos, y_pos,city_map):
                    y_pos -= 1
                self.reached_junction = False
            if y_pos == junc_y or y_pos == junc_y+1:
                self.reached_junction = True
                self.present_junction = (int(x_pos/4), int(y_pos/8))

        if y_pos-1 == junc_y:
            if x_pos < junc_x:
                if self.moveDown(x_pos, y_pos,city_map):
                    x_pos += 1
                self.reached_junction = False
            elif x_pos > junc_x+1:
                if self.moveUp(x_pos, y_pos,city_map):
                    x_pos -= 1
                self.reached_junction = False
            if x_pos == junc_x or x_pos == junc_x +1:
                self.reached_junction = True
                self.present_junction = (int(x_pos/4), int(y_pos/8))

        self.path_travelled.append([self.x, self.y])

    def traverseToJunctionShortestPath(self, junctions, junction, city_map, num):
        x_pos, y_pos = self.x, self.y
        junc_x, junc_y = junctions[junction][0], junctions[junction][1]

        if x_pos == junc_x:
            if y_pos < junc_y:
                self.moveRight(x_pos, y_pos,city_map)
                self.reached_junction = False
            elif y_pos > junc_y+1:
                self.moveLeft(x_pos, y_pos,city_map)
                self.reached_junction = False
            elif y_pos == junc_y or y_pos == junc_y+1:
                self.stayStill(x_pos, y_pos,city_map)
                self.reached_junction = True
            self.path_travelled.append([self.x, self.y])
            return

        if y_pos == junc_y:
            if x_pos < junc_x:
                self.moveDown(x_pos, y_pos,city_map)
                self.reached_junction = False
            elif x_pos > junc_x+1:
                self.moveUp(x_pos, y_pos,city_map)
                self.reached_junction = False
            elif x_pos == junc_x or x_pos == junc_x +1:
                self.stayStill(x_pos, y_pos,city_map)
                self.reached_junction = True
            self.path_travelled.append([self.x, self.y])
            return

        if x_pos-1 == junc_x:
            if y_pos < junc_y:
                self.moveRight(x_pos, y_pos,city_map)
                self.reached_junction = False
            elif y_pos > junc_y+1:
                self.moveLeft(x_pos, y_pos,city_map)
                self.reached_junction = False
            elif y_pos == junc_y or y_pos == junc_y+1:
                self.stayStill(x_pos, y_pos,city_map)
                self.reached_junction = True
            self.path_travelled.append([self.x, self.y])
            return

        if y_pos-1 == junc_y:
            if x_pos < junc_x:
                self.moveDown(x_pos, y_pos,city_map)
                self.reached_junction = False
            elif x_pos > junc_x+1:
                self.moveUp(x_pos, y_pos,city_map)
                self.reached_junction = False
            elif x_pos == junc_x or x_pos == junc_x +1:
                self.stayStill(x_pos, y_pos,city_map)
                self.reached_junction = True
            self.path_travelled.append([self.x, self.y])
            return

        if num%3 == 0:
            if x_pos < junc_x:
                if self.moveDown(x_pos, y_pos,city_map):
                    self.reached_junction = False
                    self.path_travelled.append([self.x, self.y])
                    return

            if x_pos > junc_x:
                if self.moveUp(x_pos, y_pos,city_map):
                    self.reached_junction = False
                    self.path_travelled.append([self.x, self.y])
                    return

            if y_pos < junc_y:
                if self.moveRight(x_pos, y_pos,city_map):
                    self.reached_junction = False
                    self.path_travelled.append([self.x, self.y])
                    return

            if y_pos > junc_y:
                if self.moveLeft(x_pos, y_pos,city_map):
                    self.reached_junction = False
                    self.path_travelled.append([self.x, self.y])
                    return
        else:
            if y_pos < junc_y:
                if self.moveRight(x_pos, y_pos,city_map):
                    self.reached_junction = False
                    self.path_travelled.append([self.x, self.y])
                    return

            if y_pos > junc_y:
                if self.moveLeft(x_pos, y_pos,city_map):
                    self.reached_junction = False
                    self.path_travelled.append([self.x, self.y])
                    return

            if x_pos < junc_x:
                if self.moveDown(x_pos, y_pos,city_map):
                    self.reached_junction = False
                    self.path_travelled.append([self.x, self.y])
                    return

            if x_pos > junc_x:
                if self.moveUp(x_pos, y_pos,city_map):
                    self.reached_junction = False
                    self.path_travelled.append([self.x, self.y])
                    return

    def find_max_utility_state(self,utilities,present_junction):
        max_vals = []
        maxm = -100000000
        actions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        for act in actions:
            next_state = (present_junction[0] + act[0], present_junction[1] + act[1])
            # step_cost = self.get_step_cost(present_junction, act, traffic_flow, twoDJunctions, junction_roads, borders)
            # if self.gamma * utilities[next_state] + step_cost == maxm:
            if utilities[next_state] == maxm:
                max_vals.append(next_state)
            # if self.gamma * utilities[next_state] + step_cost > maxm:
            if utilities[next_state] > maxm:
                maxm = utilities[next_state]
                max_vals = [next_state]

        # if utilities[(present_junction[0]-1, present_junction[1])] > maxm:
        #     maxm = utilities[(present_junction[0]-1, present_junction[1])]
        # if utilities[(present_junction[0]+1, present_junction[1])] > maxm:
        #     maxm = utilities[(present_junction[0]+1, present_junction[1])]
        # if utilities[(present_junction[0], present_junction[1]-1)] > maxm:
        #     maxm = utilities[(present_junction[0], present_junction[1]-1)]
        # if utilities[(present_junction[0], present_junction[1]+1)] > maxm:
        #     maxm = utilities[(present_junction[0], present_junction[1]+1)]
        #
        # if utilities[(present_junction[0]-1, present_junction[1])] == maxm:
        #     max_vals.append((present_junction[0]-1, present_junction[1]))
        # if utilities[(present_junction[0]+1, present_junction[1])] == maxm:
        #     max_vals.append((present_junction[0]+1, present_junction[1]))
        # if utilities[(present_junction[0], present_junction[1]-1)] == maxm:
        #     max_vals.append((present_junction[0], present_junction[1]-1))
        # if utilities[(present_junction[0], present_junction[1]+1)] == maxm:
        #     max_vals.append((present_junction[0], present_junction[1]+1))

        if utilities[max_vals[0]] < utilities[present_junction]:
            return present_junction

        return max_vals[random.randint(0,len(max_vals)-1)]

    def print_utilities(self, utils, n, m):
        for i in range(n):
            for j in range(m):
                # print(utils[(i,j)], end=" ")
                print ("%1f" %utils[(i,j)], end=" ")
            print ("\n")
        print("\n")

    def get_actions(self, state, borders):
        actions = []
        if state in self.destination or state in borders:
            return actions
        if (state[0]+1,state[1]) not in borders:
            actions.append([1,0])
        if (state[0]-1,state[1]) not in borders:
            actions.append([-1,0])
        if (state[0],state[1]+1) not in borders:
            actions.append([0,1])
        if (state[0],state[1]-1) not in borders:
            actions.append([0,-1])
        return actions

    def transition(self, state,action,borders):
        if (state[0]+action[0],state[1]+action[1]) not in borders:
            more_prob = (1, (state[0]+action[0],state[1]+action[1]))
        else:
            more_prob = (1, (state[0],state[1]))

        return more_prob

    def get_step_cost(self,state, action, traffic_flow, twoDJunctions, junction_roads, borders):
        dest_state = (state[0]+action[0],state[1]+action[1])
        if dest_state in borders:
            return -1000
        pres_junc = twoDJunctions[state]
        dest_junc = twoDJunctions[dest_state]
        pres_roads = junction_roads[pres_junc]
        dest_roads = junction_roads[dest_junc]
        common_road = []

        for road in pres_roads:
            if road in dest_roads:
                common_road.append(road)

        if traffic_flow[common_road[0]]==0:
            return -0.2
        # if traffic_flow[common_road[0]]==1:
        #     return -0.5
        # if traffic_flow[common_road[0]]==2:
        #     return -0.6
        # if traffic_flow[common_road[0]]==3:
        #     return -0.8
        # if traffic_flow[common_road[0]]==4:
        #     return -0.9
        else:
            return -0.4*traffic_flow[common_road[0]]

    def setNextJunc(self, utilities):
        self.next_junction = self.find_max_utility_state(utilities, self.present_junction)
        return self.next_junction

    def value_iteration_advanced(self, n, m, borders, traffic_flow, twoDJunctions, junction_roads):
        grid = self.grid
        grid[self.destination[0][0]][self.destination[0][1]] = 10
        utilities = self.prev_utilities
        states = self.states

        # self.print_utilities(utilities, n, m)
        start_time = time.time()
        while 1:
            is_change = 0
            temp_utilities = deepcopy(utilities)
            for state in states:
                maxm = -100000.0
                if self.get_actions(state, borders) != []:
                    for action in self.get_actions(state, borders):
                        trans = self.transition(state,action,borders)
                        step_cost = self.get_step_cost(state, action, traffic_flow, twoDJunctions, junction_roads, borders)
                        sum_ut = trans[0] * (step_cost + self.gamma * temp_utilities[trans[1]])
                        if maxm < sum_ut:
                            maxm = sum_ut

                if self.get_actions(state, borders) == []:
                    maxm = 0

                utilities[state] = grid[state[0]][state[1]] + maxm
                if abs(utilities[state] - temp_utilities[state]) > abs(0.1*utilities[state]):
                    is_change = 1
            # print("VALUES ARE CHANGING......")
            if not is_change:
                end_time = time.time()
                # print("Time elapsed in Advanced VI : " + str(end_time - start_time))
                self.utilities = utilities
                self.prev_utilities = utilities
                return self.utilities

    def value_iteration_native(self, n, m, borders, traffic_flow, twoDJunctions, junction_roads):
        grid = self.grid
        grid[self.destination[0][0]][self.destination[0][1]] = 10
        utilities = self.getZeroUtils(n, m)
        states = self.states

        # self.print_utilities(utilities, n, m)
        start_time = time.time()
        while 1:
            is_change = 0
            temp_utilities = deepcopy(utilities)
            for state in states:
                maxm = -100000.0
                if self.get_actions(state, borders) != []:
                    for action in self.get_actions(state, borders):
                        trans = self.transition(state,action,borders)
                        step_cost = self.get_step_cost(state, action, traffic_flow, twoDJunctions, junction_roads, borders)
                        sum_ut = trans[0] * (step_cost + self.gamma * temp_utilities[trans[1]])
                        if maxm < sum_ut:
                            maxm = sum_ut

                if self.get_actions(state, borders) == []:
                    maxm = 0

                utilities[state] = grid[state[0]][state[1]] + maxm
                if abs(utilities[state] - temp_utilities[state]) > abs(0.1*utilities[state]):
                    is_change = 1
            # print("VALUES ARE CHANGING......")
            if not is_change:
                end_time = time.time()
                print("Time elapsed in Native VI : " + str(end_time - start_time))
                self.utilities = utilities
                return self.utilities
