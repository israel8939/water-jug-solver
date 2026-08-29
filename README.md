# Water Jug Problem Solver

A small, from-scratch Python implementation of state-space search for the Water Jug Problem. The program models each configuration as a state `(amount_in_A, amount_in_B)` and each legal operation as a state transition.

## 1. Problem

Given two jugs with capacities `A` and `B`, starting empty, find an ordered sequence of **fill**, **empty**, and **pour** operations that leaves the target volume in either jug.

### State representation
`(x, y)` where:
- `x` = current litres in jug A
- `y` = current litres in jug B

### Actions
- Fill A
- Fill B
- Empty A
- Empty B
- Pour A -> B
- Pour B -> A

### Goal test
A state is a goal when `target in (x, y)`.

### Cost
Every action has unit cost, so BFS returns a shortest-operation solution.

## 2. Approach

This repository implements both algorithms without using a search library:

- **BFS** uses a FIFO queue and returns an optimal (shortest) action sequence when each action has equal cost.
- **DFS** uses an explicit LIFO stack and returns a solution when one is found, but it is not guaranteed to be shortest.

A `visited` set prevents repeated states. Parent pointers reconstruct the ordered action list after a goal is found.

A standard gcd reachability check is used before searching. If `target` is not divisible by `gcd(A, B)`, the instance is impossible.

## 3. Personalisation / anti-copy variant

Use your own roll/register number and the **exact variant id assigned by your instructor**. The variant generator uses `random.Random(seed)` where `seed = roll_number * 1009 + variant_id`, so the same student inputs always reproduce the same capacities and target.

Do **not** submit the example values from this README as your personalised variant. Replace the example command with your own values.

## 4. Requirements

- Python 3.10+
- `pytest`
- `matplotlib` (only needed for the benchmark plot)

## 5. Clean-clone setup

```bash
git clone <YOUR-REPOSITORY-URL>
cd water_jug_solver
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest -q
```

## 6. Run the solver

### Direct problem input

Example: classic 4 L / 3 L jugs, target 2 L.

```bash
python src/main.py --capacity-a 4 --capacity-b 3 --target 2 --method bfs
```

Try DFS:

```bash
python src/main.py --capacity-a 4 --capacity-b 3 --target 2 --method dfs
```

### Personalised variant

Replace the example roll number and variant id with your own:

```bash
python src/main.py --roll-number 123456 --variant-id 7 --method bfs
```

## 7. Sample input/output

Sample command:

```text
python src/main.py --capacity-a 4 --capacity-b 3 --target 2 --method bfs
```

Sample output (exact runtime may differ):

```text
Method: BFS
Problem: A=4L, B=3L, target=2L
0. Start -> (0, 0)
1.       Fill B -> (0, 3)
2.   Pour B -> A -> (3, 0)
3.       Fill B -> (3, 3)
4.   Pour B -> A -> (4, 2)
Steps: 4
Nodes expanded: <machine-dependent order, see your run>
Runtime: <machine-dependent> ms
```

## 8. Benchmark and plots

Generate BFS/DFS comparison data:

```bash
python src/benchmark.py
```

Generate plots used by the report:

```bash
python src/make_plot.py
```

Outputs:
- `results/benchmark.csv`
- `docs/bfs_vs_dfs.png`
- `docs/runtime_comparison.png`

## 9. Repository structure

```text
water_jug_solver/
├── src/
│   ├── __init__.py
│   ├── benchmark.py
│   ├── main.py
│   ├── make_plot.py
│   ├── solver.py
│   └── variant.py
├── tests/
│   └── test_solver.py
├── docs/
│   ├── report.pdf
│   ├── bfs_vs_dfs.png
│   └── runtime_comparison.png
├── results/
│   └── benchmark.csv
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## 10. Complexity

Let `S <= (A+1)(B+1)` be the number of reachable states. Each state has at most six outgoing actions.

- **BFS:** `O(S)` time and `O(S)` space for this bounded state graph.
- **DFS:** `O(S)` time in the worst case and `O(S)` space for the visited set, parent map, and stack.

The practical state-space size is small because each jug can hold only a finite number of integer litre values.

## 11. Limitations

The implementation assumes integer litre capacities and integer states. It does not model measurement noise, fractional litre actions, or real-world physical constraints.

## 12. Viva preparation

Be ready to explain:

1. Why `(x, y)` is a sufficient state description.
2. Why pour operations use `min(source, destination_space)`.
3. Why `visited` is necessary.
4. Why BFS is optimal for unit-cost actions and DFS is not guaranteed optimal.
5. How parent pointers reconstruct the ordered operation list.
6. Why the gcd condition can reject impossible instances before search.

## 13. Sources / honesty note

Concepts are based on standard introductory AI state-space search and graph-search material. For submission, add the textbook/course notes or web sources you actually consulted and keep the honesty note accurate. This repository was prepared with AI assistance; the student should review, test, understand, and modify the code before submission.

## 14. Version-control checklist

Before submission:

- Make at least 3 meaningful commits across 2+ calendar days under your own GitHub identity.
- Tag the final commit `v1.0`.
- Check `git log --oneline --decorate` and `git config user.name/user.email`.
- Do not commit `.venv`, caches, generated binaries, or large datasets.
