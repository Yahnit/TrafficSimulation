from collections import defaultdict

class CentralServer:
    def __init__(self):
        self.name = "Central Server"
        self.id = "srvr735"
        self.traffic_flow = ""
        self.junction_flow = ""

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
