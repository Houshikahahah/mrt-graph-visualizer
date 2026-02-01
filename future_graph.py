######################################################################
#                                                                    #
#                        FUTURE GRAPH                                #
#          (auto-built from mrt_stations_future.json; no LRT)        #
#                                                                    #
######################################################################

from typing import List
from graph import MRTGraph
from cost import TRAVEL_COST, build_crowding, bake_source_crowding_weights


def initialize_mrt_future() -> MRTGraph:
    graph = MRTGraph()

    ccStations = ['CC1', 'CC2', 'CC3', 'CC4', 'CC5',
                   'CC6', 'CC7', 'CC8', 'CC9', 'CC10', 
                   'CC11', 'CC12', 'CC13', 'CC14', 'CC15', 
                   'CC16', 'CC17', 'CC18', 'CC19', 'CC20', 'CC21', 
                   'CC22', 'CC23', 'CC24', 'CC25', 'CC26', 'CC27', 'CC28', 'CC29']
    ccNames = ['DHOBY GHAUT MRT STATION', 'BRAS BASAH MRT STATION', 'ESPLANADE MRT STATION',
                'PROMENADE MRT STATION', 'NICOLL HIGHWAY MRT STATION', 'STADIUM MRT STATION', 'MOUNTBATTEN MRT STATION', 
                'DAKOTA MRT STATION', 'PAYA LEBAR MRT STATION', 'MACPHERSON MRT STATION', 'TAI SENG MRT STATION',
                  'BARTLEY MRT STATION', 'SERANGOON MRT STATION', 'LORONG CHUAN MRT STATION', 'BISHAN MRT STATION', 
                  'MARYMOUNT MRT STATION', 'CALDECOTT MRT STATION', 'BUKIT BROWN MRT STATION', 'BOTANIC GARDENS MRT STATION', 
                  'FARRER ROAD MRT STATION', 'HOLLAND VILLAGE MRT STATION', 'BUONA VISTA MRT STATION',
                    'ONE-NORTH MRT STATION', 'KENT RIDGE MRT STATION', 'HAW PAR VILLA MRT STATION', 
                    'PASIR PANJANG MRT STATION', 'LABRADOR PARK MRT STATION', 'TELOK BLANGAH MRT STATION',
                      'HARBOURFRONT MRT STATION']
    



    ceStations = ['CE1', 'CE2']
    ceNames = ['BAYFRONT MRT STATION', 'MARINA BAY MRT STATION']

    crStations = ['CR1', 'CR2', 'CR3', 'CR4', 'CR5']
    crNames = ['Changi Airport T5', 'Aviation Park', 'Loyang', 'Pasir Ris East', 'Pasir Ris']



    dtStations = ['DT1', 'DT2', 'DT3', 'DT4', 'DT5', 
                  'DT6', 'DT7', 'DT8', 'DT9', 'DT10', 
                  'DT11', 'DT12', 'DT13', 'DT14', 'DT15',
                 'DT16', 'DT17', 'DT18', 'DT19', 'DT20', 
                 'DT21', 'DT22', 'DT23', 'DT24', 'DT25', 
                 'DT26', 'DT27', 'DT28', 'DT29', 'DT30', 
                 'DT31', 'DT32', 'DT33', 'DT34', 'DT35']
    dtNames = ['BUKIT PANJANG MRT STATION', 'CASHEW MRT STATION', 'HILLVIEW MRT STATION', 'HUME MRT STATION', 
               'BEAUTY WORLD MRT STATION', 'KING ALBERT PARK MRT STATION', 'SIXTH AVENUE MRT STATION', 
               'TAN KAH KEE MRT STATION', 'BOTANIC GARDENS MRT STATION', 'STEVENS MRT STATION', 
               'NEWTON MRT STATION', 'LITTLE INDIA MRT STATION', 'ROCHOR MRT STATION', 
               'BUGIS MRT STATION', 'PROMENADE MRT STATION', 'BAYFRONT MRT STATION', 
               'DOWNTOWN MRT STATION', 'TELOK AYER MRT STATION', 'CHINATOWN MRT STATION', 
               'FORT CANNING MRT STATION', 'BENCOOLEN MRT STATION', 'JALAN BESAR MRT STATION', 
               'BENDEMEER MRT STATION', 'GEYLANG BAHRU MRT STATION', 'MATTAR MRT STATION', 
               'MACPHERSON MRT STATION', 'UBI MRT STATION', 'KAKI BUKIT MRT STATION', 'BEDOK NORTH MRT STATION', 
               'BEDOK RESERVOIR MRT STATION', 'TAMPINES WEST MRT STATION', 'TAMPINES MRT STATION', 
               'TAMPINES EAST MRT STATION', 'UPPER CHANGI MRT STATION', 'EXPO MRT STATION']
    


    ewStations = ['EW1', 'EW2', 'EW3', 'EW4', 'EW5', 
                  'EW6', 'EW7', 'EW8', 'EW9', 'EW10', 
                  'EW11', 'EW12', 'EW13', 'EW14', 'EW15', 
                  'EW16', 'EW17', 'EW18', 'EW19', 'EW20', 
                  'EW21', 'EW22', 'EW23', 'EW24', 'EW25', 
                  'EW26', 'EW27', 'EW28', 'EW29', 'EW30', 
                  'EW31', 'EW32', 'EW33']
    ewNames = ['PASIR RIS MRT STATION', 'TAMPINES MRT STATION', 'SIMEI MRT STATION', 
               'TANAH MERAH MRT STATION', 'BEDOK MRT STATION', 'KEMBANGAN MRT STATION', 
               'EUNOS MRT STATION', 'PAYA LEBAR MRT STATION', 'ALJUNIED MRT STATION', 
               'KALLANG MRT STATION', 'LAVENDER MRT STATION', 'BUGIS MRT STATION', 
               'CITY HALL MRT STATION', 'RAFFLES PLACE MRT STATION', 'TANJONG PAGAR MRT STATION', 
               'OUTRAM PARK MRT STATION', 'TIONG BAHRU MRT STATION', 'REDHILL MRT STATION', 
               'QUEENSTOWN MRT STATION', 'COMMONWEALTH MRT STATION', 'BUONA VISTA MRT STATION', 
               'DOVER MRT STATION', 'CLEMENTI MRT STATION', 'JURONG EAST MRT STATION', 
               'CHINESE GARDEN MRT STATION', 'LAKESIDE MRT STATION', 'BOON LAY MRT STATION', 
               'PIONEER MRT STATION', 'JOO KOON MRT STATION', 'GUL CIRCLE MRT STATION',
                 'TUAS CRESCENT MRT STATION', 'TUAS WEST ROAD MRT STATION', 'TUAS LINK MRT STATION']
    


    neStations = ['NE1', 'NE3', 'NE4', 'NE5', 
                  'NE6', 'NE7', 'NE8', 'NE9', 'NE10',
                    'NE11', 'NE12', 'NE13', 'NE14', 'NE15', 'NE16', 'NE17']
    neNames = ['HARBOURFRONT MRT STATION', 'OUTRAM PARK MRT STATION', 'CHINATOWN MRT STATION', 'CLARKE QUAY MRT STATION',
                'DHOBY GHAUT MRT STATION', 'LITTLE INDIA MRT STATION', 'FARRER PARK MRT STATION', 'BOON KENG MRT STATION', 
                'POTONG PASIR MRT STATION', 'WOODLEIGH MRT STATION', 'SERANGOON MRT STATION', 
                'KOVAN MRT STATION', 'HOUGANG MRT STATION', 'BUANGKOK MRT STATION', 
                'SENGKANG MRT STATION', 'PUNGGOL MRT STATION']
    

    nsStations = ['NS1', 'NS2', 'NS3', 'NS4', 'NS5', 
                  'NS7', 'NS8', 'NS9', 'NS10', 'NS11',
                 'NS12', 'NS13', 'NS14', 'NS15', 'NS16', 
                 'NS17', 'NS18', 'NS19', 'NS20', 'NS21', 
                 'NS22', 'NS23', 'NS24', 'NS25', 'NS26', 'NS27', 'NS28']
    nsNames = ['JURONG EAST MRT STATION', 'BUKIT BATOK MRT STATION', 'BUKIT GOMBAK MRT STATION', 
               'CHOA CHU KANG MRT STATION', 'YEW TEE MRT STATION', 'KRANJI MRT STATION', 
               'MARSILING MRT STATION', 'WOODLANDS MRT STATION', 'ADMIRALTY MRT STATION', 
               'SEMBAWANG MRT STATION', 'CANBERRA MRT STATION', 'YISHUN MRT STATION', 
               'KHATIB MRT STATION', 'YIO CHU KANG MRT STATION', 'ANG MO KIO MRT STATION', 
               'BISHAN MRT STATION', 'BRADDELL MRT STATION', 'TOA PAYOH MRT STATION',
                 'NOVENA MRT STATION', 'NEWTON MRT STATION', 'ORCHARD MRT STATION', 
                 'SOMERSET MRT STATION', 'DHOBY GHAUT MRT STATION', 'CITY HALL MRT STATION', 
                 'RAFFLES PLACE MRT STATION', 'MARINA BAY MRT STATION', 'MARINA SOUTH PIER MRT STATION']

    teStations = ['TE1', 'TE2', 'TE3', 'TE4', 'TE5', 
                  'TE6', 'TE7', 'TE8', 'TE9', 'TE11',
                    'TE12', 'TE13', 'TE14', 'TE15', 
                    'TE16', 'TE17', 'TE18', 'TE19', 'TE20', 'TE22', 
                    'TE23', 'TE24', 'TE25', 'TE26', 'TE27', 
                    'TE28', 'TE29', 'TE30', 'TE31', 'TE32', 'TE32X', 'TE33', 'TE34', 'TE35']
    teNames = ['WOODLANDS NORTH MRT STATION', 'WOODLANDS MRT STATION', 
               'WOODLANDS SOUTH MRT STATION', 'SPRINGLEAF MRT STATION', 
               'LENTOR MRT STATION', 'MAYFLOWER MRT STATION', 'BRIGHT HILL MRT STATION',
                 'UPPER THOMSON MRT STATION', 'CALDECOTT MRT STATION', 'STEVENS MRT STATION', 
                 'NAPIER', 'ORCHARD BOULEVARD', 'ORCHARD MRT STATION', 'GREAT WORLD', 
                 'HAVELOCK', 'OUTRAM PARK', 'MAXWELL', 'SHENTON WAY', 'MARINA BAY', 
                 'GARDENS BY THE BAY', 'TANJONG RHU', 'KATONG PARK', 'TANJONG KATONG', 
                 'MARINE PARADE', 'MARINE TERRACE', 'SIGLAP', 'BAYSHORE', 'Bedok South', 
                 'Sungei Bedok', 'Changi Airport T5', 'Xilin', 'Changi Airport', 'Expo', 'Tanah Merah']

    # Add stations
    for code, name in zip(ccStations, ccNames):
        graph.add_station(code, name, 'CC')

    for code, name in zip(ceStations, ceNames):
        graph.add_station(code, name, 'CE')

    for code, name in zip(crStations, crNames):
        graph.add_station(code, name, 'CR')

    for code, name in zip(dtStations, dtNames):
        graph.add_station(code, name, 'DT')

    for code, name in zip(ewStations, ewNames):
        graph.add_station(code, name, 'EW')

    for code, name in zip(neStations, neNames):
        graph.add_station(code, name, 'NE')

    for code, name in zip(nsStations, nsNames):
        graph.add_station(code, name, 'NS')

    for code, name in zip(teStations, teNames):
        graph.add_station(code, name, 'TE')

    # Add edges between consecutive stations per line (by station number order)
    def chain(line_stations: List[str], w: float = TRAVEL_COST):
        for i in range(len(line_stations) - 1):
            graph.add_edge(line_stations[i], line_stations[i+1], w)

    chain(ccStations)
    chain(ceStations)
    chain(crStations)
    chain(dtStations)
    chain(ewStations)
    chain(neStations)
    chain(nsStations)
    chain(teStations)

    # Interchanges: stations sharing the same name across different lines
    graph.add_edge('CC9', 'EW8')
    graph.add_edge('DT32', 'EW2')
    graph.add_edge('CR5', 'EW1')
    graph.add_edge('DT35', 'TE34')
    graph.add_edge('EW24', 'NS1')
    graph.add_edge('NS9', 'TE2')
    graph.add_edge('CC22', 'EW21')
    graph.add_edge('EW4', 'TE35')
    graph.add_edge('CC10', 'DT26')
    graph.add_edge('EW13', 'NS25')
    graph.add_edge('CC29', 'NE1')
    graph.add_edge('DT14', 'EW12')
    graph.add_edge('NS22', 'TE14')
    graph.add_edge('CE1', 'DT16')
    graph.add_edge('CC17', 'TE9')
    graph.add_edge('CE2', 'NS27')
    graph.add_edge('CE2', 'TE20')
    graph.add_edge('DT19', 'NE4')
    graph.add_edge('CC1', 'NE6')
    graph.add_edge('CC1', 'NS24')
    graph.add_edge('CC13', 'NE12')
    graph.add_edge('CC15', 'NS17')
    graph.add_edge('DT12', 'NE7')
    graph.add_edge('DT10', 'TE11')
    graph.add_edge('CC4', 'DT15')
    graph.add_edge('CC19', 'DT9')
    graph.add_edge('EW14', 'NS26')
    graph.add_edge('EW16', 'NE3')
    graph.add_edge('EW16', 'TE17')
    graph.add_edge('DT11', 'NS21')
    graph.add_edge('CR1', 'TE32')

    build_crowding(graph)
    bake_source_crowding_weights(graph)

    return graph
