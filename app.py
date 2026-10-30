
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import random

st.set_page_config(
    page_title="Air Traffic Control",
    page_icon="✈️",
    layout="wide"
)

# ---------------- AIRPORT DATA ----------------

AIRPORTS = {
    "DEL": {"name": "Delhi", "x": 2, "y": 8, "capacity": 100},
    "JAI": {"name": "Jaipur", "x": 1, "y": 6, "capacity": 45},
    "LKO": {"name": "Lucknow", "x": 5, "y": 7, "capacity": 55},
    "BHO": {"name": "Bhopal", "x": 4, "y": 4, "capacity": 40},
    "MUM": {"name": "Mumbai", "x": 2, "y": 1, "capacity": 90},
    "HYD": {"name": "Hyderabad", "x": 6, "y": 2, "capacity": 65},
    "BLR": {"name": "Bengaluru", "x": 5, "y": 0, "capacity": 70},
    "CHE": {"name": "Chennai", "x": 8, "y": 1, "capacity": 60},
}

ROUTES = [
    ("DEL", "JAI", 230),
    ("DEL", "LKO", 420),
    ("DEL", "BHO", 600),
    ("JAI", "BHO", 500),
    ("JAI", "MUM", 900),
    ("LKO", "BHO", 320),
    ("LKO", "HYD", 900),
    ("BHO", "MUM", 650),
    ("BHO", "HYD", 650),
    ("MUM", "HYD", 620),
    ("MUM", "BLR", 840),
    ("HYD", "BLR", 500),
    ("HYD", "CHE", 520),
    ("BLR", "CHE", 290),
]

graph = nx.Graph()

for code, info in AIRPORTS.items():
    graph.add_node(code, **info)

for source, destination, distance in ROUTES:
    graph.add_edge(source, destination, weight=distance)

MST = nx.minimum_spanning_tree(
    graph, algorithm="prim", weight="weight"
)

TOTAL_MST = sum(
    data["weight"] for _, _, data in MST.edges(data=True)
)

POSITIONS = {
    code: (info["x"], info["y"])
    for code, info in AIRPORTS.items()
}

# ---------------- STYLE ----------------

st.markdown("""
<style>
.stApp {
    background-color: #101827;
    color: #f1f5f9;
}
[data-testid="stMetric"] {
    background-color: #1d293b;
    border: 1px solid #334155;
    padding: 18px;
    border-radius: 12px;
}
div.stButton > button {
    border-radius: 8px;
    min-height: 42px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.title("✈️ Air Control")
st.sidebar.caption("Airport Network Management")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Airport Explorer",
        "Optimal Network",
        "Traffic Simulation",
        "Performance Reports",
    ],
)

st.sidebar.divider()
st.sidebar.success("Simulation system ready")
st.sidebar.caption("Educational demonstration only")

# ---------------- GRAPH FUNCTION ----------------

def show_network(highlight_mst=False):
    fig, ax = plt.subplots(figsize=(10, 5.8))
    fig.patch.set_facecolor("#101827")
    ax.set_facecolor("#101827")

    nx.draw_networkx_edges(
        graph,
        POSITIONS,
        ax=ax,
        edge_color="#526176",
        width=1.5,
    )

    if highlight_mst:
        nx.draw_networkx_edges(
            MST,
            POSITIONS,
            ax=ax,
            edge_color="#22c55e",
            width=3.5,
        )

    nx.draw_networkx_nodes(
        graph,
        POSITIONS,
        ax=ax,
        node_color="#38bdf8",
        edgecolors="white",
        node_size=1000,
    )

    nx.draw_networkx_labels(
        graph,
        POSITIONS,
        ax=ax,
        font_color="#0f172a",
        font_weight="bold",
        font_size=9,
    )

    nx.draw_networkx_edge_labels(
        graph,
        POSITIONS,
        edge_labels=nx.get_edge_attributes(graph, "weight"),
        ax=ax,
        font_size=8,
        font_color="white",
    )

    ax.set_title(
        "Airport Connectivity Map",
        color="white",
        fontsize=15,
        pad=15,
    )
    ax.tick_params(colors="#94a3b8")
    for spine in ax.spines.values():
        spine.set_color("#334155")

    st.pyplot(fig)
    plt.close(fig)

# ---------------- DASHBOARD ----------------

if page == "Dashboard":
    st.title("✈️ Air Traffic Control Dashboard")
    st.write(
        "Monitor airport connectivity, route distances, "
        "network optimization, and simulated traffic."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Airports", len(AIRPORTS))
    c2.metric("Available Routes", graph.number_of_edges())
    c3.metric("MST Routes", MST.number_of_edges())
    c4.metric("MST Distance", f"{TOTAL_MST:,} km")

    st.subheader("Airport Network Overview")
    show_network()

    st.info(
        "Select a page from the sidebar to explore airports, "
        "calculate the optimal network, or simulate traffic."
    )

# ---------------- AIRPORT EXPLORER ----------------

elif page == "Airport Explorer":
    st.title("🔎 Airport Explorer")
    st.write("Select or search for an airport to view its details.")

    search = st.text_input(
        "Search airport by code or name",
        placeholder="Example: Delhi or DEL",
    )

    matches = [
        code for code, info in AIRPORTS.items()
        if search.lower() in code.lower()
        or search.lower() in info["name"].lower()
    ]

    if matches:
        selected = st.selectbox(
            "Choose an airport",
            matches,
            format_func=lambda code:
                f"{code} — {AIRPORTS[code]['name']}",
        )

        info = AIRPORTS[selected]
        a, b, c = st.columns(3)
        a.metric("Airport Code", selected)
        b.metric("Capacity Units", info["capacity"])
        c.metric("Direct Connections", graph.degree[selected])

        st.subheader("Connected Airports")

        neighbors = []
        for neighbor in graph.neighbors(selected):
            neighbors.append({
                "Airport": neighbor,
                "Name": AIRPORTS[neighbor]["name"],
                "Distance (km)": graph[selected][neighbor]["weight"],
            })

        st.dataframe(
            pd.DataFrame(neighbors),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("No matching airport found.")

# ---------------- OPTIMAL NETWORK ----------------

elif page == "Optimal Network":
    st.title("🌐 Optimal Airport Network")
    st.write(
        "Use Prim's algorithm to find the minimum spanning tree "
        "for the available airport network."
    )

    if st.button("Calculate Optimal Network", type="primary"):
        st.session_state["show_mst"] = True

    if st.session_state.get("show_mst", False):
        a, b, c = st.columns(3)
        a.metric("Connected Airports", len(AIRPORTS))
        b.metric("Selected Routes", MST.number_of_edges())
        c.metric("Total MST Distance", f"{TOTAL_MST:,} km")

        show_network(highlight_mst=True)

        st.success(
            "The green lines represent the selected minimum "
            "spanning tree routes."
        )

        edge_rows = [
            {
                "From": u,
                "To": v,
                "Distance (km)": data["weight"],
            }
            for u, v, data in MST.edges(data=True)
        ]

        st.subheader("Selected Routes")
        st.dataframe(
            pd.DataFrame(edge_rows),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Click the button to display the optimized network.")

# ---------------- TRAFFIC SIMULATION ----------------

elif page == "Traffic Simulation":
    st.title("📊 Traffic Simulation")
    st.write(
        "Generate synthetic flight demand and compare it with "
        "illustrative airport capacity."
    )

    flight_count = st.slider(
        "Number of simulated flights",
        min_value=20,
        max_value=500,
        value=160,
        step=20,
    )

    if st.button("Simulate Traffic", type="primary"):
        random.seed(42)

        total_capacity = sum(
            info["capacity"] for info in AIRPORTS.values()
        )

        rows = []
        for code, info in AIRPORTS.items():
            # Random variation makes this a simple demand scenario.
            flights = max(
                0,
                round(
                    flight_count * info["capacity"] / total_capacity
                    + random.randint(-4, 4)
                ),
            )

            utilization = flights / info["capacity"] * 100
            delay_index = max(0, utilization - 70) * 0.5

            rows.append({
                "Code": code,
                "Airport": info["name"],
                "Flights": flights,
                "Capacity": info["capacity"],
                "Utilization (%)": round(utilization, 1),
                "Delay Indicator": round(delay_index, 1),
            })

        st.session_state["traffic_results"] = rows

    if "traffic_results" in st.session_state:
        df = pd.DataFrame(st.session_state["traffic_results"])

        a, b, c = st.columns(3)
        a.metric("Simulated Flights", int(df["Flights"].sum()))
        b.metric("Average Utilization", f"{df['Utilization (%)'].mean():.1f}%")
        c.metric("Highest Utilization", f"{df['Utilization (%)'].max():.1f}%")

        st.subheader("Airport Traffic")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Capacity Utilization")
        chart_df = df.set_index("Airport")[["Utilization (%)"]]
        st.bar_chart(chart_df)

        st.subheader("Delay Indicator by Airport")
        delay_df = df.set_index("Airport")[["Delay Indicator"]]
        st.bar_chart(delay_df)

        st.caption(
            "All flights, capacity values, and delay indicators are "
            "synthetic. They are not real aviation predictions."
        )

# ---------------- PERFORMANCE REPORTS ----------------

elif page == "Performance Reports":
    st.title("📈 Performance Reports")

    original_distance = sum(
        data["weight"]
        for _, _, data in graph.edges(data=True)
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Network Nodes", graph.number_of_nodes())
    col2.metric("Network Edges", graph.number_of_edges())
    col3.metric("MST Total Weight", f"{TOTAL_MST:,} km")

    st.subheader("Route Distance Comparison")

    comparison = pd.DataFrame({
        "Network": ["All available routes", "Minimum spanning tree"],
        "Route Count": [
            graph.number_of_edges(),
            MST.number_of_edges(),
        ],
        "Distance Sum (km)": [
            original_distance,
            TOTAL_MST,
        ],
    })

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True,
    )

    st.bar_chart(
        comparison.set_index("Network")[["Distance Sum (km)"]]
    )

    st.subheader("Airport Capacity")
    capacity_df = pd.DataFrame([
        {"Airport": code, "Capacity": info["capacity"]}
        for code, info in AIRPORTS.items()
    ])

    st.bar_chart(capacity_df.set_index("Airport"))

    st.warning(
        "MST distance is a network-weight comparison. It does not "
        "measure actual flight distance, safety, delays, or fuel savings."
    )

st.divider()
st.caption("Air Traffic Control Simulation | Python + Streamlit + Prim's Algorithm")
