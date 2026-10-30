
# main.py

import matplotlib.pyplot as plt
import networkx as nx

from airports import AIRPORTS, ROUTES
from prim_algorithm import (
    build_airport_graph,
    find_minimum_spanning_tree,
    calculate_total_distance
)
from simulation import (
    simulate_traffic,
    print_traffic_report
)


def draw_network(graph, tree):
    """Display the complete network and its MST."""
    positions = {
        code: (data["x"], data["y"])
        for code, data in AIRPORTS.items()
    }

    plt.figure(figsize=(12, 7))

    # Draw all possible routes in light gray
    nx.draw_networkx_edges(
        graph,
        positions,
        edge_color="lightgray",
        width=1.5
    )

    # Highlight MST routes
    nx.draw_networkx_edges(
        tree,
        positions,
        edge_color="green",
        width=3
    )

    nx.draw_networkx_nodes(
        graph,
        positions,
        node_size=1100,
        node_color="skyblue",
        edgecolors="black"
    )

    nx.draw_networkx_labels(
        graph,
        positions,
        font_size=9,
        font_weight="bold"
    )

    # Show distance on each possible route
    labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(
        graph,
        positions,
        edge_labels=labels,
        font_size=8
    )

    plt.title(
        "Air Traffic Control: Airport Network and Prim's MST"
    )
    plt.xlabel("Illustrative map X coordinate")
    plt.ylabel("Illustrative map Y coordinate")
    plt.grid(alpha=0.2)
    plt.tight_layout()
    plt.show()


def main():
    print("=" * 55)
    print("     AIR TRAFFIC CONTROL SIMULATION")
    print("=" * 55)

    graph = build_airport_graph(AIRPORTS, ROUTES)

    try:
        tree = find_minimum_spanning_tree(graph)
    except ValueError as error:
        print("Network error:", error)
        return

    print("\nAIRPORTS")
    for code, data in AIRPORTS.items():
        print(
            f"{code}: {data['name']} "
            f"(capacity: {data['capacity']})"
        )

    print("\nMINIMUM SPANNING TREE ROUTES")
    for source, destination, data in sorted(
        tree.edges(data=True)
    ):
        print(
            f"{source} - {destination}: "
            f"{data['weight']} km"
        )

    total_distance = calculate_total_distance(tree)

    print("\nTotal airports:", graph.number_of_nodes())
    print("MST routes:", tree.number_of_edges())
    print("Total MST distance:", total_distance, "km")

    traffic = simulate_traffic(AIRPORTS, flight_count=160)
    print_traffic_report(traffic)

    draw_network(graph, tree)


if __name__ == "__main__":
    main()
