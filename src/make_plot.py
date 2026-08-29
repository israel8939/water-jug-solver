from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / "results" / "benchmark.csv"
OUT = ROOT / "docs" / "bfs_vs_dfs.png"


def main() -> None:
    with CSV_FILE.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    cases = []
    bfs_nodes = []
    dfs_nodes = []
    bfs_runtime = []
    dfs_runtime = []
    for row in rows:
        case = row["case"]
        if case not in cases:
            cases.append(case)
        if row["method"] == "BFS":
            bfs_nodes.append(int(row["nodes_expanded"]))
            bfs_runtime.append(float(row["runtime_ms"]))
        else:
            dfs_nodes.append(int(row["nodes_expanded"]))
            dfs_runtime.append(float(row["runtime_ms"]))

    fig, ax = plt.subplots(figsize=(8, 4.6))
    x = range(len(cases))
    width = 0.38
    ax.bar([i - width / 2 for i in x], bfs_nodes, width, label="BFS nodes expanded")
    ax.bar([i + width / 2 for i in x], dfs_nodes, width, label="DFS nodes expanded")
    ax.set_xticks(list(x))
    ax.set_xticklabels(cases, rotation=20, ha="right")
    ax.set_ylabel("Nodes expanded")
    ax.set_title("BFS vs DFS: State-space search effort")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=180)
    plt.close(fig)

    runtime_out = ROOT / "docs" / "runtime_comparison.png"
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.plot(list(x), bfs_runtime, marker="o", label="BFS runtime (ms)")
    ax.plot(list(x), dfs_runtime, marker="o", label="DFS runtime (ms)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(cases, rotation=20, ha="right")
    ax.set_ylabel("Runtime (ms)")
    ax.set_title("BFS vs DFS runtime")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(runtime_out, dpi=180)
    plt.close(fig)
    print(f"Created {OUT}")
    print(f"Created {runtime_out}")


if __name__ == "__main__":
    main()
