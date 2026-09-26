# ✅ LAB 2 — SOLUTION
import json
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))
from module1_single_agent.agent import Agent
from toolbox import calculate, wiki_search
from llm import client, MODEL, paint

BUDGET = 15000

planner = Agent(
    "Planner", color="blue", tools=[wiki_search], memory=True,
    instructions="You plan budget trips for students. Use wiki_search once to learn about the place. "
                 "Write a short day-by-day plan. Put the cost in rupees next to EVERY item "
                 "(travel, stay, food, tickets), like '- Hawa Mahal entry: ₹200'.",
)


def check_budget(plan):
    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content":
                   f"You check trip budgets. Always reply in English. Add up every cost in the plan. The budget is ₹{BUDGET}. "
                   'Reply in JSON: {"total": number, "within_budget": true/false, "advice": "what to cut"}'},
                  {"role": "user", "content": plan}],
    )
    verdict = json.loads(response.choices[0].message.content)
    mark = paint("✅ within budget", "green") if verdict.get("within_budget") else paint("❌ over budget", "red")
    print(f"   💰 Budget Checker: ₹{verdict.get('total')} {mark} — {verdict.get('advice', '')}")
    return verdict


request = " ".join(sys.argv[1:]) or f"A 3-day trip to Jaipur for 2 college students. Budget ₹{BUDGET}."
plan = planner.run(request)

for _ in range(3):
    verdict = check_budget(plan)
    if verdict.get("within_budget"):
        break
    plan = planner.run(f"Your plan costs ₹{verdict.get('total')}, over the ₹{BUDGET} budget. "
                       f"Advice: {verdict.get('advice')}. Rewrite the full plan with costs.")

print(paint("\n═════════ FINAL PLAN ═════════\n", "bold") + plan)
