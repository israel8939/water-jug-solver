from __future__ import annotations

import random
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Variant:
    roll_number: int
    variant_id: int
    capacity_a: int
    capacity_b: int
    target: int


def build_variant(roll_number: int, variant_id: int = 1) -> Variant:
    """Create a deterministic personal variant from roll number + assigned id.

    The assigned variant id should be replaced with the instructor's value.
    """
    if roll_number < 0 or variant_id < 0:
        raise ValueError("roll_number and variant_id must be non-negative")
    rng = random.Random((roll_number * 1009) + variant_id)
    # Keep capacities small enough for a classroom demo, but varied per student.
    a = rng.randint(4, 12)
    b = rng.randint(3, 10)
    target = rng.randint(1, max(a, b))
    # Force a reachable target so every personal variant has a meaningful path.
    d = gcd(a, b)
    target -= target % d
    if target == 0:
        target = d
    return Variant(roll_number, variant_id, a, b, target)
