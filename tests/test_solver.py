import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from solver import JugProblem, bfs, dfs, solve, validate_problem
from variant import build_variant


def test_classic_bfs_solution():
    problem = JugProblem(4, 3, 2)
    path, expanded = bfs(problem)
    assert path
    assert problem.is_goal(path[-1][1])
    assert len(path) == 4
    assert expanded > 0


def test_dfs_finds_solution():
    problem = JugProblem(4, 3, 2)
    path, expanded = dfs(problem)
    assert path
    assert problem.is_goal(path[-1][1])
    assert expanded > 0


def test_unreachable_instance():
    problem = JugProblem(4, 6, 5)
    assert not validate_problem(problem)
    assert solve(problem, "bfs") == ([], 0)


def test_invalid_method():
    try:
        solve(JugProblem(4, 3, 2), "astar")
    except ValueError as exc:
        assert "method" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_personal_variant_is_deterministic():
    v1 = build_variant(123456, 7)
    v2 = build_variant(123456, 7)
    assert v1 == v2
    assert v1.target <= max(v1.capacity_a, v1.capacity_b)
