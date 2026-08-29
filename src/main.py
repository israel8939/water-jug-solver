from __future__ import annotations

import argparse
import time
from typing import List, Tuple

from solver import JugProblem, solve
from variant import build_variant


def format_solution(path: List[Tuple[str, Tuple[int, int]]]) -> str:
    lines = ["0. Start -> (0, 0)"]
    for index, (action, state) in enumerate(path, start=1):
        lines.append(f"{index}. {action:>12} -> {state}")
    return "\n".join(lines)


def run(method: str, problem: JugProblem) -> None:
    started = time.perf_counter()
    path, expanded = solve(problem, method)
    elapsed_ms = (time.perf_counter() - started) * 1000

    print(f"Method: {method.upper()}")
    print(
        f"Problem: A={problem.capacity_a}L, B={problem.capacity_b}L, "
        f"target={problem.target}L"
    )
    if not path:
        print("No solution found.")
    else:
        print(format_solution(path))
        print(f"Steps: {len(path)}")
    print(f"Nodes expanded: {expanded}")
    print(f"Runtime: {elapsed_ms:.4f} ms")


def main() -> None:
    parser = argparse.ArgumentParser(description="Water Jug state-space solver")
    parser.add_argument("--capacity-a", type=int, help="capacity of jug A")
    parser.add_argument("--capacity-b", type=int, help="capacity of jug B")
    parser.add_argument("--target", type=int, help="target amount")
    parser.add_argument("--method", choices=["bfs", "dfs"], default="bfs")
    parser.add_argument("--roll-number", type=int, help="student roll/register number")
    parser.add_argument(
        "--variant-id", type=int, default=1,
        help="instructor-assigned variant id (replace default with your assigned value)",
    )
    args = parser.parse_args()

    if args.roll_number is not None:
        variant = build_variant(args.roll_number, args.variant_id)
        a, b, target = variant.capacity_a, variant.capacity_b, variant.target
        print(
            f"Personal variant: roll={args.roll_number}, variant={args.variant_id}, "
            f"A={a}L, B={b}L, target={target}L"
        )
    elif all(x is not None for x in (args.capacity_a, args.capacity_b, args.target)):
        a, b, target = args.capacity_a, args.capacity_b, args.target
    else:
        parser.error(
            "Provide --roll-number (recommended) or all of --capacity-a, --capacity-b, --target."
        )

    problem = JugProblem(a, b, target)
    run(args.method, problem)


if __name__ == "__main__":
    main()
