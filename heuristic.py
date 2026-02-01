def build_line_heuristic(graph, goal):
    """
    h(n) = 0 if n is goal
           1 if n shares a line with goal
           2 otherwise
    """
    goal_lines = graph.stations[goal].lines
    h = {}

    for code, station in graph.stations.items():
        if code == goal:
            h[code] = 0
        elif not station.lines.isdisjoint(goal_lines):
            h[code] = 1
        else:
            h[code] = 2
    return h
