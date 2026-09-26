# 🛠  LAB 1 — Build your own To-Do agent  (≈20 min)
#
# Goal: an agent you can chat with in plain English:
#     "add buy milk and call mom"   "what's left?"   "I bought the milk"
# It manages a real Python list using tools YOU write.
#
# Fill in the 4 TODOs. Run:  python module1_single_agent/lab_todo_agent.py
# Stuck? The answer is in solutions/lab_todo_agent.py — try for 10 minutes first!
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from module1_single_agent.agent import Agent
from llm import paint

tasks = []  # each task: {"title": "buy milk", "done": False}


def add_task(title: str):
    """Add a new task to the to-do list."""
    # TODO 1: append a dict to `tasks` and return a short confirmation string
    ...


def list_tasks():
    """Show every task with its number and whether it is done."""
    # TODO 2: return a string like "1. [ ] buy milk\n2. [x] call mom"
    #         (return "No tasks yet." if the list is empty)
    ...


# TODO 3: write a complete_task(number: int) tool.
#   - Give it a docstring (the model reads it — it's the tool's description!)
#   - Mark tasks[number - 1] as done; return an error string if the number is wrong


# TODO 4: create the agent. Give it a name, instructions, and your 3 tools.
#   Hint: memory=True so it remembers the conversation.
#   Hint: small models sometimes SAY "done!" without calling a tool. Tell it:
#         "Never say you changed the list unless you actually called the tool."
todo_agent = None

print(paint("Talk to your to-do agent. Type 'quit' to stop.", "gray"))
while True:
    text = input(paint("\nYou: ", "green"))
    if text.strip().lower() in {"quit", "exit"}:
        break
    todo_agent.run(text)

# ⭐ BONUS: add a delete_task tool. Then try: "delete everything I've finished".
