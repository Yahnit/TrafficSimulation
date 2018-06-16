from city import City
from vehicle import Vehicle
import random, os
from alarmexception import *
from getchunix import *
from colorama import Fore

city = City()
city.makeCity()
city.insertRoads()
city.displayCity()

getch  = GetchUnix()

MAX_VEHICLES = 30
vehicles = [' ' for x in range(0,MAX_VEHICLES)]
num_vehicles = 0

while True:
    x = random.randint(2,36)
    y = random.randint(4,72)
    if city.isAccomodate(x,y):
        vehicles[num_vehicles] = Vehicle(x,y)
        city.city_map[x][y] = 'O'
        num_vehicles += 1
    if num_vehicles == MAX_VEHICLES:
        break


def updateCity():
    os.system('clear')
    city.displayCity()
    print(Fore.BLACK+"Press q to exit the game")

def hello():
    print("Hello")

def alarmHandler(signum, frame):
    raise AlarmException
'''
Function which takes input from the user and returns it
'''
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
    inpt = input_to()
    updateCity()

    for vhcl in range(MAX_VEHICLES):
        vehicles[vhcl].motion(city.city_map)

    if(inpt == 'q' or inpt == 'Q'):
        exit()
