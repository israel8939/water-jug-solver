"""Integration demo for the Smart City Water Allocation project.

The jug sequence is an illustrative metering simulation, not physical
valve control. The CSP independently calculates reservoir-to-zone allocation.
"""
from src.project_config import REGISTER_NUMBER, VARIANT_ID
from src.variant import build_variant
from src.solver import JugProblem, solve
from src.water_allocation import (
    SCENARIOS,
    solve_allocation,
    zone_totals_units,
    reservoir_totals_units,
)


def show_city_allocation(scenario_name: str) -> None:
    """Display a feasible allocation for the selected city scenario."""
    scenario = SCENARIOS[scenario_name]
    result = solve_allocation(scenario_name, use_propagation=True)
    zone_totals = zone_totals_units(result)
    reservoir_totals = reservoir_totals_units(result)

    print(f"\n{'=' * 55}")
    print(f"{scenario_name.upper()} CITY WATER ALLOCATION")
    print(f"{'=' * 55}")

    print("\nReservoir usage:")
    for reservoir, capacity in scenario.items():
        used = reservoir_totals.get(reservoir, 0)
        print(f"  {reservoir}: {used}/{capacity} units (10 kL per unit)")

    print("\nZone allocation:")
    for zone, units in zone_totals.items():
        print(f"  {zone}: {units * 10} kL/day")

    print(
        f"\nCSP search: {result.nodes_visited} nodes visited; "
        f"{result.pruned_branches} branches pruned."
    )


def show_jug_operations(method: str) -> None:
    """Show the student's configured jug operations using BFS or DFS."""
    variant = build_variant(REGISTER_NUMBER, VARIANT_ID)
    problem = JugProblem(
        variant.capacity_a,
        variant.capacity_b,
        variant.target,
    )
    path, expanded = solve(problem, method)

    print(f"\n{'=' * 55}")
    print(f"JUG METERING SIMULATION — {method.upper()}")
    print(f"{'=' * 55}")
    print(
        f"Register: {REGISTER_NUMBER}; variant: {VARIANT_ID}\n"
        f"Jug A: {problem.capacity_a} L; Jug B: {problem.capacity_b} L; "
        f"target: {problem.target} L"
    )
    print("Note: these are simulated jug operations, not physical valve commands.")
    print("Start -> (0, 0)")

    if not path:
        print("No solution found for this configuration.")
    else:
        for index, (action, state) in enumerate(path, start=1):
            print(f"{index}. {action} -> {state}")
        print(f"Operations: {len(path)}")

    print(f"Nodes expanded: {expanded}")


def main() -> None:
    print("SMART CITY WATER ALLOCATION — INTEGRATED DEMONSTRATION")

    show_city_allocation("normal")
    show_city_allocation("drought")

    show_jug_operations("bfs")
    show_jug_operations("dfs")


if __name__ == "__main__":
    main()
