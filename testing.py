
from today_graph import initialize_mrt_today
from search import (bfs, dfs, greedy_best_first_search, a_star_search )
from cost import path_cost
from use_cases import TODAY_CASES
from cost import TRAVEL_COST

graph = initialize_mrt_today()



def print_edges(graph, only=None):
    """
    Print baked edge weights.
    - only=None  -> print ALL edges
    - only='EW12'-> print edges out of that one code
    - only=[...] -> print edges for that list of codes
    """
    if only is None:
        codes = sorted(graph.stations.keys())
    elif isinstance(only, str):
        codes = [only]
    else:
        codes = list(only)

    for u in codes:
        if u not in graph.stations:
            print(f"[skip] {u} not in graph"); continue
        for v, val in graph.stations[u].connections.items():
            w = val if isinstance(val, (int, float)) else val.get("w", val.get("w_first"))
            print(f"{u} -> {v} : {w}")


print_edges(graph, only="EW12")
