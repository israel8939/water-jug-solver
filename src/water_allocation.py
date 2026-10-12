
"""Water allocation CSP using backtracking and propagation."""
from src.project_config import REGISTER_NUMBER, VARIANT_ID
from dataclasses import dataclass
from math import ceil
import random


# One unit represents 10 kilolitres of water per day.
UNIT_KL = 10
MINIMUM_LITRES_PER_PERSON_PER_DAY = 10

Edge = tuple[str, str]


@dataclass(frozen=True)
class Zone:
    name: str
    population: int
    demand_units: int
    priority: int

    @property
    def minimum_units(self) -> int:
        litres_needed = (
            self.population
            * MINIMUM_LITRES_PER_PERSON_PER_DAY
        )
        litres_per_unit = UNIT_KL * 1000
        return ceil(litres_needed / litres_per_unit)


@dataclass
class AllocationResult:
    scenario: str
    allocation_units: dict[Edge, int]
    nodes_visited: int
    pruned_branches: int
    propagation_enabled: bool


ZONES = (
    Zone("Hospital", 3000, 6, 3),
    Zone("Residential East", 3000, 5, 2),
    Zone("Residential West", 2000, 4, 1),
)

RESERVOIR_NAMES = (
    "North Reservoir",
    "South Reservoir",
)

PIPELINE_LIMITS: dict[Edge, int] = {
    ("North Reservoir", "Hospital"): 4,
    ("North Reservoir", "Residential East"): 4,
    ("North Reservoir", "Residential West"): 3,
    ("South Reservoir", "Hospital"): 3,
    ("South Reservoir", "Residential East"): 3,
    ("South Reservoir", "Residential West"): 3,
}

SCENARIOS = {
    "normal": {
        "North Reservoir": 9,
        "South Reservoir": 6,
    },
    "drought": {
        "North Reservoir": 5,
        "South Reservoir": 4,
    },
}


def _valid_complete_assignment(assignment, capacities, zones):
    """Validate reservoir capacities and zone demand limits."""

    for reservoir, capacity in capacities.items():
        used = sum(
            amount
            for (source, _), amount in assignment.items()
            if source == reservoir
        )
        if used > capacity:
            return False

    for zone in zones:
        supplied = sum(
            amount
            for (_, destination), amount in assignment.items()
            if destination == zone.name
        )
        if not zone.minimum_units <= supplied <= zone.demand_units:
            return False

    return True


def _propagate(assignment, domains, capacities, zones):
    """Remove domain values that cannot satisfy current constraints."""

    changed = True

    while changed:
        changed = False

        for zone in zones:
            supplied = sum(
                amount
                for (_, destination), amount in assignment.items()
                if destination == zone.name
            )

            if supplied > zone.demand_units:
                return False

            edges = [
                edge for edge in domains
                if edge[1] == zone.name
            ]

            maximum_possible = supplied + sum(
                max(domains[edge]) for edge in edges
            )

            if maximum_possible < zone.minimum_units:
                return False

            for edge in edges:
                others = [item for item in edges if item != edge]

                lowest_allowed = (
                    zone.minimum_units
                    - supplied
                    - sum(max(domains[item]) for item in others)
                )

                highest_allowed = (
                    zone.demand_units
                    - supplied
                    - sum(min(domains[item]) for item in others)
                )

                filtered = [
                    value for value in domains[edge]
                    if lowest_allowed <= value <= highest_allowed
                ]

                if not filtered:
                    return False

                if filtered != domains[edge]:
                    domains[edge] = filtered
                    changed = True

        for reservoir, capacity in capacities.items():
            used = sum(
                amount
                for (source, _), amount in assignment.items()
                if source == reservoir
            )

            if used > capacity:
                return False

            edges = [
                edge for edge in domains
                if edge[0] == reservoir
            ]

            minimum_possible = used + sum(
                min(domains[edge]) for edge in edges
            )

            if minimum_possible > capacity:
                return False

            for edge in edges:
                others = [item for item in edges if item != edge]

                highest_allowed = (
                    capacity
                    - used
                    - sum(min(domains[item]) for item in others)
                )

                filtered = [
                    value for value in domains[edge]
                    if value <= highest_allowed
                ]

                if not filtered:
                    return False

                if filtered != domains[edge]:
                    domains[edge] = filtered
                    changed = True

    return True


def solve_allocation(
    scenario: str,
    use_propagation: bool = True,
    seed: int = REGISTER_NUMBER,
) -> AllocationResult:
    """Find a feasible allocation using CSP backtracking."""

    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")

    capacities = dict(SCENARIOS[scenario])
    rng = random.Random(seed)

    # Prioritize hospital pipeline variables.
    variables = []

    for zone in sorted(
        ZONES,
        key=lambda item: (-item.priority, item.name),
    ):
        edges = [
            edge for edge in PIPELINE_LIMITS
            if edge[1] == zone.name
        ]
        rng.shuffle(edges)
        variables.extend(edges)

    domains = {}

    for edge in variables:
        zone = next(z for z in ZONES if z.name == edge[1])
        maximum = min(
            PIPELINE_LIMITS[edge],
            zone.demand_units,
        )
        domains[edge] = list(range(maximum + 1))

    nodes_visited = 0
    pruned_branches = 0

    if use_propagation and not _propagate(
        {}, domains, capacities, ZONES
    ):
        raise ValueError("No feasible allocation exists.")

    def backtrack(assignment, remaining):
        nonlocal nodes_visited, pruned_branches

        if not remaining:
            if _valid_complete_assignment(
                assignment, capacities, ZONES
            ):
                return dict(assignment)
            return None

        edge = next(v for v in variables if v in remaining)

        for value in sorted(remaining[edge], reverse=True):
            nodes_visited += 1

            next_assignment = dict(assignment)
            next_assignment[edge] = value

            next_domains = {
                key: list(values)
                for key, values in remaining.items()
                if key != edge
            }

            if use_propagation:
                possible = _propagate(
                    next_assignment,
                    next_domains,
                    capacities,
                    ZONES,
                )
                if not possible:
                    pruned_branches += 1
                    continue

            solution = backtrack(
                next_assignment,
                next_domains,
            )

            if solution is not None:
                return solution

            pruned_branches += 1

        return None

    solution = backtrack({}, domains)

    if solution is None:
        raise ValueError("No feasible allocation exists.")

    return AllocationResult(
        scenario=scenario,
        allocation_units=solution,
        nodes_visited=nodes_visited,
        pruned_branches=pruned_branches,
        propagation_enabled=use_propagation,
    )


def zone_totals_units(result):
    """Return total allocated units for every zone."""

    return {
        zone.name: sum(
            amount
            for (_, destination), amount
            in result.allocation_units.items()
            if destination == zone.name
        )
        for zone in ZONES
    }


def reservoir_totals_units(result):
    """Return total used units for every reservoir."""

    return {
        reservoir: sum(
            amount
            for (source, _), amount
            in result.allocation_units.items()
            if source == reservoir
        )
        for reservoir in RESERVOIR_NAMES
    }
