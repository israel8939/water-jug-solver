
"""Rule-based water leak and shortage diagnosis."""

from dataclasses import dataclass


@dataclass
class Diagnosis:
    condition: str
    certainty_factor: float
    explanation: str


def diagnose(
    pressure_low: bool,
    flow_high: bool,
    reservoir_low: bool,
    supply_insufficient: bool,
) -> list[Diagnosis]:
    """Apply diagnostic rules and return their reasoning traces."""

    results = []

    # Rule 1: Low pressure AND high flow suggests a leak.
    if pressure_low and flow_high:
        results.append(
            Diagnosis(
                condition="LeakSuspected",
                certainty_factor=0.8,
                explanation=(
                    "Rule 1 fired: PressureLow AND FlowHigh "
                    "-> LeakSuspected (CF=0.8)."
                ),
            )
        )

    # Rule 2: Low reservoir AND insufficient supply suggests shortage.
    if reservoir_low and supply_insufficient:
        results.append(
            Diagnosis(
                condition="WaterShortageSuspected",
                certainty_factor=0.9,
                explanation=(
                    "Rule 2 fired: ReservoirLow AND "
                    "SupplyInsufficient -> WaterShortageSuspected "
                    "(CF=0.9)."
                ),
            )
        )

    if not results:
        results.append(
            Diagnosis(
                condition="NoKnownIssueDetected",
                certainty_factor=0.7,
                explanation=(
                    "No configured diagnostic rule matched "
                    "the supplied observations."
                ),
            )
        )

    return results
