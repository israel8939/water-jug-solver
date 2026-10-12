from src.water_allocation import (
    solve_allocation,
    zone_totals_units,
    reservoir_totals_units,
    SCENARIOS,
    PIPELINE_LIMITS,
    ZONES,
)


def test_normal_allocation_respects_constraints():
    result = solve_allocation("normal")
    totals = zone_totals_units(result)
    reservoirs = reservoir_totals_units(result)

    for zone in ZONES:
        assert zone.minimum_units <= totals[zone.name] <= zone.demand_units

    for reservoir, used in reservoirs.items():
        assert used <= SCENARIOS["normal"][reservoir]

    for edge, amount in result.allocation_units.items():
        assert 0 <= amount <= PIPELINE_LIMITS[edge]


def test_drought_allocation_respects_constraints():
    result = solve_allocation("drought")
    totals = zone_totals_units(result)
    reservoirs = reservoir_totals_units(result)

    for zone in ZONES:
        assert zone.minimum_units <= totals[zone.name] <= zone.demand_units

    for reservoir, used in reservoirs.items():
        assert used <= SCENARIOS["drought"][reservoir]

    for edge, amount in result.allocation_units.items():
        assert 0 <= amount <= PIPELINE_LIMITS[edge]


def test_propagation_finds_feasible_normal_allocation():
    result = solve_allocation("normal", use_propagation=True)
    assert result.propagation_enabled is True
    assert zone_totals_units(result)["Hospital"] >= 3


def test_invalid_scenario_is_rejected():
    try:
        solve_allocation("unknown")
    except ValueError:
        pass
    else:
        raise AssertionError("An unknown scenario should raise ValueError")
