######################################################################
#                                                                    #
#                              ALGO                                  #
#                                                                    #
######################################################################

# bfs, dfs, gbfs, a*

from collections import deque
import heapq
from cost import edge_cost



################################
#             BFS              #
################################
def bfs(graph, start, end):
    if start not in graph.stations:
        return None
    if end not in graph.stations:
        return None

    visited = set()
    parent = {}
    queue = deque()

    queue.append(start)
    visited.add(start)
    parent[start] = None

    while len(queue) > 0:
        current = queue.popleft()
        if current == end:
            break

        neighbours = graph.stations[current].connections
        for next_station in neighbours:
            if next_station not in visited:
                visited.add(next_station)
                parent[next_station] = current
                queue.append(next_station)

    if end not in parent:
        return None

    path = []
    temp = end
    while temp is not None:
        path.append(temp)
        temp = parent[temp]

    path.reverse()
    return path



################################
#             DFS              #
################################
def dfs(graph, start, end):
    if start not in graph.stations:
        return None
    if end not in graph.stations:
        return None

    visited = set()
    parent = {}

    def dfs_visit(current):
        visited.add(current)
        if current == end:
            return True

        neighbours = graph.stations[current].connections
        for next_station in neighbours:
            if next_station not in visited:
                parent[next_station] = current
                if dfs_visit(next_station):
                    return True
        return False

    parent[start] = None
    dfs_visit(start)

    if end not in parent:
        return None

    path = []
    temp = end
    while temp is not None:
        path.append(temp)
        temp = parent[temp]

    path.reverse()
    return path


################################
#            GBFS              #
################################
def greedy_best_first_search(graph, start, end, heuristic):
    if start not in graph.stations:
        return None
    if end not in graph.stations:
        return None

    visited = set()
    parent = {}
    pq = []

    heapq.heappush(pq, (heuristic[start], start))
    parent[start] = None

    while len(pq) > 0:
        h_value, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        if current == end:
            break

        neighbours = graph.stations[current].connections
        for next_station in neighbours:
            if next_station not in visited:
                if next_station not in parent:
                    parent[next_station] = current
                heapq.heappush(pq, (heuristic[next_station], next_station))

    if end not in parent:
        return None

    path = []
    temp = end
    while temp is not None:
        path.append(temp)
        temp = parent[temp]

    path.reverse()
    return path


################################
#             A*               #
################################
def a_star_search(graph, start, end, heuristic):
    if start not in graph.stations:
        return None
    if end not in graph.stations:
        return None

    g_cost = {}
    parent = {}
    visited = set()

    for code in graph.stations:
        g_cost[code] = float("inf")
        parent[code] = None

    g_cost[start] = 0

    pq = []
    heapq.heappush(pq, (g_cost[start] + heuristic[start], start))

    while len(pq) > 0:
        f_current, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        if current == end:
            break

        neighbours = graph.stations[current].connections
        for next_station in neighbours:
            step_cost = edge_cost(graph, current, next_station)
            new_g = g_cost[current] + step_cost

            if new_g < g_cost[next_station]:
                g_cost[next_station] = new_g
                parent[next_station] = current
                heapq.heappush(pq, (new_g + heuristic[next_station], next_station))

    if g_cost[end] == float("inf"):
        return None

    path = []
    temp = end
    while temp is not None:
        path.append(temp)
        temp = parent[temp]

    path.reverse()
    return path