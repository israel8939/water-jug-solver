# Smart City Water Allocation System + Water Jug Problem Solver

A Python-based Artificial Intelligence project combining state-space search, a Constraint Satisfaction Problem (CSP), constraint propagation, and rule-based diagnosis.

The project extends a classic Water Jug Problem Solver into a simplified Smart City Water Allocation System. It demonstrates water allocation under normal and drought conditions, compares search effort with and without constraint propagation, and explains a sample leak diagnosis.

> **Scope:** This is an educational simulation using illustrative data. It is not a real water-distribution controller, and its certainty factors are not calibrated probabilities.

## 1. Project objectives

- Solve the classic Water Jug Problem using Breadth-First Search (BFS) and Depth-First Search (DFS).
- Allocate water from multiple reservoirs to hospital and residential zones.
- Respect reservoir capacities, pipeline limits, zone demand limits, and minimum daily supply constraints.
- Compare CSP search effort with and without constraint propagation.
- Apply rule-based reasoning to identify possible leaks or water shortages.
- Produce understandable output that can be checked and reproduced.

## 2. Technologies

- Python 3.10+
- `pytest` for automated tests
- `matplotlib` for existing benchmark plots
- Python standard library for the allocation and diagnosis logic

Install dependencies using `python -m pip install -r requirements.txt`.

## 3. Project structure

```text
water_jug_solver/
├── src/
│   ├── __init__.py
│   ├── benchmark.py
│   ├── diagnosis.py
│   ├── main.py
│   ├── make_plot.py
│   ├── make_report.py
│   ├── project_config.py
│   ├── smart_city_demo.py
│   ├── solver.py
│   ├── variant.py
│   └── water_allocation.py
├── tests/
│   ├── test_diagnosis.py
│   ├── test_solver.py
│   └── test_water_allocation.py
├── docs/
│   ├── report.pdf
│   ├── bfs_vs_dfs.png
│   └── runtime_comparison.png
├── results/
│   └── smart_city_demo.txt
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## 4. Setup from a fresh clone

Clone your repository and enter the project root directory:

```bash
git clone <YOUR-REPOSITORY-URL>
cd water_jug_solver
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the automated tests:

```bash
python -m pytest -v
```

The current development version passes **12 tests** on the author's machine. Run the tests again after cloning; results may differ if the code or environment changes.

## 5. Original Water Jug Problem Solver

Each state is represented as `(x, y)`, where `x` and `y` are the current amounts in jugs A and B.

Supported actions:

- Fill jug A or B
- Empty jug A or B
- Pour A into B
- Pour B into A

The goal is reached when the target amount is present in either jug.

### Run BFS

```bash
python src/main.py --capacity-a 4 --capacity-b 3 --target 2 --method bfs
```

BFS explores states using a FIFO queue and returns a shortest action sequence when all actions have equal cost.

### Run DFS

```bash
python src/main.py --capacity-a 4 --capacity-b 3 --target 2 --method dfs
```

DFS explores using a stack. It can find a solution, but it does not guarantee the shortest solution.

### Personalised variant

Use your own register number and the exact variant ID assigned by your instructor:

```bash
python src/main.py --roll-number YOUR_REGISTER_NUMBER --variant-id YOUR_ASSIGNED_VARIANT --method bfs
```

Replace both placeholders with actual integer values before running the command. The variant generator uses a deterministic seed so the same inputs reproduce the same variant.

## 6. Smart City Water Allocation System

The allocation module models a simplified city with two reservoirs and three service zones:

- Hospital
- Residential East
- Residential West

The CSP solver searches for an allocation that satisfies the configured constraints.

### Constraints

1. Reservoir use must not exceed available capacity.
2. Each pipeline must stay within its configured limit.
3. Every zone must receive at least its configured minimum allocation.
4. Zone allocations must not exceed configured demand.
5. Hospital priority influences the search order; the implementation should not be interpreted as a formal proof of globally optimal fairness.

The model uses allocation units of **10 kL per day**. Its population and demand values are illustrative and should not be interpreted as actual city data.

### Run the complete demonstration

From the project root:

```bash
python -m src.smart_city_demo
```

This runs normal and drought scenarios, compares search effort with and without propagation, and demonstrates the leak-diagnosis rule.

Save the output to a text file:

```powershell
python -m src.smart_city_demo | Tee-Object -FilePath results\smart_city_demo.txt
```

## 7. Sample allocation results

The current demonstration produces the following results:

| Zone | Normal supply | Drought supply |
|---|---:|---:|
| Hospital | 60 kL/day | 40 kL/day |
| Residential East | 50 kL/day | 30 kL/day |
| Residential West | 40 kL/day | 20 kL/day |
| **Total** | **150 kL/day** | **90 kL/day** |

These are the results from the current configured scenarios, not real-world recommendations.

The normal scenario has 150 kL/day of reservoir capacity available. The drought scenario has 90 kL/day available. The current solutions use all available capacity while respecting the configured constraints.

## 8. Constraint propagation experiment

The current program reports these node counts:

| Scenario | Without propagation | With propagation |
|---|---:|---:|
| Normal | 475 | 6 |
| Drought | 1,377 | 7 |

For these runs, propagation reduces the number of visited search nodes substantially. These counts are specific to the current implementation and configuration. Node counts are not the same as elapsed runtime, and the results do not guarantee the same improvement for every CSP.

## 9. Rule-based diagnosis

The diagnosis module includes example rules such as:

```text
PressureLow AND FlowHigh
    -> LeakSuspected (CF = 0.8)

ReservoirLow AND SupplyInsufficient
    -> WaterShortageSuspected (CF = 0.9)
```

For example, the demo supplies low-pressure and high-flow observations and prints `LeakSuspected` along with the rule explanation.

The certainty factors are illustrative confidence values used to demonstrate rule-based reasoning. They are not probabilities, sensor-calibrated confidence values, or evidence that a physical leak actually exists.

## 10. Existing benchmark and plots

Run the existing BFS/DFS benchmark:

```bash
python src/benchmark.py
```

Generate the existing plots:

```bash
python src/make_plot.py
```

The existing scripts produce benchmark data and comparison plots. Check their output paths and repository status before committing generated files.

## 11. Complexity notes

For the Water Jug Problem, let `S` be the number of reachable states. Each state has at most six legal actions.

- BFS has `O(S)` time and `O(S)` space on this bounded graph.
- DFS has `O(S)` worst-case time and `O(S)` space when tracking visited states, parents, and the stack.

For the allocation CSP, practical search effort depends on variable domains, constraints, variable ordering, and propagation. The observed node counts are experimental results, not a general complexity guarantee.

## 12. Limitations and future improvements

- The water-allocation data is synthetic and simplified.
- The model does not represent a full real-world hydraulic network.
- The hospital-priority heuristic is not a formal optimization objective.
- Fairness could be improved with explicit per-capita reporting and a defined fairness objective.
- Diagnosis rules require real sensor data and validation before operational use.
- The certainty factors have not been calibrated against observed incidents.
- A future interface could use Streamlit to let users change reservoir capacity, demand, and sensor readings.

## 13. References and academic honesty

Before submission, add the specific course notes, textbooks, papers, or reliable online sources you actually consulted for BFS, DFS, constraint satisfaction, constraint propagation, and rule-based expert systems.

Do not list a source as consulted unless you have checked it. Review and understand every submitted module, test, and result, and follow your institution's policy for disclosing AI assistance.

## 14. Submission checklist

- [ ] Confirm `REGISTER_NUMBER` and `VARIANT_ID` in `src/project_config.py` match your actual assigned values.
- [ ] Run `python -m pytest -v`.
- [ ] Run `python -m src.smart_city_demo`.
- [ ] Update `docs/report.pdf` to describe both the original solver and the Smart City extension.
- [ ] Check that `README.md`, `requirements.txt`, `.gitignore`, and `LICENSE` are present.
- [ ] Ensure `.venv`, Python caches, and unnecessary generated files are not committed.
- [ ] Review `git status` before staging changes.
- [ ] Make meaningful commits under your own Git identity across at least two calendar days, as required.
- [ ] Tag the final reviewed version `v1.0`.
- [ ] Submit the correct GitHub repository URL through your course LMS.
