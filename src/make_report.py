from pathlib import Path
import csv
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)


# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"
DOCS_DIR = BASE_DIR / "docs"

REPORT_PATH = DOCS_DIR / "report.pdf"
CSV_PATH = RESULTS_DIR / "benchmark.csv"

BFS_DFS_PLOT = DOCS_DIR / "bfs_vs_dfs.png"
RUNTIME_PLOT = DOCS_DIR / "runtime_comparison.png"


# -------------------------------------------------
# Read benchmark data
# -------------------------------------------------
def read_results():
    data = []

    if CSV_PATH.exists():
        with open(CSV_PATH, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)

    return data


# -------------------------------------------------
# Create charts
# -------------------------------------------------
def create_charts(data):
    if not data:
        return

    problems = []
    bfs_expanded = []
    dfs_expanded = []
    bfs_runtime = []
    dfs_runtime = []

    grouped = {}

    for row in data:
        problem = row["case"]
        method = row["method"]

        if problem not in grouped:
            grouped[problem] = {}

        grouped[problem][method] = row

    for problem, methods in grouped.items():
        if "BFS" in methods and "DFS" in methods:
            problems.append(problem)

            bfs_expanded.append(
                int(methods["BFS"]["nodes_expanded"])
            )

            dfs_expanded.append(
                int(methods["DFS"]["nodes_expanded"])
            )

            bfs_runtime.append(
                float(methods["BFS"]["runtime_ms"])
            )

            dfs_runtime.append(
                float(methods["DFS"]["runtime_ms"])
            )

    # Nodes expanded chart
    plt.figure(figsize=(9, 5))

    x = range(len(problems))

    plt.plot(x, bfs_expanded, marker="o", label="BFS")
    plt.plot(x, dfs_expanded, marker="o", label="DFS")

    plt.xticks(x, problems, rotation=20)
    plt.xlabel("Water Jug Problems")
    plt.ylabel("Nodes Expanded")
    plt.title("BFS vs DFS: Nodes Expanded")
    plt.legend()
    plt.tight_layout()

    plt.savefig(BFS_DFS_PLOT, dpi=150)
    plt.close()

    # Runtime chart
    plt.figure(figsize=(9, 5))

    plt.plot(x, bfs_runtime, marker="o", label="BFS")
    plt.plot(x, dfs_runtime, marker="o", label="DFS")

    plt.xticks(x, problems, rotation=20)
    plt.xlabel("Water Jug Problems")
    plt.ylabel("Runtime (ms)")
    plt.title("BFS vs DFS: Runtime Comparison")
    plt.legend()
    plt.tight_layout()

    plt.savefig(RUNTIME_PLOT, dpi=150)
    plt.close()


# -------------------------------------------------
# Build PDF report
# -------------------------------------------------
def build_report():
    DOCS_DIR.mkdir(exist_ok=True)
    RESULTS_DIR.mkdir(exist_ok=True)

    data = read_results()
    create_charts(data)

    document = SimpleDocTemplate(
        str(REPORT_PATH),
        pagesize=A4,
        rightMargin=1.7 * cm,
        leftMargin=1.7 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=24,
        spaceAfter=15,
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=11,
        leading=15,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=10,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        alignment=TA_JUSTIFY,
        fontSize=10,
        leading=15,
        spaceAfter=8,
    )

    story = []

    # -------------------------------------------------
    # TITLE
    # -------------------------------------------------
    story.append(
        Paragraph(
            "Water Jug Problem Solver",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "State-Space Search using Breadth-First Search (BFS) "
            "and Depth-First Search (DFS)",
            subtitle_style,
        )
    )

    story.append(
        Paragraph(
            "<b>Course Project Report</b><br/>"
            "Student: __________________________<br/>"
            "Register Number: __________________<br/>"
            "Project: Water Jug Problem Solver",
            body_style,
        )
    )

    story.append(Spacer(1, 10))

    # -------------------------------------------------
    # 1 PROBLEM FORMULATION
    # -------------------------------------------------
    story.append(
        Paragraph(
            "1. Problem Formulation",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "The Water Jug Problem is a classical artificial intelligence "
            "state-space search problem. Two jugs with fixed capacities A "
            "and B are initially empty. The objective is to obtain a target "
            "quantity of water in either jug by applying a sequence of legal "
            "operations.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "<b>State Representation:</b> A state is represented as "
            "(x, y), where x is the current amount of water in Jug A and "
            "y is the current amount of water in Jug B. The initial state "
            "is (0, 0).",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "<b>Actions:</b> The legal actions are Fill A, Fill B, Empty A, "
            "Empty B, Pour A to B, and Pour B to A. Every action transforms "
            "the current state into a new valid state.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "<b>Goal Test:</b> A state is considered a goal when the target "
            "amount exists in either jug. Therefore, the goal condition is "
            "x = target or y = target.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "<b>Path Cost:</b> Each operation has a uniform cost of one. "
            "Therefore, the total path cost equals the number of operations "
            "used to reach the goal.",
            body_style,
        )
    )

    # -------------------------------------------------
    # 2 STATE TRANSITIONS
    # -------------------------------------------------
    story.append(
        Paragraph(
            "2. Modelling Actions as State Transitions",
            heading_style,
        )
    )

    transitions = [
        ["Action", "State Transition"],
        ["Fill A", "(x, y) -> (A, y)"],
["Fill B", "(x, y) -> (x, B)"],
["Empty A", "(x, y) -> (0, y)"],
["Empty B", "(x, y) -> (x, 0)"],
["Pour A -> B", "Transfer water until A is empty or B is full"],
["Pour B -> A", "Transfer water until B is empty or A is full"],
        
    ]

    table = Table(
        transitions,
        colWidths=[4.2 * cm, 11 * cm],
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(table)

    # -------------------------------------------------
    # 3 APPROACH
    # -------------------------------------------------
    story.append(
        Paragraph(
            "3. Approach and Algorithms",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "<b>Breadth-First Search (BFS):</b> BFS explores the state "
            "space level by level using a FIFO queue. Since every operation "
            "has the same cost, BFS guarantees that the first solution found "
            "contains the minimum possible number of operations. A visited "
            "set prevents repeated exploration of states, while parent "
            "pointers are used to reconstruct the ordered solution path.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "<b>Depth-First Search (DFS):</b> DFS explores one branch of "
            "the state space as deeply as possible before backtracking. "
            "It uses a LIFO stack. DFS may reach a solution while exploring "
            "fewer states, but it does not guarantee the shortest sequence "
            "of operations.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Both algorithms demonstrate the concept of modelling a problem "
            "as a graph where each node is a state and each edge is a legal "
            "action. The final output reconstructs the path from the start "
            "state to the goal state.",
            body_style,
        )
    )

    # -------------------------------------------------
    # 4 COMPLEXITY
    # -------------------------------------------------
    story.append(
        Paragraph(
            "4. Complexity Analysis",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "For jug capacities A and B, the maximum number of possible "
            "states is S = (A + 1)(B + 1). Each state has at most six "
            "possible actions. Therefore, in the bounded state-space graph, "
            "both BFS and DFS have time complexity O(S) and space complexity "
            "O(S). The practical performance depends on the order in which "
            "states are explored.",
            body_style,
        )
    )

    complexity_data = [
        ["Algorithm", "Time Complexity", "Space Complexity", "Guarantee"],
        ["BFS", "O(S)", "O(S)", "Shortest path"],
        ["DFS", "O(S)", "O(S)", "Solution not always shortest"],
    ]

    complexity_table = Table(
        complexity_data,
        colWidths=[3 * cm, 4 * cm, 4 * cm, 5 * cm],
    )

    complexity_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(complexity_table)

    story.append(PageBreak())

    # -------------------------------------------------
    # 5 RESULTS
    # -------------------------------------------------
    story.append(
        Paragraph(
            "5. Experimental Results and Comparison",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "The solver was evaluated on multiple Water Jug Problem "
            "configurations. The benchmark compares BFS and DFS using three "
            "main metrics: number of solution steps, nodes expanded, and "
            "execution runtime.",
            body_style,
        )
    )

    if data:
        result_table = [
            [
                "Problem",
                "Method",
                "Steps",
                "Nodes Expanded",
                "Runtime (ms)",
            ]
        ]

        for row in data:
            result_table.append(
                [
                    row["case"],
                    row["method"],
                    row["steps"],
                    row["nodes_expanded"],
                    f'{float(row["runtime_ms"]):.4f}',
                ]
            )

        table = Table(
            result_table,
            repeatRows=1,
            colWidths=[
                3.2 * cm,
                2.2 * cm,
                2 * cm,
                4 * cm,
                3.2 * cm,
            ],
        )

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("PADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )

        story.append(table)

    story.append(Spacer(1, 15))

    # -------------------------------------------------
    # Charts
    # -------------------------------------------------
    if BFS_DFS_PLOT.exists():
        story.append(
            Paragraph(
                "Figure 1: Comparison of Nodes Expanded",
                heading_style,
            )
        )

        story.append(
            Image(
                str(BFS_DFS_PLOT),
                width=15 * cm,
                height=8.3 * cm,
            )
        )

    story.append(PageBreak())

    if RUNTIME_PLOT.exists():
        story.append(
            Paragraph(
                "Figure 2: Runtime Comparison",
                heading_style,
            )
        )

        story.append(
            Image(
                str(RUNTIME_PLOT),
                width=15 * cm,
                height=8.3 * cm,
            )
        )

    story.append(
        Paragraph(
            "Interpretation of Results",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "The results show that BFS consistently provides an optimal "
            "solution in terms of the number of operations because it "
            "explores states level by level. DFS can sometimes expand fewer "
            "nodes and execute faster, but its solution may contain more "
            "steps. Therefore, BFS is preferred when the shortest sequence "
            "of operations is important, while DFS can be useful when memory "
            "or quick exploration is the primary concern.",
            body_style,
        )
    )

    # -------------------------------------------------
    # 6 REFLECTION
    # -------------------------------------------------
    story.append(
        Paragraph(
            "6. Reflection and Future Improvements",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "The most challenging part of the project was correctly "
            "representing the Water Jug Problem as a finite state-space "
            "graph and ensuring that repeated states did not create cycles. "
            "The use of a visited set solved this issue, while parent "
            "pointers made it possible to display the ordered sequence of "
            "operations.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Future improvements could include an interactive graphical "
            "interface, animation of water transfers, support for more than "
            "two jugs, and additional search algorithms such as Uniform "
            "Cost Search or A*. Another improvement would be allowing users "
            "to enter custom jug capacities and targets directly through a "
            "user interface.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "<b>Honesty Note:</b> AI tools were used for guidance and "
            "documentation assistance. The algorithms, code structure, "
            "execution, testing, and project understanding were reviewed "
            "and verified by the student.",
            body_style,
        )
    )

    document.build(story)

    print(f"Created {REPORT_PATH}")


if __name__ == "__main__":
    build_report()