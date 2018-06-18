from city import City
from vehicle import Vehicle
from central_server import CentralServer
import random, os
from alarmexception import *
from getchunix import *
from colorama import Fore

city = City()
city.makeCity()
city.insertRoads()
city.computeRoads()
city.computeJunctions()
city.displayCity()
city.mapRoadsToJunctions()
city.mapJunctionsToRoads()

getch  = GetchUnix()

MAX_VEHICLES = 80
vehicles = [' ' for x in range(0,MAX_VEHICLES)]
num_vehicles = 0

server = CentralServer()
server.initializeVehiclesPath(MAX_VEHICLES)
server.findRoadTrafficFlow(city.city_map, city.roads)
server.findJunctionTrafficFlow(city.city_map, city.junctions)


while True:
    x = random.randint(2,city.width-2)
    y = random.randint(4,city.length-4)
    if city.isAccomodate(x,y):
        vehicles[num_vehicles] = Vehicle(x,y)
        city.city_map[x][y] = 'O'
        num_vehicles += 1
    if num_vehicles == MAX_VEHICLES:
        break


def updateCity():
    os.system('clear')
    city.displayCity()
    print(Fore.BLACK+"Press q to exit the simulation")
    print ("Timestamp: "+ str(city.timer))

def alarmHandler(signum, frame):
    raise AlarmException

def input_to(timeout=1):
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.alarm(timeout)
    try:
        text = getch()
        signal.alarm(0)
        return text
    except AlarmException:
        print("\n ")
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''

updateCity()

while True:
    city.timer += 1
    inpt = input_to()
    updateCity()
    server.findRoadTrafficFlow(city.city_map, city.roads)
    server.findJunctionTrafficFlow(city.city_map, city.junctions)


    for vhcl in range(MAX_VEHICLES):
        #vehicles[vhcl].random_motion(city.city_map)
        vehicles[vhcl].traverseToJunctionShortestPath(city.junctions,96,city.city_map, vhcl)
        server.vehicles_path[vhcl].append([vehicles[vhcl].x,vehicles[vhcl].y])

    if(inpt == 'q' or inpt == 'Q'):
        exit()
