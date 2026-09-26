# STEP 4 — The boss (orchestrator + workers)
#
#                 ┌── ask_researcher ──► Researcher (wiki_search)
#   request ─► Manager
#                 └── ask_analyst ─────► Analyst    (calculate)
#
# Big idea: an agent can be a TOOL for another agent (Agent.as_tool in module 1).
# Now the MODEL decides who works, in what order, and how many times.
# Compare with step 1, where OUR code fixed the order.
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from module1_single_agent.agent import Agent
from toolbox import wiki_search, calculate
from llm import paint

researcher = Agent("Researcher", color="blue", tools=[wiki_search],
                   instructions="Find the facts asked for with wiki_search. Reply with just the facts and numbers.")
analyst = Agent("Analyst", color="green", tools=[calculate],
                instructions="Do the calculation asked for with the calculate tool. Show the formula and result.")

manager = Agent(
    "Manager", color="magenta", max_steps=12,
    tools=[
        researcher.as_tool("Ask the Researcher to look up facts. Give it one clear question."),
        analyst.as_tool("Ask the Analyst to do math. Give it the numbers and what to compute."),
    ],
    instructions="You are a manager. Break the request into small tasks and delegate EVERY task to "
                 "your team — never look things up or calculate yourself. "
                 "When you have all the pieces, write the final answer.",
)

request = " ".join(sys.argv[1:]) or ("How tall is Mount Everest, and how many Burj Khalifas "
                                     "stacked on top of each other would it take to reach that height?")
answer = manager.run(request)
print(paint("\n═════════ FINAL ANSWER ═════════\n", "bold") + answer)

# 🧪 TRY IT: add a third worker — a "Writer" with no tools — and tell the manager
#           to have the Writer turn the answer into a tweet.
