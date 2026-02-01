######################################################################
#                                                                    #
#                        TODAY GRAPH                                 #
#                                                                    #
######################################################################


from typing import List
from graph import MRTGraph
from cost import TRAVEL_COST, build_crowding, bake_source_crowding_weights



## init the data for the today transport 
def initialize_mrt_today() -> MRTGraph:
    graph = MRTGraph()

    # North-South Line (NS)
    nsStations = [
        'NS1', 'NS2', 'NS3', 'NS4', 'NS5', 'NS7', 'NS8', 'NS9', 'NS10',
        'NS11', 'NS12', 'NS13', 'NS14', 'NS15', 'NS16', 'NS17', 'NS18',
        'NS19', 'NS20', 'NS21', 'NS22', 'NS23', 'NS24', 'NS25', 'NS26', 'NS27', 'NS28'
    ]
    nsNames = [
        'Jurong East', 'Bukit Batok', 'Bukit Gombak', 'Choa Chu Kang', 'Yew Tee',
        'Kranji', 'Marsiling', 'Woodlands', 'Admiralty', 'Sembawang', 'Canberra',
        'Yishun', 'Khatib', 'Yio Chu Kang', 'Ang Mo Kio', 'Bishan', 'Braddell',
        'Toa Payoh', 'Novena', 'Newton', 'Orchard', 'Somerset', 'Dhoby Ghaut',
        'City Hall', 'Raffles Place', 'Marina Bay', 'Marina South Pier'
    ]

    # East-West Line (EW)
    ewStations = [
        'EW1', 'EW2', 'EW3', 'EW4', 'EW5', 'EW6', 'EW7', 'EW8', 'EW9',
        'EW10', 'EW11', 'EW12', 'EW13', 'EW14', 'EW15', 'EW16', 'EW17',
        'EW18', 'EW19', 'EW20', 'EW21', 'EW22', 'EW23', 'EW24', 'EW25', 'EW26', 'EW27',
        'EW28', 'EW29', 'EW30', 'EW31', 'EW32', 'EW33'
    ]
    ewNames = [
        'Pasir Ris', 'Tampines', 'Simei', 'Tanah Merah', 'Bedok', 'Kembangan',
        'Eunos', 'Paya Lebar', 'Aljunied', 'Kallang', 'Lavender', 'Bugis',
        'City Hall', 'Raffles Place', 'Tanjong Pagar', 'Outram Park', 'Tiong Bahru',
        'Redhill', 'Queenstown', 'Commonwealth', 'Buona Vista', 'Dover', 'Clementi',
        'Jurong East', 'Boon Lay', 'Pioneer', 'Joo Koon', 'Gul Circle', 'Tuas Crescent',
        'Tuas West Road', 'Tuas Link'
    ]

    # Changi Branch Line (CG)
    cgStations = [
        'CG1', 'CG2', 'CG3'
    ]
    cgNames = [
        'Tanah Merah','Expo', 'Changi Airport'
    ]

    # Circle Line (CC)
    ccStations = [
        'CC1', 'CC2', 'CC3', 'CC4', 'CC5', 'CC6', 'CC7', 'CC8', 'CC9',
        'CC10', 'CC11', 'CC12', 'CC13', 'CC14', 'CC15', 'CC16', 'CC17','CC18',
        'CC19', 'CC20', 'CC21', 'CC22', 'CC23', 'CC24', 'CC25', 'CC26',
        'CC27', 'CC28', 'CC29'
    ]
    ccNames = [
        'Dhoby Ghaut', 'Bras Basah', 'Esplanade', 'Promenade', 'Nicoll Highway',
        'Stadium', 'Mountbatten', 'Dakota', 'Paya Lebar', 'MacPherson', 'Tai Seng',
        'Bartley', 'Serangoon', 'Lorong Chuan', 'Bishan', 'Marymount', 'Caldecott',
        'Botanic Gardens', 'Farrer Road', 'Holland Village', 'Buona Vista',
        'One-North', 'Kent Ridge', 'Haw Par Villa', 'Pasir Panjang', 'Labrador Park',
        'Telok Blangah', 'HarbourFront'
    ]

    # (CE)
    ceStations = [
        'CE1', 'CE2', 'CE3'
    ]
    ceNames = [
        'Promenade','Bayfront', 'Marina Bay'
    ]


    # Downtown Line (DT)
    dtStations = [
        'DT1', 'DT2', 'DT3','DT4', 'DT5', 'DT6', 'DT7', 'DT8', 'DT9', 'DT10',
        'DT11', 'DT12', 'DT13', 'DT14', 'DT15', 'DT16', 'DT17', 'DT18',
        'DT19', 'DT20', 'DT21', 'DT22', 'DT23', 'DT24', 'DT25', 'DT26',
        'DT27', 'DT28', 'DT29', 'DT30', 'DT31', 'DT32', 'DT33', 'DT34', 'DT35'
    ]
    dtNames = [
        'Bukit Panjang', 'Cashew', 'Hillview', 'Hume', 'Beauty World', 'King Albert Park',
        'Sixth Avenue', 'Tan Kah Kee', 'Botanic Gardens', 'Stevens', 'Newton',
        'Little India', 'Rochor', 'Bugis', 'Promenade', 'Bayfront', 'Downtown',
        'Telok Ayer', 'Chinatown', 'Fort Canning', 'Bencoolen', 'Jalan Besar',
        'Bendemeer', 'Geylang Bahru', 'Mattar', 'MacPherson', 'Ubi', 'Kaki Bukit',
        'Bedok North', 'Bedok Reservoir', 'Tampines West', 'Tampines', 'Tampines East',
        'Upper Changi', 'Expo'
    ]

    #te stations
    teStations = [
        'TE1', 'TE2', 'TE3', 'TE4', 'TE5',
        'TE6', 'TE7', 'TE8', 'TE9','TE11',
        'TE12', 'TE13', 'TE14', 'TE15', 'TE16', 
        'TE17','TE18', 'TE19', 'TE20', 'TE22',
        'TE23', 'TE24','TE25', 'TE26', 'TE27',
        'TE28', 'TE29'
    ]

    teNames = [
        'Woodlands North', 'Woodlands', 'Woodlands South', 'Springleaf', 'Lentor',
        'Mayflower', 'Bright Hill', 'Upper Thomson', 'Caldecott', 'Stevens',
        'Napier', 'Orchard Boulevard', 'Orchard', 'Great World', 'Havelock',
        'Outram Park', 'Maxwell', 'Shenton Way', 'Marina Bay', 'Gardens by the Bay',
        'Tanjong Rhu', 'Katong Park', 'Tanjong Katong','Marine Parade', 'Marine Terrace',
        'Siglap', 'Bayshore'
    ]


    # North-East Line (NE)
    neStations = [
        'NE1', 'NE3', 'NE4', 'NE5', 'NE6', 'NE7', 'NE8', 'NE9', 'NE10',
        'NE11', 'NE12', 'NE13', 'NE14', 'NE15', 'NE16', 'NE17', 'NE18'
    ]
    neNames = [
        'HarbourFront', 'Outram Park', 'Chinatown', 'Clarke Quay', 'Dhoby Ghaut',
        'Little India', 'Farrer Park', 'Boon Keng', 'Potong Pasir',
        'Woodleigh', 'Serangoon', 'Kovan', 'Hougang', 'Buangkok', 'Sengkang', 'Punggol', 'Punggol Coast'
    ]

    # Add stations
    for code, name in zip(nsStations, nsNames):
        graph.add_station(code, name, "NS")
    for code, name in zip(ewStations, ewNames):
        graph.add_station(code, name, "EW")
    for code, name in zip(cgStations, cgNames):
        graph.add_station(code, name, "CG")
    for code, name in zip(ccStations, ccNames):
        graph.add_station(code, name, "CC")
    for code, name in zip(ceStations, ceNames):
        graph.add_station(code, name ,'CE')
    for code, name in zip(dtStations, dtNames):
        graph.add_station(code, name, "DT")
    for code, name in zip(neStations, neNames):
        graph.add_station(code, name, "NE")
    for code, name in zip(teStations, teNames):
        graph.add_station(code, name, "TE")
    
    # Add edges between consecutive stations
    def chain(line_stations: List[str], w: float = TRAVEL_COST):
        for i in range(len(line_stations) - 1):
            graph.add_edge(line_stations[i], line_stations[i+1], w)


    chain(nsStations)
    chain(ewStations)
    chain(cgStations)
    chain(ccStations)
    chain(ceStations)
    chain(dtStations)
    chain(neStations)
    chain(teStations)

    # Interchanges - connected stations 
    graph.add_edge('NS1', 'EW24')   # Jurong East
    graph.add_edge('NS25', 'EW13')  # City Hall
    graph.add_edge('NS26', 'EW14')  # Raffles Place
    graph.add_edge('NS17', 'CC15')  # Bishan
    graph.add_edge('NS24', 'CC1')   # Dhoby Ghaut 
    graph.add_edge('NS24', 'NE6')   # Dhoby Ghaut
    graph.add_edge('CC1', 'NE6')    # Dhoby Ghaut 
    graph.add_edge('EW8', 'CC9')    # Paya Lebar
    graph.add_edge('EW12', 'DT14')  # Bugis
    graph.add_edge('EW16', 'NE3')   # Outram Park
    graph.add_edge('EW16', 'TE17')  # Outram Park
    graph.add_edge('NE3', 'TE17')   # Outram Park
    graph.add_edge('EW21', 'CC22')  # Buona Vista
    graph.add_edge('CC4', 'DT15')   # Promenade
    graph.add_edge('DT15', 'CE1')   # Promenade
    graph.add_edge('CC4', 'CE1')    # Promenade
    graph.add_edge('CC10', 'DT26')  # MacPherson
    graph.add_edge('CC13', 'NE12')  # Serangoon
    graph.add_edge('CC19', 'DT9')   # Botanic Gardens
    graph.add_edge('CC29', 'NE1')   # HarbourFront
    graph.add_edge('DT12', 'NE7')   # Little India
    graph.add_edge('DT19', 'NE4')   # Chinatown
    graph.add_edge('DT32', 'EW2')   # Tampines
    graph.add_edge('NS27', 'TE20')  # Marina Bay
    graph.add_edge('NS27', 'CE3')   # Marina Bay
    graph.add_edge('CE3', 'TE20')   # Marina Bay
    graph.add_edge('NS9', 'TE2')    # Woodlands
    graph.add_edge('CC17', 'TE9')   # Caldecott
    graph.add_edge('DT10', 'TE11')  # Stevens
    graph.add_edge('NS21', 'DT11')  # Newton
    graph.add_edge('TE14', 'NS22')  # Orchard
    graph.add_edge('DT16', 'CE2')   # Bayfront
    graph.add_edge('EW4', 'CG1')    # Tanah Merah
    graph.add_edge('DT35', 'CG2')   # Expo
    

    build_crowding(graph)
    bake_source_crowding_weights(graph)
  


    return graph
