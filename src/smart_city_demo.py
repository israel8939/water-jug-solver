
"""Demonstration of Smart City water allocation and diagnosis."""

from src.water_allocation import (
    SCENARIOS,
    solve_allocation,
    zone_totals_units,
    reservoir_totals_units,
)
from src.diagnosis import diagnose


def show_allocation(scenario_name: str) -> None:
    print("\n" + "=" * 55)
    print(f"{scenario_name.upper()} WATER ALLOCATION")
    print("=" * 55)

    scenario = SCENARIOS[scenario_name]
    result = solve_allocation(scenario_name, use_propagation=True)
    totals = zone_totals_units(result)
    reservoir_totals = reservoir_totals_units(result)

    print("\nReservoir capacities (10 kL units):")
    for reservoir, capacity in scenario.items():
        used = reservoir_totals.get(reservoir, 0)
        print(f"  {reservoir}: {used}/{capacity} units used")

    print("\nWater allocated to each zone:")
    for zone, units in totals.items():
        print(f"  {zone}: {units * 10} kL/day")

    print("\nSearch statistics:")
    print(f"  Nodes visited: {result.nodes_visited}")
    print(f"  Branches pruned: {result.pruned_branches}")
    print(f"  Propagation enabled: {result.propagation_enabled}")


def show_search_comparison(scenario_name: str) -> None:
    print(f"\n{scenario_name.upper()} SEARCH COMPARISON")

    for enabled in (False, True):
        result = solve_allocation(
            scenario_name,
            use_propagation=enabled,
        )
        label = "With propagation" if enabled else "Without propagation"
        print(
            f"  {label}: nodes={result.nodes_visited}, "
            f"pruned={result.pruned_branches}"
        )


def show_diagnosis() -> None:
    print("\n" + "=" * 55)
    print("WATER SYSTEM DIAGNOSIS")
    print("=" * 55)

    results = diagnose(
        pressure_low=True,
        flow_high=True,
        reservoir_low=False,
        supply_insufficient=False,
    )

    print("Observed conditions: low pressure and high flow")
    for item in results:
        print(f"Diagnosis: {item.condition}")
        print(f"Certainty factor: {item.certainty_factor}")
        print(f"Explanation: {item.explanation}")


def main() -> None:
    print("SMART CITY WATER ALLOCATION SYSTEM")

    show_allocation("normal")
    show_allocation("drought")

    show_search_comparison("normal")
    show_search_comparison("drought")

    show_diagnosis()


if __name__ == "__main__":
    main()
