# STEP 5 — CAPSTONE: a tiny software team
#
#   request ─► Planner ─► spec ─► Coder ─► solution.py
#                                   ▲          │
#                                   │      Tester writes test_solution.py
#                                   │          │
#                                   └─ fail ◄─ our code RUNS the tests ─► pass ─► ship 🚀
#
# Everything from the course in one file:
#   • agents with different jobs, prompts and tools        (module 1)
#   • a pipeline (plan → code → test)                      (step 1)
#   • a feedback loop until the work is good               (step 2)
#   • real tools in a sandbox                              (module 1, step 5)
# Plus one new rule: DON'T TRUST, VERIFY. The agents say "done" all the time.
# Our code runs the tests itself and believes the exit code, not the agent.
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from module1_single_agent.agent import Agent
import toolbox
from toolbox import write_file, read_file, run_python
from llm import paint

toolbox.AUTO_APPROVE = True  # the team writes/runs many files; still locked inside ./workspace

planner = Agent(
    "Planner", color="blue",
    instructions="You turn a feature request into a precise spec for ONE Python function: "
                 "its name, parameters, return value, edge cases, and 4 example input → output pairs. "
                 "No code. Be short and exact.",
)
coder = Agent(
    "Coder", color="green", tools=[write_file, read_file], memory=True,
    instructions="You implement the spec as a Python function in solution.py using write_file. "
                 "Only the function (plus imports) — no tests, no input(), no prints. "
                 "When you get a failing test report, read it, fix solution.py, and write it again.",
)
tester = Agent(
    "Tester", color="magenta", tools=[write_file, run_python], memory=True,
    instructions="You write test_solution.py for the spec: `from solution import *`, then 5-8 plain "
                 "assert statements at the TOP LEVEL of the file (not inside a function), taken from "
                 "the spec's examples, and as the last line print('ALL TESTS PASSED'). "
                 "Write it with write_file, run it once with run_python, and report what happened. "
                 "Do NOT edit solution.py.",
)

request = " ".join(sys.argv[1:]) or ("A function that checks if a password is strong: at least 8 "
                                     "characters, one uppercase letter, one digit and one symbol.")
print(paint("📋 Request: ", "bold") + request)

spec = planner.run(request)
coder.run(f"Implement this spec in solution.py:\n{spec}")
tester.run(f"Write and run tests for this spec:\n{spec}")

for round_number in range(1, 5):
    # Missing files? Send the job back to whoever skipped it.
    if not (toolbox.WORKSPACE / "solution.py").exists():
        print(paint("\n   → there is no solution.py yet. Back to the Coder.", "gray"))
        coder.run("solution.py does not exist. Write it now with the write_file tool.")
        continue
    if not (toolbox.WORKSPACE / "test_solution.py").exists():
        print(paint("\n   → there is no test file yet. Back to the Tester.", "gray"))
        tester.run("test_solution.py does not exist. Create it now with the write_file tool.")
        continue
    report = run_python("test_solution.py")  # 👈 our code checks — not an agent
    ran_ok = report.startswith("exit code 0")
    passed = ran_ok and "ALL TESTS PASSED" in report
    print(paint(f"\n🧪 Test run {round_number}: ", "bold") +
          (paint("PASS", "green") if passed else paint("FAIL", "red")))
    if passed:
        print(paint("\n🚀 Shipped! See workspace/solution.py and workspace/test_solution.py", "bold"))
        break
    # Who gets the feedback? Send the problem to the agent who can fix it.
    if ran_ok:  # no crash, but the final print never happened → the TEST file is broken
        print(paint("   → the tests never actually ran. Back to the Tester.", "gray"))
        tester.run("test_solution.py ran but never printed ALL TESTS PASSED, so your asserts never ran. "
                   "Rewrite it with the asserts at the top level of the file.")
    else:       # an assert failed or the code crashed → back to the Coder
        print(paint("   → a test failed. Back to the Coder.", "gray"))
        coder.run(f"The tests failed. Here is the report:\n{report}\nFix solution.py.")
else:
    print(paint("\n⚠️  Still failing after 4 rounds — time for a human to look.", "red"))
    print("   (Sometimes the TEST is wrong, not the code. Open both files and decide.)")

# 🧪 TRY IT:
#   python module2_multi_agent/step5_dev_team.py "A function that converts Roman numerals to integers"
#   Add a 4th agent: a "Reviewer" who reads solution.py and suggests one improvement after it passes.
