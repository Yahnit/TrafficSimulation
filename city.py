from __future__ import print_function
from colorama import Fore
from termcolor import colored

class City:
    def __init__(self):
        self.__length = 76
        self.__width = 38
        self.city_map = ""

    def getLength(self):
        return self.__length

    def getWidth(self):
        return self.__width

    def setLength(self,x):
        self.__length = x

    def setWidth(self,y):
        self.__width = y

    def makeCity(self):
        self.city_map = [[' ' for x in range(0,76)] for y in range(0,38)]

    def isAccomodate(self,x,y):
        if(self.city_map[x][y] == ' '):
            return True
        return False

    def insertRoads(self):
		for i in range(0,2):
			for j in range(0,76):
				self.city_map[i][j] = 'X'

		for i in range(2,36):
			for j in range(0,4):
				self.city_map[i][j] = 'X'

		for i in range(2,36):
			for j in range(72,76):
				self.city_map[i][j] = 'X'

		for i in range(36,38):
			for j in range(0,76):
				self.city_map[i][j] = 'X'

		for i in range(2,36):
			if i%4==1 or i%4==0:
				for j in range(4,72):
					if j%8==3 or j%8==2 or j%8==1 or j%8==0:
						self.city_map[i][j] = 'X'

    def displayCity(self):
        for i in range(0,38):
            for j in range(0,76):
                if self.city_map[i][j] == 'X':
                    print(Fore.YELLOW+self.city_map[i][j],end='')
                elif self.city_map[i][j] == 'O':
                    print(Fore.MAGENTA+self.city_map[i][j],end='')
                else:
                    print(Fore.CYAN+self.city_map[i][j],end='')
            print()
