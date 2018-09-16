from __future__ import print_function
from colorama import Fore
from termcolor import colored
from collections import defaultdict

class City:
    def __init__(self):
        self.length = 164
        self.width = 46
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
        self.insertRoads()
        self.computeRoads()
        self.computeJunctions()
        self.displayCity()
        self.mapRoadsToJunctions()
        self.mapJunctionsToRoads()
        self.map2Dto1DJunctions()
        self.map2Dto1DRoads()

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
        for j in range(6, self.length-12,8):
            roads.append([42,j])

        self.roads = roads

    def computeJunctions(self):
        junctions = []
        for i in range(2,self.width-3,4):
            for j in range(4, self.length-7,8):
                junctions.append([i,j])

        self.junctions = junctions

    def map2Dto1DJunctions(self):
        junc_mapping = {}
        factor = self.length/8
        junctions = self.junctions
        for junc in range(len(junctions)):
            junction = (junc/factor, junc%factor)
            junc_mapping[junction] = junc

        self.TwoDJunctions = junc_mapping

    def findIndexOfRoad(self,road):
        for i in range(len(self.roads)):
            if(self.roads[i] == road):
                return i

    def map2Dto1DRoads(self):
        road_mapping = {}
        for i in range(len(self.roads)):
            road = (self.roads[i][0],self.roads[i][1])
            road_mapping[road] = i

        self.OneDRoads = road_mapping

    #OPTIMISE!
    def mapRoadsToJunctions(self):
        junction_roads = defaultdict(list)
        for i in range(len(self.junctions)):
            junction_roads[i] = []
        roads = self.roads
        junctions = self.junctions
        for i in range(len(self.junctions)):
            junc = self.junctions[i]
            if(self.city_map[junc[0]][junc[1]-6] != 'X'):
                road = [junc[0],junc[1]-6]
                road_index = self.findIndexOfRoad(road)
                if road_index is not None:
                    junction_roads[i].append(road_index)
            if(self.city_map[junc[0]][junc[1]+2] != 'X'):
                road = [junc[0],junc[1]+2]
                road_index = self.findIndexOfRoad(road)
                if road_index is not None:
                    junction_roads[i].append(road_index)
            if(self.city_map[junc[0]-2][junc[1]] != 'X'):
                road = [junc[0]-2,junc[1]]
                road_index = self.findIndexOfRoad(road)
                if road_index is not None:
                    junction_roads[i].append(road_index)
            if(self.city_map[junc[0]+2][junc[1]] != 'X'):
                road = [junc[0]+2,junc[1]]
                road_index = self.findIndexOfRoad(road)
                if road_index is not None:
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

        self.road_junctions = road_junctions

    def insertRoads(self):
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

        self.city_map[22][84] = "D"
        for i in range(22,24):
            for j in range(84,86):
                self.city_map[i][j] = 'D'

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
