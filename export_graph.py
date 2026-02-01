# import json
# import os
# from today_graph import initialize_mrt_today

# def export_graph(out_path=None):
#     # default output: MRT/frontend/data/graph.json
#     if out_path is None:
#         out_path = os.path.join("frontend", "data", "graph.json")

#     graph = initialize_mrt_today()

#     # --- nodes ---
#     nodes = []
#     for code, st in graph.stations.items():
#         # st.lines is usually a set; make it JSON friendly
#         try:
#             lines = sorted(list(st.lines))
#         except Exception:
#             lines = []
#         nodes.append({
#             "id": code,
#             "name": st.name,
#             "lines": lines
#         })

#     # --- edges (unique undirected, for display) ---
#     edges = []
#     seen = set()
#     for a, st in graph.stations.items():
#         for b in st.connections.keys():
#             key = tuple(sorted((a, b)))
#             if key in seen:
#                 continue
#             seen.add(key)
#             edges.append({"from": a, "to": b})

#     # --- weights (directed, for cost) ---
#     weights = {}
#     for a, st in graph.stations.items():
#         for b, w in st.connections.items():
#             weights[f"{a}->{b}"] = w

#     payload = {
#         "nodes": nodes,
#         "edges": edges,
#         "weights": weights
#     }

#     # ensure folder exists
#     os.makedirs(os.path.dirname(out_path), exist_ok=True)

#     with open(out_path, "w", encoding="utf-8") as f:
#         json.dump(payload, f, ensure_ascii=False, indent=2)

#     print(f"[OK] Exported nodes={len(nodes)} edges={len(edges)} -> {out_path}")

# if __name__ == "__main__":
#     export_graph()


import json
import os
from future_graph import initialize_mrt_future   # 👈 CHANGE HERE


def export_graph(out_path=None):
    # default output: MRT/frontend/data/graph_future.json
    if out_path is None:
        out_path = os.path.join("frontend", "data", "graph_future.json")

    graph = initialize_mrt_future()   # 👈 CHANGE HERE

    # --- nodes ---
    nodes = []
    for code, st in graph.stations.items():
        try:
            lines = sorted(list(st.lines))
        except Exception:
            lines = []
        nodes.append({
            "id": code,
            "name": st.name,
            "lines": lines
        })

    # --- edges (unique undirected, for display) ---
    edges = []
    seen = set()
    for a, st in graph.stations.items():
        for b in st.connections.keys():
            key = tuple(sorted((a, b)))
            if key in seen:
                continue
            seen.add(key)
            edges.append({"from": a, "to": b})

    # --- weights (directed, for cost) ---
    weights = {}
    for a, st in graph.stations.items():
        for b, w in st.connections.items():
            weights[f"{a}->{b}"] = w

    payload = {
        "nodes": nodes,
        "edges": edges,
        "weights": weights
    }

    # ensure folder exists
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"[OK] Exported FUTURE nodes={len(nodes)} edges={len(edges)} -> {out_path}")


if __name__ == "__main__":
    export_graph()

