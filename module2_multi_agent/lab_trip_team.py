# 🛠  LAB 2 — Build a trip-planning TEAM  (≈30 min)
#
#   request ─► Planner ─► itinerary ─► Budget Checker ─► over budget? ─ yes ─► back to Planner
#                                                           │ no
#                                                           ▼
#                                                        final plan
#
# You'll combine a pipeline (step 1) with a feedback loop (step 2).
# Fill in the TODOs. Run:  python module2_multi_agent/lab_trip_team.py
# Answer: solutions/lab_trip_team.py
import json
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from module1_single_agent.agent import Agent
from toolbox import calculate, wiki_search
from llm import client, MODEL, paint

BUDGET = 15000  # rupees

# TODO 1: the Planner. Tools: wiki_search (to learn about the place).
#   Instructions: plan a day-by-day trip and list the COST of every item in rupees.
#   memory=True, so it remembers its plan when the budget checker complains.
planner = None


def check_budget(plan):
    """TODO 2: the Budget Checker — one JSON call (like the critic in step 2).
    Ask the model to add up every cost in the plan and reply:
        {"total": 12345, "within_budget": true/false, "advice": "what to cut"}
    Then print the verdict and return the dict.
    Hint: copy critique() from step2_critic_loop.py and change the prompt.
    Hint: add "Always reply in English" — some local models switch language in JSON mode."""
    ...


request = " ".join(sys.argv[1:]) or f"A 3-day trip to Jaipur for 2 college students. Budget ₹{BUDGET}."

# TODO 3: the loop.
#   plan = planner.run(request)
#   up to 3 times: check the budget; if within budget → stop; else send the advice back to the planner
#   Finally print the plan.

# ⭐ BONUS: the model is bad at adding big lists of numbers. Give the Budget Checker
#   the `calculate` tool (make it an Agent instead of one JSON call). Is the total more accurate?
