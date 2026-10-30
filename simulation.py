
# simulation.py

def simulate_traffic(airports, flight_count=160):
    """
    Generate synthetic flight demand for each airport.

    These values are for a classroom simulation only.
    """
    if flight_count < 0:
        raise ValueError("Flight count cannot be negative.")

    total_capacity = sum(
        airport["capacity"]
        for airport in airports.values()
    )

    results = {}

    for code, airport in airports.items():
        share = airport["capacity"] / total_capacity
        flights = round(flight_count * share)
        capacity = airport["capacity"]

        utilization = (
            flights / capacity * 100
            if capacity > 0 else 0
        )

        # Simple illustrative delay indicator
        delay = max(0, utilization - 70) * 0.5

        results[code] = {
            "name": airport["name"],
            "capacity": capacity,
            "flights": flights,
            "utilization": utilization,
            "estimated_delay": delay
        }

    return results


def print_traffic_report(results):
    print("\nAIRPORT TRAFFIC REPORT")
    print("-" * 76)
    print(
        f"{'Code':<8}{'Airport':<15}{'Flights':>10}"
        f"{'Capacity':>12}{'Usage %':>12}{'Delay Index':>15}"
    )
    print("-" * 76)

    for code, item in results.items():
        print(
            f"{code:<8}{item['name']:<15}"
            f"{item['flights']:>10}"
            f"{item['capacity']:>12}"
            f"{item['utilization']:>11.1f}%"
            f"{item['estimated_delay']:>14.1f}"
        )
