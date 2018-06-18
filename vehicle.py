from __future__ import print_function
import random
from copy import deepcopy

class Vehicle:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.source = []
        self.destination = []
        self.present_road = ""
        self.present_junction = ""
        self.reached_junction = False
        self.path_travelled = []

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
