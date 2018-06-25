from __future__ import print_function
import random
from copy import deepcopy

class Vehicle:
    def __init__(self,x,y,city):
        self.x = x
        self.y = y
        self.source = []
        self.destination = []
        self.present_road = ""
        self.present_junction = ""
        self.next_junction = ""
        self.reached_junction = True
        self.path_travelled = []
        self.grid = [[ -0.2 for x in range(0,city.junc_len)] for y in range(0,city.junc_wid)]
        self.utilities = {}
        self.initial_utilities = {}
        self.states = []
        self.speed = 0

    def initialize(self,n,m):
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
        self.initial_utilities = utilities
        self.states = states

    def moveRight(self,x,y,screen):
        for j in range(1,self.speed+2):
            is_move = 1
            for i in range(1,self.speed+2-j+1 ):
                if not (screen[x][y+i] == " " or screen[x][y+i] == "D"):
                    is_move = 0
            if is_move == 1:
                break

        if is_move == 1:
            screen[x][y] = " "
            screen[x][y+self.speed+2-j] = 'O'
            self.x, self.y = x ,y+self.speed+2-j
            return True
        return False

    def moveLeft(self,x,y,screen):
        for j in range(1,self.speed+2):
            is_move = 1
            for i in range(1,self.speed+2-j+1 ):
                if not (screen[x][y-i] == " " or screen[x][y-i] == "D"):
                    is_move = 0
            if is_move == 1:
                break

        if is_move == 1:
            screen[x][y] = " "
            screen[x][y-self.speed-2+j] = 'O'
            self.x, self.y = x ,y-self.speed-2+j
            return True
        return False

    def moveUp(self,x,y,screen):
        for j in range(1,self.speed+2):
            is_move = 1
            for i in range(1,self.speed+2-j+1 ):
                if not (screen[x-i][y] == " " or screen[x-i][y] == "D"):
                    is_move = 0
            if is_move == 1:
                break

        if is_move == 1:
            screen[x][y] = " "
            screen[x-self.speed-2+j][y] = 'O'
            self.x, self.y = x-self.speed-2+j ,y
            return True

    def moveDown(self,x,y,screen):
        for j in range(1,self.speed+2):
            is_move = 1
            for i in range(1,self.speed+2-j+1 ):
                if not (screen[x+i][y] == " " or screen[x+i][y] == "D"):
                    is_move = 0
            if is_move == 1:
                break

        if is_move == 1:
            screen[x][y] = " "
            screen[x+self.speed+2-j][y] = 'O'
            self.x, self.y = x +self.speed+2-j,y
            return True
        return False


    # def moveRight(self,x,y,screen):
    #     if screen[x][y+1] == " " or screen[x][y+1] == "D":
    #         screen[x][y] = " "
    #         screen[x][y+1] = 'O'
    #         self.x, self.y = x ,y+1
    #         return True
    #     return False
    #
    # def moveLeft(self,x,y,screen):
    #     if screen[x][y-1] == " " or screen[x][y-1] == "D":
    #         screen[x][y] = " "
    #         screen[x][y-1] = 'O'
    #         self.x, self.y = x ,y-1
    #         return True
    #     return False
    #
    # def moveUp(self,x,y,screen):
    #     if screen[x-1][y] == " " or screen[x-1][y] == "D":
    #         screen[x][y] = " "
    #         screen[x-1][y] = 'O'
    #         self.x, self.y = x-1 ,y
    #         return True
    #     return False
    #
    # def moveDown(self,x,y,screen):
    #     if screen[x+1][y] == " " or screen[x+1][y] == "D":
    #         screen[x][y] = " "
    #         screen[x+1][y] = 'O'
    #         self.x, self.y = x+1 ,y
    #         return True
    #     return False

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
                self.moveRight(x_pos, y_pos,city_map)
                self.reached_junction = False
            elif y_pos > junc_y+1:
                self.moveLeft(x_pos, y_pos,city_map)
                self.reached_junction = False
            elif y_pos == junc_y or y_pos == junc_y+1:
                self.stayStill(x_pos, y_pos,city_map)
                self.reached_junction = True
                self.present_junction = (x_pos/4, y_pos/8)

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
                self.present_junction = (x_pos/4, y_pos/8)

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
                self.present_junction = (x_pos/4, y_pos/8)

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
                self.present_junction = (x_pos/4, y_pos/8)

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

    def print_utilities(self, utils, n, m):
        for i in range(n):
            for j in range(m):
                print ("%.3f" %utils[(i,j)], end=" ")
            print ("\n")

    def get_actions(self, state, borders):
        if state in self.destination or state in borders:
            return []
        return [(1,0), (0,1), (-1,0), (0,-1)]

    def transition(self, state,action,borders):
        if (state[0]+action[0],state[1]+action[1]) not in borders:
            more_prob = (1, (state[0]+action[0],state[1]+action[1]))
        else:
            more_prob = (1, (state[0],state[1]))

        return more_prob

    def find_max_utility_state(self,utilities,present_junction):
        max_vals = []
        maxm = -100000
        if(utilities[(present_junction[0]-1, present_junction[1])] > maxm):
            maxm = utilities[(present_junction[0]-1, present_junction[1])]
        if(utilities[(present_junction[0]+1, present_junction[1])] > maxm):
            maxm = utilities[(present_junction[0]+1, present_junction[1])]
        if(utilities[(present_junction[0], present_junction[1]-1)] > maxm):
            maxm = utilities[(present_junction[0], present_junction[1]-1)]
        if(utilities[(present_junction[0], present_junction[1]+1)] > maxm):
            maxm = utilities[(present_junction[0], present_junction[1]+1)]

        if utilities[(present_junction[0]-1, present_junction[1])] == maxm:
            max_vals.append((present_junction[0]-1, present_junction[1]))
        if utilities[(present_junction[0]+1, present_junction[1])] == maxm:
            max_vals.append((present_junction[0]+1, present_junction[1]))
        if utilities[(present_junction[0], present_junction[1]-1)] == maxm:
            max_vals.append((present_junction[0], present_junction[1]-1))
        if utilities[(present_junction[0], present_junction[1]+1)] == maxm:
            max_vals.append((present_junction[0], present_junction[1]+1))

        if utilities[max_vals[0]] < utilities[(present_junction[0], present_junction[1])]:
            return present_junction

        return max_vals[random.randint(0,len(max_vals)-1)]

    def value_iteration(self, n, m, borders):
        grid = self.grid
        grid[5][10] = 10
        self.destination = [(5,10)]
        utilities = self.initial_utilities
        states = self.states

        while 1:
            is_change = 0
            temp_utilities = deepcopy(utilities)
            for state in states:
                maxm = -100000.0
                if self.get_actions(state, borders) != []:
                    for action in self.get_actions(state, borders):
                        trans = self.transition(state,action,borders)
                        sum_ut = 0.0
                        sum_ut += trans[0] * temp_utilities[trans[1]]
                        if maxm < sum_ut:
                            maxm = sum_ut

                if self.get_actions(state, borders) == []:
                    maxm = 0

                utilities[state] = grid[state[0]][state[1]] + maxm
                if abs(utilities[state] - temp_utilities[state]) > abs(0.1*utilities[state]):
                    is_change = 1

            if not is_change:
                best_move = self.find_max_utility_state(utilities, self.present_junction)
                self.next_junction = best_move
                self.utilities = utilities
                return best_move
