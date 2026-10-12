from src.city_integration import show_jug_operations
from src.project_config import REGISTER_NUMBER, VARIANT_ID
from src.variant import build_variant
from src.solver import JugProblem, solve


def test_integration_uses_student_configuration():
    variant = build_variant(REGISTER_NUMBER, VARIANT_ID)
    assert variant.capacity_a > 0
    assert variant.capacity_b > 0
    assert variant.target >= 0


def test_bfs_integration_reaches_target():
    variant = build_variant(REGISTER_NUMBER, VARIANT_ID)
    problem = JugProblem(
        variant.capacity_a,
        variant.capacity_b,
        variant.target,
    )
    path, expanded = solve(problem, "bfs")

    assert path
    assert problem.is_goal(path[-1][1])
    assert expanded > 0


def test_dfs_integration_reaches_target():
    variant = build_variant(REGISTER_NUMBER, VARIANT_ID)
    problem = JugProblem(
        variant.capacity_a,
        variant.capacity_b,
        variant.target,
    )
    path, expanded = solve(problem, "dfs")

    assert path
    assert problem.is_goal(path[-1][1])
    assert expanded > 0


def test_bfs_operation_display(capsys):
    show_jug_operations("bfs")
    output = capsys.readouterr().out

    assert "JUG METERING SIMULATION" in output
    assert "Operations: 2" in output
    assert "not physical valve commands" in output
