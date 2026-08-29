from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solver import JugProblem, solve  # noqa: E402


def benchmark(problems):
    rows = []
    for label, problem in problems:
        for method in ("bfs", "dfs"):
            start = time.perf_counter()
            path, expanded = solve(problem, method)
            runtime_ms = (time.perf_counter() - start) * 1000
            rows.append(
                {
                    "case": label,
                    "jug_a": problem.capacity_a,
                    "jug_b": problem.capacity_b,
                    "target": problem.target,
                    "method": method.upper(),
                    "steps": len(path),
                    "nodes_expanded": expanded,
                    "runtime_ms": runtime_ms,
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "results" / "benchmark.csv"))
    args = parser.parse_args()

    problems = [
        ("classic-4-3-2", JugProblem(4, 3, 2)),
        ("5-3-4", JugProblem(5, 3, 4)),
        ("7-4-6", JugProblem(7, 4, 6)),
        ("8-5-6", JugProblem(8, 5, 6)),
        ("9-4-7", JugProblem(9, 4, 7)),
    ]
    rows = benchmark(problems)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} measurements to {output}")
    for row in rows:
        print(
            f"{row['case']:16} {row['method']:3} steps={row['steps']:2} "
            f"expanded={row['nodes_expanded']:2} runtime={row['runtime_ms']:.4f} ms"
        )


if __name__ == "__main__":
    main()
