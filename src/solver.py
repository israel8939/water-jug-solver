from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, Iterable, List, Optional, Tuple

State = Tuple[int, int]


@dataclass(frozen=True)
class JugProblem:
    """Water-jug state-space problem.

    Each state is (amount_in_jug_a, amount_in_jug_b).
    """

    capacity_a: int
    capacity_b: int
    target: int

    def __post_init__(self) -> None:
        if self.capacity_a <= 0 or self.capacity_b <= 0:
            raise ValueError("Jug capacities must be positive integers.")
        if self.target < 0 or self.target > max(self.capacity_a, self.capacity_b):
            raise ValueError(
                "Target must be non-negative and no larger than the biggest jug."
            )

    @property
    def start(self) -> State:
        return (0, 0)

    def is_goal(self, state: State) -> bool:
        return self.target in state

    def transitions(self, state: State) -> Iterable[Tuple[str, State]]:
        """Return all valid actions from a state."""
        a, b = state
        ca, cb = self.capacity_a, self.capacity_b

        yield "Fill A", (ca, b)
        yield "Fill B", (a, cb)
        yield "Empty A", (0, b)
        yield "Empty B", (a, 0)

        pour_a_to_b = min(a, cb - b)
        yield "Pour A -> B", (a - pour_a_to_b, b + pour_a_to_b)

        pour_b_to_a = min(b, ca - a)
        yield "Pour B -> A", (a + pour_b_to_a, b - pour_b_to_a)


def reconstruct_path(
    parents: Dict[State, Optional[State]], actions: Dict[State, str], goal: State
) -> List[Tuple[str, State]]:
    path: List[Tuple[str, State]] = []
    current = goal
    while parents[current] is not None:
        path.append((actions[current], current))
        parent = parents[current]
        assert parent is not None
        current = parent
    path.reverse()
    return path


def bfs(problem: JugProblem) -> Tuple[List[Tuple[str, State]], int]:
    """Breadth-first search; returns a shortest operation sequence."""
    queue: Deque[State] = deque([problem.start])
    visited = {problem.start}
    parents: Dict[State, Optional[State]] = {problem.start: None}
    actions: Dict[State, str] = {}
    expanded = 0

    while queue:
        state = queue.popleft()
        expanded += 1
        if problem.is_goal(state):
            return reconstruct_path(parents, actions, state), expanded

        for action, next_state in problem.transitions(state):
            if next_state not in visited:
                visited.add(next_state)
                parents[next_state] = state
                actions[next_state] = action
                queue.append(next_state)

    return [], expanded


def dfs(problem: JugProblem) -> Tuple[List[Tuple[str, State]], int]:
    """Depth-first search using an explicit stack."""
    stack: List[State] = [problem.start]
    visited = {problem.start}
    parents: Dict[State, Optional[State]] = {problem.start: None}
    actions: Dict[State, str] = {}
    expanded = 0

    while stack:
        state = stack.pop()
        expanded += 1
        if problem.is_goal(state):
            return reconstruct_path(parents, actions, state), expanded

        # Reverse insertion keeps the displayed action order intuitive.
        successors = list(problem.transitions(state))
        for action, next_state in reversed(successors):
            if next_state not in visited:
                visited.add(next_state)
                parents[next_state] = state
                actions[next_state] = action
                stack.append(next_state)

    return [], expanded


def validate_problem(problem: JugProblem) -> bool:
    """Check the standard gcd reachability condition."""
    from math import gcd

    return problem.target % gcd(problem.capacity_a, problem.capacity_b) == 0


def solve(problem: JugProblem, method: str = "bfs") -> Tuple[List[Tuple[str, State]], int]:
    """Dispatch to BFS or DFS and reject impossible instances early."""
    if not validate_problem(problem):
        return [], 0
    method = method.lower()
    if method == "bfs":
        return bfs(problem)
    if method == "dfs":
        return dfs(problem)
    raise ValueError("method must be 'bfs' or 'dfs'")
