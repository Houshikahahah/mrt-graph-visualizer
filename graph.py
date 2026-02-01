######################################################################
#                                                                    #
#                            CLASSES                                 #
#                                                                    #
######################################################################

# STATION CLASS 
# MRT GRPAH CLASS ( adding stations and adding edge )


# station init
class Station:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.lines = set()
        self.connections = {}



# mrtgraph
class MRTGraph:
    def __init__(self):
        self.stations = {} 
        self.lines = {}
        self.crowding_penalty_by_code = {}
        self._crowding_ready = False


    # adding the stations
    def add_station(self, code, name, line):

        if code not in self.stations:
            self.stations[code] = Station(code, name)

        self.stations[code].lines.add(line)

        if line not in self.lines:
            self.lines[line] = set()

        self.lines[line].add(code)

    # adding the edge 
    def add_edge(self, a, b, w=1.0):
        if a not in self.stations or b not in self.stations:
            return
        self.stations[a].connections[b] = w
        self.stations[b].connections[a] = w


    def is_transfer(self, a: str, b: str) -> bool:
        # transfer = switching lines at the SAME physical station (same name),
        # between per-line nodes whose line sets don’t overlap
        sa = self.stations[a]
        sb = self.stations[b]
        return (sa.name == sb.name) and not (sa.lines & sb.lines)

    
