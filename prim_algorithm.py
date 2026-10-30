

# prim_algorithm.py

import networkx as nx


def build_airport_graph(airports, routes):
    """Build a weighted graph of the airport network."""
    graph = nx.Graph()

    for code, data in airports.items():
        graph.add_node(code, **data)

    for source, destination, distance in routes:
        graph.add_edge(
            source,
            destination,
            weight=distance
        )

    return graph


def find_minimum_spanning_tree(graph):
    """Return the MST using Prim's algorithm."""
    if graph.number_of_nodes() == 0:
        return nx.Graph()

    if not nx.is_connected(graph):
        raise ValueError(
            "The airport network is disconnected. "
            "Add routes to connect all airports."
        )

    return nx.minimum_spanning_tree(
        graph,
        algorithm="prim",
        weight="weight"
    )


def calculate_total_distance(tree):
    """Calculate total distance of selected MST routes."""
    return sum(
        data["weight"]
        for _, _, data in tree.edges(data=True)
    )
