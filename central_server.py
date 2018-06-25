from city import City
from vehicle import Vehicle
import random, os
from alarmexception import *
from getchunix import *
from colorama import Fore
from collections import defaultdict

class CentralServer:
    def __init__(self):
        self.name = "Central Server"
        self.id = "srvr735"
        self.traffic_flow = {}
        self.junction_flow = {}
        self.vehicles_path = {}
        self.MAX_VEHICLES = 20
        self.timer = 0

    def startSimulation(self):
        self.constructCity()
        self.setupServer()
        self.createVehicles()
        self.updateCity()
        self.tickSimulation()

    def constructCity(self):
        city = City()
        city.makeCity()
        getch  = GetchUnix()
        self.city = city
        self.getch = getch

    def setupServer(self):
        self.initializeVehiclesPath(self.MAX_VEHICLES)
        self.findRoadTrafficFlow(self.city.city_map, self.city.roads)
        self.findJunctionTrafficFlow(self.city.city_map, self.city.junctions)

    def createVehicles(self):
        self.vehicles = [' ' for x in range(0,self.MAX_VEHICLES)]
        num_vehicles = 0

        while True:
            x = random.randint(0,self.city.junc_wid-1)
            y = random.randint(0,self.city.junc_len-1)
            x_pos = x*4 + 2
            y_pos = y*8 + 4
            if self.city.isAccomodate(x_pos,y_pos):
                self.vehicles[num_vehicles] = Vehicle(x_pos,y_pos,self.city)
                self.vehicles[num_vehicles].initialize(self.city.junc_wid, self.city.junc_len)
                self.vehicles[num_vehicles].speed = num_vehicles%2
                self.vehicles[num_vehicles].present_junction = (x,y)
                self.city.city_map[x_pos][y_pos] = 'O'
                num_vehicles += 1
            if num_vehicles == self.MAX_VEHICLES:
                break

    def tickSimulation(self):
        while True:
            self.timer += 1
            inpt = self.input_to()
            self.updateCity()
            self.findRoadTrafficFlow(self.city.city_map, self.city.roads)
            self.findJunctionTrafficFlow(self.city.city_map, self.city.junctions)

            for vhcl in range(self.MAX_VEHICLES):
                self.vehicles_path[vhcl].append([self.vehicles[vhcl].x,self.vehicles[vhcl].y])
                if self.vehicles[vhcl].reached_junction:
                    self.vehicles[vhcl].value_iteration(self.city.junc_wid,self.city.junc_len,self.city.borders)
                self.vehicles[vhcl].traverseToJunctionVI(self.city.junctions,self.vehicles[vhcl].next_junction ,self.city.city_map)

            if(inpt == 'q' or inpt == 'Q'):
                exit()

    def findRoadTrafficFlow(self, screen, roads):
        traffic_flow = defaultdict(list)
        for road in range(len(roads)):
            num_vehicles = 0
            if roads[road][0]%4:
                for i in range(roads[road][0],roads[road][0]+2):
                    for j in range(roads[road][1],roads[road][1]+6):
                        if screen[i][j] == 'O':
                            num_vehicles += 1
            else:
                for i in range(roads[road][0],roads[road][0]+2):
                    for j in range(roads[road][1],roads[road][1]+2):
                        if screen[i][j] == 'O':
                            num_vehicles += 1
            traffic_flow[road] = num_vehicles

        self.traffic_flow = traffic_flow

    def findJunctionTrafficFlow(self, screen, junctions):
        junction_flow = defaultdict(list)
        for junction in range(len(junctions)):
            num_vehicles = 0
            for i in range(junctions[junction][0],junctions[junction][0]+2):
                for j in range(junctions[junction][1],junctions[junction][1]+2):
                    if screen[i][j] == 'O':
                        num_vehicles += 1
            junction_flow[junction] = num_vehicles

        self.junction_flow = junction_flow

    def initializeVehiclesPath(self, num_vehicles):
        for i in range(num_vehicles):
            self.vehicles_path[i] = []

    def updateCity(self):
        os.system('clear')
        self.city.displayCity()
        print(Fore.BLACK+"Press q to exit the simulation")
        print ("Timestamp: "+ str(self.timer))

    def alarmHandler(self,signum, frame):
        raise AlarmException

    def input_to(self,timeout=1):
        signal.signal(signal.SIGALRM, self.alarmHandler)
        signal.alarm(timeout)
        try:
            text = self.getch()
            signal.alarm(0)
            return text
        except AlarmException:
            print("\n ")
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return ''
