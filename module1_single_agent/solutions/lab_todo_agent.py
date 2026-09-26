# ✅ LAB 1 — SOLUTION
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))
from module1_single_agent.agent import Agent
from llm import paint

tasks = []


def add_task(title: str):
    """Add a new task to the to-do list."""
    tasks.append({"title": title, "done": False})
    return f"Added task #{len(tasks)}: {title}"


def list_tasks():
    """Show every task with its number and whether it is done."""
    if not tasks:
        return "No tasks yet."
    return "\n".join(f"{i}. [{'x' if t['done'] else ' '}] {t['title']}" for i, t in enumerate(tasks, 1))


def complete_task(number: int):
    """Mark a task as done, using its number from list_tasks."""
    if not 1 <= number <= len(tasks):
        return f"Error: there is no task #{number}. Call list_tasks to see the numbers."
    tasks[number - 1]["done"] = True
    return f"Done: {tasks[number - 1]['title']}"


def delete_task(number: int):
    """Delete a task, using its number from list_tasks. Numbers shift after a delete."""
    if not 1 <= number <= len(tasks):
        return f"Error: there is no task #{number}."
    return f"Deleted: {tasks.pop(number - 1)['title']}"


todo_agent = Agent(
    "To-Do", memory=True, tools=[add_task, list_tasks, complete_task, delete_task],
    instructions="You manage the user's to-do list with your tools. If you need a task's number, "
                 "call list_tasks first. Split requests like 'add X and Y' into separate tasks. "
                 "Never say you changed the list unless you actually called the tool. "
                 "Reply in one short, friendly sentence.",
)

print(paint("Talk to your to-do agent. Type 'quit' to stop.", "gray"))
while True:
    text = input(paint("\nYou: ", "green"))
    if text.strip().lower() in {"quit", "exit"}:
        break
    todo_agent.run(text)
