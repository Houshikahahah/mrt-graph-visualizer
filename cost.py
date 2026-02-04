######################################################################
#                                                                    #
#                               COST                                 #
#                                                                    #
######################################################################

TRAVEL_COST = 1.0
TRANSFER_COST = 4.0


def build_crowding(graph, extra_crowded_names=None):
    name_to_lines = {}
    for station in graph.stations.values():
        if station.name not in name_to_lines:
            name_to_lines[station.name] = set()
        name_to_lines[station.name].update(station.lines)

    extra_set = set(extra_crowded_names) if extra_crowded_names else set()

    graph.crowding_penalty_by_code = {}

    for code, station in graph.stations.items():
        line_count = len(name_to_lines.get(station.name, set()))
        if line_count <= 1:
            penalty = 0
        elif line_count == 2:
            penalty = 1  # 2 lines -> +1
        else:
            penalty = 2  # 3+ lines -> +2

        if station.name in extra_set and penalty == 0:
            penalty = 1

        graph.crowding_penalty_by_code[code] = penalty

    graph._crowding_ready = True


def _ensure_crowded(graph):
    if not graph._crowding_ready:
        build_crowding(graph)


def crowding_penalty(graph, code):
    _ensure_crowded(graph)
    return graph.crowding_penalty_by_code.get(code, 0)


# def is_transfer(graph, a, b):
#     if a not in graph.stations or b not in graph.stations:
#         return False
#     return graph.stations[a].lines.isdisjoint(graph.stations[b].lines)


def edge_cost(graph, a, b):
    w = graph.stations[a].connections.get(b)
    if w is None:
        raise RuntimeError(f"No edge {a} -> {b}")
    return w

def path_cost(graph, path):
    if not path or len(path) == 1:
        return 0.0
    _ensure_crowded(graph)
    total = 0.0
    for i in range(len(path) - 1):
        total += edge_cost(graph, path[i], path[i + 1])
    return total



def bake_source_crowding_weights(graph):
    """
    For every directed edge A->B:
        w(A->B) = 1 (travel)
              + (4 if transfer(A,B) else 0)
              + (crowding(A) only if transfer)
    """
    _ensure_crowded(graph)

    for a, sa in graph.stations.items():
        for b in list(sa.connections.keys()):
            base = TRAVEL_COST  # 1.0

            if graph.is_transfer(a, b):
                base += TRANSFER_COST          # +4.0
                base += crowding_penalty(graph, a)  # crowding only on transfer

            sa.connections[b] = base
