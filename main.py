# # main.py

# from today_graph import initialize_mrt_today
# from future_graph import initialize_mrt_future
# from search import (bfs, dfs, greedy_best_first_search, a_star_search)
# from cost import path_cost, edge_cost, crowding_penalty
# from use_cases import TODAY_CASES, FUTURE_CASES
# from cost import TRAVEL_COST
# from heuristic import build_euclidean_time_heuristic_from_json




# def print_edge_details(graph, path):
#     if not path or len(path) == 1:
#         print("No edges (start == end).")
#         return

#     print("\nDetailed edge costs:")
#     total = 0.0
#     for i in range(len(path) - 1):
#         a, b = path[i], path[i + 1]
#         w = edge_cost(graph, a, b)
#         cp = crowding_penalty(graph, a)  # crowding from source node
#         is_transfer = graph.is_transfer(a, b)
#         print(f"{a} -> {b}: cost={w} "
#               f"(step=1"
#               f"{' + transfer=4' if is_transfer else ''}"
#               f"{f' + crowding({a})={cp}' if cp > 0 else ''})")
#         total += w
#     print("Recomputed total cost:", total)


# def run_case(graph, start, end, label):
#     print("\n==================================================")
#     print(label)
#     print("Start:", start, "->", graph.stations[start].name)
#     print("End  :", end, "->", graph.stations[end].name)
#     print("==================================================")

#     # heuristic: zero heuristic (A* becomes Dijkstra)
#     # heuristic = {code: 0 for code in graph.stations}
#     # heuristic = build_line_heuristic(graph, end)

#     coords_json = "mrt_stations_today.json"   # for TODAY graph
#     heuristic = build_euclidean_time_heuristic_from_json(graph, end, coords_json, minutes_per_km=2.5)

#     coords_json = "mrt_stations_future.json"
#     heuristic = build_euclidean_time_heuristic_from_json(graph, end, coords_json, minutes_per_km=2.5)




#     # BFS
#     p_bfs = bfs(graph, start, end)
#     print("\n[BFS]")
#     print("Path:", p_bfs)
#     print("Cost:", path_cost(graph, p_bfs))
#     print_edge_details(graph, p_bfs)

#     # DFS
#     p_dfs = dfs(graph, start, end)
#     print("\n[DFS]")
#     print("Path:", p_dfs)
#     print("Cost:", path_cost(graph, p_dfs))
#     print_edge_details(graph, p_dfs)

#     # # GBFS
#     p_gbfs = greedy_best_first_search(graph, start, end, heuristic)
#     print("\n[GBFS]")
#     print("Path:", p_gbfs)
#     print("Cost:", path_cost(graph, p_gbfs))
#     print_edge_details(graph, p_gbfs)


#     # A star
#     p_astar = a_star_search(graph, start, end, heuristic)
#     print("\n[A*]")
#     print("Path:", p_astar)
#     print("Cost:", path_cost(graph, p_astar))
#     print_edge_details(graph, p_astar)


# if __name__ == "__main__":
#     print("Initializing TODAY MRT graph...")
#     graph = initialize_mrt_today()
#     print("Total stations:", len(graph.stations))

#     for start, end, label in TODAY_CASES:
#         run_case(graph, start, end, label)



#     print("\nInitializing FUTURE MRT graph (TELe / CRL)...")
#     future_graph = initialize_mrt_future()
#     print("Total stations (FUTURE):", len(future_graph.stations))

#     for start, end, label in FUTURE_CASES:
#         run_case(future_graph, start, end, "[FUTURE] " + label)


# main.py

from today_graph import initialize_mrt_today
from future_graph import initialize_mrt_future
from search import (bfs, dfs, greedy_best_first_search, a_star_search)
from cost import path_cost, edge_cost, crowding_penalty
from use_cases import TODAY_CASES, FUTURE_CASES
from heuristic import build_euclidean_time_heuristic_from_json
from pathlib import Path


def print_edge_details(graph, path):
    if not path or len(path) == 1:
        print("No edges (start == end).")
        return

    print("\nDetailed edge costs:")
    total = 0.0
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        w = edge_cost(graph, a, b)
        is_transfer = graph.is_transfer(a, b)
        cp = crowding_penalty(graph, a) if is_transfer else 0

        is_transfer = graph.is_transfer(a, b)
        print(
            f"{a} -> {b}: cost={w} "
            f"(step=1"
            f"{' + transfer=4' if is_transfer else ''}"
            f"{f' + crowding({a})={cp}' if cp > 0 else ''})"
        )
        total += w
    print("Recomputed total cost:", total)



def run_case(graph, start, end, label, coords_json):
    print("\n==================================================")
    print(label)
    print("Start:", start, "->", graph.stations[start].name)
    print("End  :", end, "->", graph.stations[end].name)
    print("==================================================")

 
    heuristic = build_euclidean_time_heuristic_from_json(
        graph,
        end,
        coords_json,
        minutes_per_km=2.5
    )

    # BFS
    p_bfs = bfs(graph, start, end)
    print("\n[BFS]")
    print("Path:", p_bfs)
    print("Cost:", path_cost(graph, p_bfs))
    print_edge_details(graph, p_bfs)

    # DFS
    p_dfs = dfs(graph, start, end)
    print("\n[DFS]")
    print("Path:", p_dfs)
    print("Cost:", path_cost(graph, p_dfs))
    print_edge_details(graph, p_dfs)

    # GBFS
    p_gbfs = greedy_best_first_search(graph, start, end, heuristic)
    print("\n[GBFS]")
    print("Path:", p_gbfs)
    print("Cost:", path_cost(graph, p_gbfs))
    print_edge_details(graph, p_gbfs)

    # A*
    p_astar = a_star_search(graph, start, end, heuristic)
    print("\n[A*]")
    print("Path:", p_astar)
    print("Cost:", path_cost(graph, p_astar))
    print_edge_details(graph, p_astar)


if __name__ == "__main__":
    # -----------------------
    # TODAY
    # -----------------------
    print("Initializing TODAY MRT graph...")
    graph = initialize_mrt_today()
    print("Total stations:", len(graph.stations))

    BASE_DIR = Path(__file__).resolve().parent
    TODAY_COORDS_JSON = str(BASE_DIR / "mrt_stations_today.json")
    FUTURE_COORDS_JSON = str(BASE_DIR / "mrt_stations_future.json")

    for start, end, label in TODAY_CASES:
        run_case(graph, start, end, label, TODAY_COORDS_JSON)

    # -----------------------
    # FUTURE
    # -----------------------
    print("\nInitializing FUTURE MRT graph (TELe / CRL)...")
    future_graph = initialize_mrt_future()
    print("Total stations (FUTURE):", len(future_graph.stations))


    for start, end, label in FUTURE_CASES:
        run_case(future_graph, start, end, "[FUTURE] " + label, FUTURE_COORDS_JSON)
