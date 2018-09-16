from __future__ import print_function
from colorama import Fore
from termcolor import colored
from collections import defaultdict

class City:
    def __init__(self):
        self.length = 122    #  8*15 + 2
        self.width = 34      # 4*8 + 2
        self.junc_len = self.length/8
        self.junc_wid = self.width/4
        self.city_map = ""
        self.roads = []
        self.junctions = []
        self.TwoDJunctions = {}
        self.OneDRoads = {}
        self.junction_roads = {}
        self.road_junctions = {}
        self.timer = 0
        self.borders = []

    def makeCity(self):
        self.city_map = [[' ' for x in range(0,self.length)] for y in range(0,self.width)]
        borders = []
        n = self.width/4
        m = self.length/8
        for i in range(n):
            borders.append((i,-1))
            borders.append((i,m))
        for i in range(m):
            borders.append((-1,i))
            borders.append((n,i))

        self.borders = borders
        self.insertObstacles()
        self.computeRoads()
        self.computeJunctions()
        self.map2Dto1DJunctions()
        self.map2Dto1DRoads()
        self.mapRoadsToJunctions()
        self.mapJunctionsToRoads()
        self.displayCity()


    def isAccomodate(self,x,y):
        if(self.city_map[x][y] == ' '):
            return True
        return False

    def computeRoads(self):
        roads = []
        for i in range(2,self.width-4,4):
            for j in range(6, self.length-7,8):
                roads.append([i,j])
            for j in range(6, self.length,8):
                roads.append([i+2,j-2])
        for j in range(6, self.length-11,8):
            roads.append([self.width-4,j])

        # print(roads)
        # exit()
        self.roads = roads

    def computeJunctions(self):
        junctions = []
        for i in range(2,self.width-3,4):
            for j in range(4, self.length-4,8):
                junctions.append([i,j])

        # print(junctions)
        # exit()
        self.junctions = junctions

    def map2Dto1DJunctions(self):
        junc_mapping = {}
        factor = self.length/8
        junctions = self.junctions
        for junc in range(len(junctions)):
            junction = (junc/factor, junc%factor)
            junc_mapping[junction] = junc

        # print(junc_mapping)
        # exit()
        self.TwoDJunctions = junc_mapping

    def findIndexOfRoad(self,road):
        rd = (road[0], road[1])
        if self.OneDRoads[rd] >= 0:
            return self.OneDRoads[rd]
        return -1

    def map2Dto1DRoads(self):
        road_mapping = {}
        for i in range(len(self.roads)):
            road = (self.roads[i][0],self.roads[i][1])
            road_mapping[road] = i

        # print(road_mapping)
        # exit()
        self.OneDRoads = road_mapping

    def mapRoadsToJunctions(self):
        junction_roads = defaultdict(list)
        for i in range(len(self.junctions)):
            junction_roads[i] = []

        for i in range(len(self.junctions)):
            junc = self.junctions[i]
            if(self.city_map[junc[0]][junc[1]-6] != 'X' and junc[1]-6 >= 0):
                road = [junc[0],junc[1]-6]
                road_index = self.findIndexOfRoad(road)
                if road_index!=-1:
                    junction_roads[i].append(road_index)
            if(self.city_map[junc[0]][junc[1]+2] != 'X' and junc[1]+2<self.length):
                road = [junc[0],junc[1]+2]
                road_index = self.findIndexOfRoad(road)
                if road_index!=-1:
                    junction_roads[i].append(road_index)
            if(self.city_map[junc[0]-2][junc[1]] != 'X' and junc[0]-2 >= 0):
                road = [junc[0]-2,junc[1]]
                road_index = self.findIndexOfRoad(road)
                if road_index!=-1:
                    junction_roads[i].append(road_index)
            if(self.city_map[junc[0]+2][junc[1]] != 'X' and junc[0]+2< self.width):
                road = [junc[0]+2,junc[1]]
                road_index = self.findIndexOfRoad(road)
                if road_index!=-1:
                    junction_roads[i].append(road_index)

        self.junction_roads = junction_roads

    def mapJunctionsToRoads(self):
        road_junctions = defaultdict(list)
        roads = self.roads
        junctions = self.junctions
        junction_roads = self.junction_roads
        for i in range(len(roads)):
            road_junctions[i] = []
        for junc in junction_roads:
            for road in junction_roads[junc]:
                road_junctions[road].append(junc)

        # print(road_junctions)
        # exit()
        self.road_junctions = road_junctions

    def insertObstacles(self):
    	for i in range(0,2):
    		for j in range(0,self.length):
    			self.city_map[i][j] = 'X'

    	for i in range(2,self.width-2):
    		for j in range(0,4):
    			self.city_map[i][j] = 'X'

    	for i in range(2,self.width-2):
    		for j in range(self.length-4,self.length):
    			self.city_map[i][j] = 'X'

    	for i in range(self.width-2,self.width):
    		for j in range(0,self.length):
    			self.city_map[i][j] = 'X'

        for i in range(2,self.width-2):
            if i%4==1 or i%4==0:
                for j in range(4,self.length-6):
                    if j%8==3 or j%8==2 or j%8==1 or j%8==0 or j%8==7 or j%8==6:
                        self.city_map[i][j] = 'X'

        self.city_map[6][20] = "D"
        for i in range(6,8):
            for j in range(20,22):
                self.city_map[i][j] = 'D'

        # self.city_map[2][12] = "O"
        # self.city_map[3][9] = "O"
        # self.city_map[3][17] = "O"
        # self.city_map[2][19] = "O"
        # self.city_map[2][27] = "O"
        # self.city_map[2][32] = "O"
        # self.city_map[5][20] = "O"
        # self.city_map[3][24] = "O"
        # self.city_map[6][14] = "O"
        # self.city_map[7][18] = "O"
        # self.city_map[6][17] = "O"
        # self.city_map[7][25] = "O"
        # self.city_map[6][27] = "O"
        # self.city_map[7][33] = "O"
        # self.city_map[10][13] = "O"
        # self.city_map[10][25] = "O"
        # self.city_map[11][17] = "O"
        # self.city_map[11][26] = "O"

    def displayCity(self):
        for i in range(0,self.width):
            for j in range(0,self.length):
                if self.city_map[i][j] == 'X':
                    print(Fore.YELLOW+self.city_map[i][j],end='')
                elif self.city_map[i][j] == 'O':
                    print(Fore.MAGENTA+self.city_map[i][j],end='')
                elif self.city_map[i][j] == 'D':
                    print(Fore.GREEN+self.city_map[i][j],end='')
                else:
                    print(Fore.CYAN+self.city_map[i][j],end='')
            print()
