
from src.diagnosis import diagnose


def test_low_pressure_and_high_flow_suggest_leak():
    results = diagnose(
        pressure_low=True,
        flow_high=True,
        reservoir_low=False,
        supply_insufficient=False,
    )

    assert results[0].condition == "LeakSuspected"
    assert results[0].certainty_factor == 0.8
    assert "Rule 1 fired" in results[0].explanation


def test_low_reservoir_and_insufficient_supply_suggest_shortage():
    results = diagnose(
        pressure_low=False,
        flow_high=False,
        reservoir_low=True,
        supply_insufficient=True,
    )

    assert results[0].condition == "WaterShortageSuspected"
    assert results[0].certainty_factor == 0.9
    assert "Rule 2 fired" in results[0].explanation


def test_no_matching_rule_reports_no_known_issue():
    results = diagnose(
        pressure_low=False,
        flow_high=False,
        reservoir_low=False,
        supply_insufficient=False,
    )

    assert results[0].condition == "NoKnownIssueDetected"
