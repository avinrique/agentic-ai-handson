# STEP 3 — The router (triage + handoff)
#
#                  ┌─► Math Tutor      (has calculate)
#   question ─► Router ─► History Buff   (has wiki_search)
#                  └─► Code Helper     (has write_file + run_python)
#
# A receptionist doesn't answer your question — they send you to the right expert.
# Each specialist gets ONLY the tools it needs. Fewer tools = fewer wrong choices.
import json
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from module1_single_agent.agent import Agent
from toolbox import calculate, wiki_search, write_file, run_python
from llm import client, MODEL, paint

specialists = {
    "math": Agent("Math Tutor", color="blue", tools=[calculate],
                  instructions="Solve step by step. Use calculate for every calculation."),
    "history": Agent("History Buff", color="magenta", tools=[wiki_search],
                     instructions="Answer history questions with facts from wiki_search. Be brief."),
    "code": Agent("Code Helper", color="green", tools=[write_file, run_python],
                  instructions="ALWAYS save the code with write_file and run it with run_python "
                                "before answering. Then show the code and explain it briefly."),
}


def route(question):
    """The router is one cheap JSON call. It never answers — it only picks."""
    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content":
                   'Pick the best expert for the question: "math", "history" or "code". '
                   'Reply in JSON: {"expert": "...", "reason": "a few words"}'},
                  {"role": "user", "content": question}],
    )
    choice = json.loads(response.choices[0].message.content)
    expert = choice.get("expert") if choice.get("expert") in specialists else "history"
    print(paint(f"   🧭 Router → {specialists[expert].name} ({choice.get('reason', '')})", "yellow"))
    return specialists[expert]


print(paint("Ask anything (math, history, or code). Type 'quit' to stop.", "gray"))
while True:
    question = input(paint("\nYou: ", "green"))
    if question.strip().lower() in {"quit", "exit"}:
        break
    route(question).run(question)

# 🧪 TRY IT: "What is 17% of 2340?"  /  "Who was Ashoka?"  /  "Write code to reverse a string"
#           Then add a 4th specialist — "science" — and teach the router about it.
