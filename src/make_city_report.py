"""Generate the Smart City Water Allocation project report."""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Preformatted,
)

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPORT_PATH = DOCS / "smart_city_report.pdf"
DOCS.mkdir(exist_ok=True)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle", parent=styles["Title"],
    fontSize=21, leading=28, alignment=TA_CENTER, spaceAfter=20,
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading1"],
    fontSize=15, leading=19, spaceBefore=14, spaceAfter=8,
    textColor=colors.HexColor("#163A5F"),
))
styles.add(ParagraphStyle(
    name="SubSection", parent=styles["Heading2"],
    fontSize=11, leading=14, spaceBefore=9, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="BodyTextCustom", parent=styles["BodyText"],
    fontSize=9.5, leading=14, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="SmallCustom", parent=styles["BodyText"],
    fontSize=8, leading=11, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="CodeCustom", parent=styles["Code"],
    fontName="Courier", fontSize=8, leading=10,
))

story = []

def para(text, style="BodyTextCustom"):
    story.append(Paragraph(text, styles[style]))

def heading(text):
    para(text, "Section")

def table(headers, rows, widths=None):
    data = [[Paragraph(str(v), styles["SmallCustom"]) for v in headers]]
    for row in rows:
        data.append([Paragraph(str(v), styles["SmallCustom"]) for v in row])
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F1")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#163A5F")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

def footer(canvas, document):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, 1.1 * cm, "Smart City Water Allocation System")
    canvas.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f"Page {document.page}")
    canvas.restoreState()

# Cover page
story.append(Spacer(1, 1.8 * cm))
para("FOUNDATIONS OF ARTIFICIAL INTELLIGENCE", "CoverTitle")
para("SMART CITY WATER ALLOCATION SYSTEM", "CoverTitle")
para("Water Jug Search, Constraint Satisfaction and Rule-Based Diagnosis", "SubSection")
story.append(Spacer(1, 1.3 * cm))
para("<b>Submitted by</b>", "BodyTextCustom")
para("ISRAEL P", "BodyTextCustom")
para("Register Number: 113025148035", "BodyTextCustom")
para("B.E. Computer Science and Engineering (AI &amp; ML)", "BodyTextCustom")
para("Second Year - Third Semester", "BodyTextCustom")
story.append(Spacer(1, 0.5 * cm))
para("<b>Course Code:</b> 25ML35T", "BodyTextCustom")
para("<b>Submitted to:</b> Dr. Manoj Kumar D S, Associate Professor", "BodyTextCustom")
para("<b>Department:</b> CSE (AI &amp; ML)", "BodyTextCustom")
para("<b>Academic Year:</b> 2026-2027", "BodyTextCustom")
story.append(Spacer(1, 1.2 * cm))
para("Project report generated from the current implementation and recorded test results.", "SmallCustom")
story.append(PageBreak())

heading("Abstract")
para(
    "This project combines a classical Water Jug Problem solver with a "
    "prototype Smart City Water Allocation System. Breadth-First Search (BFS) "
    "and Depth-First Search (DFS) find sequences of jug operations. A "
    "constraint-satisfaction model allocates reservoir water to a hospital "
    "and two residential zones while respecting reservoir availability, "
    "pipeline limits and minimum daily supply constraints. A rule-based "
    "diagnosis module flags possible leaks or shortages from supplied "
    "indicators. The current automated test suite reports 16 passing tests. "
    "This is a software simulation, not a live water-control system."
)
heading("1. Objectives")
for item in [
    "Model the Water Jug Problem as a finite state-space search problem.",
    "Implement and test BFS and DFS solution paths.",
    "Allocate reservoir water to zones using constraint satisfaction and backtracking.",
    "Compare search effort with and without constraint propagation.",
    "Demonstrate transparent rule-based leak and shortage warnings.",
    "Document minimum-supply constraints, limitations and responsible-use considerations.",
]:
    para("&#8226; " + item)

heading("2. Introduction and Problem Formulation")
para(
    "The Water Jug Problem represents states as pairs (A, B), where A and B "
    "are the current amounts of water in two jugs. Legal actions include "
    "filling, emptying and pouring between jugs. A goal state has the target "
    "amount in at least one jug. BFS explores states level by level and "
    "returns a shortest path in an unweighted state graph; DFS explores a "
    "branch before backtracking and does not guarantee a shortest path."
)
para(
    "The extension models water allocation as a constraint-satisfaction "
    "problem (CSP). Reservoir supplies are finite, pipeline flows have "
    "limits, and each zone has a minimum daily demand. The solver searches "
    "for an allocation satisfying the encoded constraints."
)

heading("3. AI Concepts Used")
para("<b>State-space search:</b> BFS and DFS explore reachable jug states.")
para("<b>Constraint satisfaction:</b> reservoir-to-zone flows must satisfy supply, pipeline and minimum-demand constraints.")
para("<b>Backtracking:</b> the allocation solver explores candidate assignments and reverses choices when constraints cannot be satisfied.")
para("<b>Constraint propagation:</b> impossible candidate assignments are pruned earlier, reducing search effort in the recorded scenarios.")
para("<b>Rule-based reasoning:</b> input indicators activate diagnosis rules and produce a label, certainty factor and explanation.")

heading("4. System Architecture")
table(
    ["Component", "Responsibility"],
    [
        ["project_config.py", "Stores the register number and configured variant ID."],
        ["solver.py / variant.py", "Defines the jug problem and BFS/DFS search."],
        ["water_allocation.py", "Defines zones, reservoir scenarios, pipeline limits and CSP search."],
        ["diagnosis.py", "Applies rule-based leak and shortage diagnosis."],
        ["city_integration.py", "Presents jug search and city allocations in one demonstration."],
        ["tests/", "Automated checks for search, allocation, diagnosis and integration."],
        ["results/", "Stores recorded demonstration outputs and benchmark data."],
    ],
    [4.2 * cm, 12 * cm],
)

heading("5. Methodology")
para(
    "The jug solver represents each state as a pair of integer volumes. "
    "BFS uses a queue and DFS uses a stack; visited-state handling prevents "
    "unbounded revisiting. The configured instance uses jug capacities of "
    "4 L and 5 L with a 1 L target. This configuration is controlled by "
    "the local variant settings and should be confirmed against the instructor's assignment."
)
para(
    "The allocation model uses 10 kL units. Its minimum-supply rule is "
    "10 litres per person per day. The encoded zone populations produce "
    "minimums of 3 units for the Hospital, 3 for Residential East and 2 "
    "for Residential West. Reservoir and pipeline constraints are applied "
    "during search."
)
table(
    ["Scenario", "North supply", "South supply", "Hospital minimum", "East minimum", "West minimum"],
    [
        ["Normal", "9 units", "6 units", "3 units", "3 units", "2 units"],
        ["Drought", "5 units", "4 units", "3 units", "3 units", "2 units"],
    ],
    [2.4 * cm, 2.4 * cm, 2.4 * cm, 2.8 * cm, 2.8 * cm, 2.8 * cm],
)

heading("6. Rule-Based Diagnosis")
table(
    ["Condition", "Output", "Certainty factor"],
    [
        ["Low pressure AND high flow", "LeakSuspected", "0.8"],
        ["Low reservoir AND insufficient supply", "WaterShortageSuspected", "0.9"],
        ["No listed rule matches", "NoKnownIssueDetected", "0.7"],
    ],
    [6 * cm, 5 * cm, 3.5 * cm],
)
para(
    "Example trace: low pressure = true and high flow = true activates "
    "the LeakSuspected rule with CF 0.8. These certainty factors are "
    "illustrative rule weights, not calibrated probabilities and not "
    "proof of a real leak. Field use would require validated sensors, "
    "calibration and human review."
)

heading("7. Implementation and Reproducibility")
para(
    "The project is implemented in Python. Tests are run with pytest. "
    "From the repository root, use the commands below in an environment "
    "where the dependencies in requirements.txt are installed."
)
story.append(Preformatted(
    "python -m pytest -v\n"
    "python -m src.smart_city_demo\n"
    "python -m src.city_integration\n"
    "python src/main.py --roll-number 113025148035 --variant-id 1 --method bfs\n"
    "python src/main.py --roll-number 113025148035 --variant-id 1 --method dfs",
    styles["CodeCustom"],
))
para(
    "The integration output is recorded in results/city_integration.txt; "
    "the standalone allocation and diagnosis demonstration is recorded in "
    "results/smart_city_demo.txt. Confirm that these outputs match the "
    "current code before submission."
)

heading("8. Results and Observations")
table(
    ["Scenario", "Hospital", "Residential East", "Residential West", "North used", "South used"],
    [
        ["Normal", "60 kL/day", "50 kL/day", "40 kL/day", "9/9 units", "6/6 units"],
        ["Drought", "40 kL/day", "30 kL/day", "20 kL/day", "5/5 units", "4/4 units"],
    ],
    [2.2 * cm, 2.8 * cm, 3.2 * cm, 3.2 * cm, 2.6 * cm, 2.6 * cm],
)
table(
    ["Scenario", "Propagation", "Nodes visited", "Pruned branches"],
    [
        ["Normal", "Disabled", "475", "469"],
        ["Normal", "Enabled", "6", "0"],
        ["Drought", "Disabled", "1377", "1371"],
        ["Drought", "Enabled", "7", "1"],
    ],
    [3.2 * cm, 3.2 * cm, 3.2 * cm, 3.5 * cm],
)
para(
    "The recorded node counts show substantially less search effort with "
    "propagation for these two scenarios. Node counts are not execution "
    "times and should not be generalized beyond the tested model."
)
table(
    ["Jug search method", "Recorded operations", "Expanded nodes", "Observation"],
    [
        ["BFS", "2", "6", "Shortest path for the configured unweighted problem."],
        ["DFS", "12", "14", "Valid path, but longer than BFS in this instance."],
    ],
    [2.6 * cm, 3 * cm, 3 * cm, 6.5 * cm],
)
para(
    "The automated suite completed with 16 passed tests in 0.06 seconds "
    "in the recorded run. This includes tests for jug search, configured "
    "integration, diagnosis rules and allocation constraints."
)

heading("9. Responsible AI, Limitations and Future Work")
para(
    "The encoded minimum daily supply provides a baseline service constraint. "
    "The model reports zone allocations and reservoir usage so that results "
    "can be inspected. Hospital priority currently affects search ordering; "
    "it is not a formal optimization objective and does not guarantee a "
    "globally fair allocation beyond the encoded constraints."
)
para(
    "The scenarios and diagnosis inputs are simulated. The certainty factors "
    "are illustrative. The model does not account for real-time demand, "
    "water quality, losses, changing population, energy costs, uncertainty "
    "or physical network hydraulics. The jug sequence is a metering "
    "illustration and must not be interpreted as a physical valve command."
)
para(
    "Future work could add validated real-world data, explicit fairness "
    "objectives, uncertainty-aware diagnosis, a user interface, more scenarios, "
    "and a human approval step before any operational decision."
)

heading("10. Conclusion")
para(
    "The project demonstrates how classical search can be integrated with "
    "constraint satisfaction and rule-based reasoning in a simulated Smart "
    "City water allocation use case. The recorded tests verify the current "
    "implemented behaviors, while the scenario results illustrate the "
    "effect of constraint propagation. Real deployment would require "
    "additional engineering, validated data and operational safeguards."
)

heading("11. References")
for item in [
    "Russell, S. and Norvig, P., Artificial Intelligence: A Modern Approach, 4th edition, Pearson.",
    "Python documentation: https://docs.python.org/3/",
    "pytest documentation: https://docs.pytest.org/",
    "ReportLab documentation: https://docs.reportlab.com/",
]:
    para("&#8226; " + item)

heading("Final Submission Checklist")
for item in [
    "Confirm the assigned variant ID with the instructor.",
    "Run the tests again and retain the final test output.",
    "Check the generated report against the actual implementation and college template.",
    "Add genuine screenshots and the actual GitHub repository URL if required by the template.",
    "Verify Git history, meaningful commits on at least two calendar days, and the v1.0 tag.",
    "Ensure .venv, caches and backup files are excluded from the submitted repository.",
]:
    para("&#9744; " + item)

document = SimpleDocTemplate(
    str(REPORT_PATH), pagesize=A4,
    rightMargin=2 * cm, leftMargin=2 * cm,
    topMargin=1.8 * cm, bottomMargin=1.8 * cm,
    title="Smart City Water Allocation System Project Report",
    author="ISRAEL P",
)
document.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"Created report: {REPORT_PATH}")
