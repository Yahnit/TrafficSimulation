from city import City
from vehicle import Vehicle
import random, os
from alarmexception import *
from getchunix import *
from colorama import Fore
from collections import defaultdict
import time

class CentralServer:
    def __init__(self):
        self.name = "Central Server"
        self.id = "srvr735"
        self.traffic_flow = {}
        self.junction_flow = {}
        self.vehicles_path = {}
        self.MAX_VEHICLES = 20
        self.utilities = {}
        self.timer = 0

    def startSimulation(self):
        self.constructCity()
        self.setupServer()
        self.createVehicles()
        # self.TestCreateVehicles()
        self.updateCity()
        self.tickSimulation()
        # self.testTickSimulation()

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
                self.vehicles[num_vehicles].next_junction = (x,y)
                self.city.city_map[x_pos][y_pos] = 'O'
                num_vehicles += 1
            if num_vehicles == self.MAX_VEHICLES:
                break

        # MARK DESTINATION IN THE CITY MAP
        dest_x = (self.vehicles[0].destination[0][0])*4 + 2
        dest_y = (self.vehicles[0].destination[0][1])*8 + 4
        self.city.city_map[dest_x][dest_y] = "D"
        for i in range(dest_x,dest_x+2):
            for j in range(dest_y,dest_y+2):
                self.city.city_map[i][j] = 'D'



    def TestCreateVehicles(self):
        self.MAX_VEHICLES = 1
        self.vehicles = [' ' for x in range(0,self.MAX_VEHICLES)]
        num_vehicles = 0

        while True:
            x = random.randint(self.city.junc_wid-1,self.city.junc_wid-1)
            y = random.randint(0, 0)
            x_pos = x*4 + 2
            y_pos = y*8 + 4
            if self.city.isAccomodate(x_pos,y_pos):
                self.vehicles[num_vehicles] = Vehicle(x_pos,y_pos,self.city)
                self.vehicles[num_vehicles].initialize(self.city.junc_wid, self.city.junc_len)
                self.vehicles[num_vehicles].speed = num_vehicles%2
                self.vehicles[num_vehicles].present_junction = (x,y)
                self.vehicles[num_vehicles].next_junction = (x,y)
                self.vehicles[num_vehicles].destination = [(1,self.city.junc_len-1)]
                self.city.city_map[x_pos][y_pos] = 'O'
                num_vehicles += 1
            if num_vehicles == self.MAX_VEHICLES:
                break

        # MARK DESTINATION IN THE CITY MAP
        dest_x = (self.vehicles[0].destination[0][0])*4 + 2
        dest_y = (self.vehicles[0].destination[0][1])*8 + 4
        self.city.city_map[dest_x][dest_y] = "D"
        for i in range(dest_x,dest_x+2):
            for j in range(dest_y,dest_y+2):
                self.city.city_map[i][j] = 'D'

        self.temp_vehicles = []
        self.MAX_TEMP_VEHICLES = 0


    def testTickSimulation(self):
        while True:
            self.timer += 1
            inpt = self.input_to()
            self.updateCity()
            self.findRoadTrafficFlow(self.city.city_map, self.city.roads)
            # self.findJunctionTrafficFlow(self.city.city_map, self.city.junctions)

            if self.timer%3 == 0:
                x = random.randint(0,0)
                y = random.randint(self.city.junc_len-2,self.city.junc_len-2)
                x_pos = random.randint(x*4 + 2, x*4 + 3)
                y_pos = random.randint(y*8 + 4, y*8 + 5)
                if self.city.isAccomodate(x_pos,y_pos):
                    self.temp_vehicles.append(Vehicle(x_pos,y_pos,self.city))
                    self.temp_vehicles[self.MAX_TEMP_VEHICLES].present_junction = (x,y)
                    self.temp_vehicles[self.MAX_TEMP_VEHICLES].next_junction = (self.city.junc_wid-1,self.city.junc_len-2)
                    self.city.city_map[x_pos][y_pos] = 'O'
                    self.MAX_TEMP_VEHICLES += 1

            if self.timer%4 -1 == 0:
                x = random.randint(self.city.junc_wid/2,self.city.junc_wid/2)
                y = random.randint(0,0)
                x_pos = random.randint(x*4 + 2, x*4 + 3)
                y_pos = random.randint(y*8 + 4, y*8 + 5)
                if self.city.isAccomodate(x_pos,y_pos):
                    self.temp_vehicles.append(Vehicle(x_pos,y_pos,self.city))
                    self.temp_vehicles[self.MAX_TEMP_VEHICLES].present_junction = (x,y)
                    self.temp_vehicles[self.MAX_TEMP_VEHICLES].next_junction = (self.city.junc_wid/2, self.city.junc_len-1)
                    self.city.city_map[x_pos][y_pos] = 'O'
                    self.MAX_TEMP_VEHICLES += 1

            for vhcl in range(self.MAX_VEHICLES):
                # self.vehicles_path[vhcl].append([self.vehicles[vhcl].x,self.vehicles[vhcl].y])
                if self.vehicles[vhcl].reached_junction:
                    self.vehicles[vhcl].value_iteration(self.city.junc_wid,self.city.junc_len,self.city.borders, self.traffic_flow, self.city.TwoDJunctions, self.city.junction_roads)
                self.vehicles[vhcl].traverseToJunctionVI(self.city.junctions,self.vehicles[vhcl].next_junction ,self.city.city_map)

            for vhcl in range(self.MAX_TEMP_VEHICLES):
                self.temp_vehicles[vhcl].traverseToJunctionVI(self.city.junctions,self.temp_vehicles[vhcl].next_junction ,self.city.city_map)

            if(inpt == 'q' or inpt == 'Q'):
                exit()

            if(inpt == 'x'):
                self.vehicles[0].print_utilities(self.vehicles[0].utilities,self.city.width/4,self.city.length/8)
                time.sleep(3)


    def tickSimulation(self):
        while True:
            self.timer += 1
            inpt = self.input_to()
            self.updateCity()
            self.findRoadTrafficFlow(self.city.city_map, self.city.roads)
            # self.findJunctionTrafficFlow(self.city.city_map, self.city.junctions)

            self.utilities = self.vehicles[0].value_iteration_advanced(self.city.junc_wid,self.city.junc_len,self.city.borders, self.traffic_flow, self.city.TwoDJunctions, self.city.junction_roads)
            # self.vehicles[1].value_iteration_native(self.city.junc_wid,self.city.junc_len,self.city.borders, self.traffic_flow, self.city.TwoDJunctions, self.city.junction_roads)

            for vhcl in range(self.MAX_VEHICLES):
                # self.vehicles_path[vhcl].append([self.vehicles[vhcl].x,self.vehicles[vhcl].y])
                if self.vehicles[vhcl].reached_junction:
                    # utils = self.vehicles[vhcl].value_iteration_advanced(self.city.junc_wid,self.city.junc_len,self.city.borders, self.traffic_flow, self.city.TwoDJunctions, self.city.junction_roads)
                    # self.vehicles[vhcl].setNextJunc(utils)
                    self.vehicles[vhcl].setNextJunc(self.utilities)

                self.vehicles[vhcl].traverseToJunctionVI(self.city.junctions,self.vehicles[vhcl].next_junction ,self.city.city_map)

            if(inpt == 'q' or inpt == 'Q'):
                exit()

            if(inpt == 'x'):
                self.vehicles[0].print_utilities(self.vehicles[0].utilities,int(self.city.width/4),int(self.city.length/8))
                time.sleep(3)


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
