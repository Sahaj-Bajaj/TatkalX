import networkx as nx
from app.data.stations import STATIONS, CONNECTIONS


def build_graph() -> nx.Graph:
    G = nx.Graph()

    for code, info in STATIONS.items():
        G.add_node(code, **info)

    for src, dst, distance, duration in CONNECTIONS:
        G.add_edge(
            src,
            dst,
            weight=distance,
            distance=distance,
            duration=duration,
        )

    return G


graph = build_graph()


def find_routes(source: str, destination: str, max_routes: int = 3) -> dict:
    src = source.upper()
    dst = destination.upper()

    if src not in graph:
        return {"error": f"Station code '{src}' not found"}

    if dst not in graph:
        return {"error": f"Station code '{dst}' not found"}

    if src == dst:
        return {"error": "Source and destination cannot be the same"}

    if not nx.has_path(graph, src, dst):
        return {"routes": [], "message": "No route exists between these stations"}

    raw_paths = list(
        nx.shortest_simple_paths(graph, src, dst, weight="weight")
    )[:max_routes]

    routes = []

    for path in raw_paths:
        total_distance = 0
        total_duration = 0
        segments = []

        for i in range(len(path) - 1):
            edge = graph[path[i]][path[i + 1]]

            total_distance += edge["distance"]
            total_duration += edge["duration"]

            segments.append({
                "from": path[i],
                "from_name": graph.nodes[path[i]]["name"],
                "to": path[i + 1],
                "to_name": graph.nodes[path[i + 1]]["name"],
                "distance_km": edge["distance"],
                "duration_hrs": edge["duration"],
            })

        routes.append({
            "path": path,
            "is_direct": len(path) == 2,
            "stops": len(path) - 2,
            "total_distance_km": total_distance,
            "total_duration_hrs": round(total_duration, 1),
            "segments": segments,
        })

    return {
        "source": {
            "code": src,
            "name": graph.nodes[src]["name"]
        },
        "destination": {
            "code": dst,
            "name": graph.nodes[dst]["name"]
        },
        "routes_found": len(routes),
        "routes": routes,
    }