# STEP 4 — The agent loop  ⭐ the most important file in this course
#
#     ┌──────────► THINK  (model reads everything so far)
#     │              │
#     │        wants a tool? ── no ──► ANSWER, stop
#     │              │ yes
#     │            ACT    (our code runs the tool)
#     │              │
#     └──────── OBSERVE   (result goes back into the messages)
#
# That while-loop is the whole difference between a chatbot and an agent.
# WE don't decide the steps. The MODEL does.
import json
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from llm import client, MODEL, paint, short
from toolbox import calculate, get_current_time, wiki_search

# name → real function, so we can look tools up by the name the model uses
TOOLS = {"calculate": calculate, "get_current_time": get_current_time, "wiki_search": wiki_search}

MENU = [
    {"type": "function", "function": {
        "name": "calculate", "description": "Evaluate a math expression. Use for ANY arithmetic.",
        "parameters": {"type": "object", "properties": {"expression": {"type": "string"}},
                       "required": ["expression"]}}},
    {"type": "function", "function": {
        "name": "get_current_time", "description": "Get today's date and the current time.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "wiki_search", "description": "Look up a person, place or thing on Wikipedia (e.g. 'Eiffel Tower').",
        "parameters": {"type": "object", "properties": {"query": {"type": "string"}},
                       "required": ["query"]}}},
]

question = " ".join(sys.argv[1:]) or "How many years older is the Taj Mahal than the Eiffel Tower?"
messages = [
    {"role": "system", "content": "You are a careful research assistant. Never guess facts or math — "
                                  "use your tools. You do NOT know today's date: for anything about "
                                  "'now', 'today' or 'ago', call get_current_time. Answer briefly."},
    {"role": "user", "content": question},
]
print(paint("You: ", "green") + question)

MAX_STEPS = 8  # safety brake: an agent must ALWAYS have a way to stop
for step in range(1, MAX_STEPS + 1):
    # THINK
    message = client.chat.completions.create(model=MODEL, messages=messages, tools=MENU).choices[0].message
    messages.append(message.model_dump(exclude_none=True))

    if not message.tool_calls:  # no order slips → the model is done
        print(paint("\nAI: ", "cyan") + message.content)
        break

    for call in message.tool_calls:
        # ACT
        args = json.loads(call.function.arguments or "{}")
        print(paint(f"\n[step {step}] 🔧 {call.function.name}({args})", "yellow"))
        result = TOOLS[call.function.name](**args)
        # OBSERVE
        print(paint(f"          ↳ {short(result, 160)}", "gray"))
        messages.append({"role": "tool", "tool_call_id": call.id, "content": str(result)})
else:
    print(paint("Stopped: hit MAX_STEPS without a final answer.", "red"))

# 🧪 TRY IT:
#   "How many years ago was the Eiffel Tower completed?"
#      → big models call get_current_time; small local ones often assume a year.
#        Tools only help if the model is smart enough to reach for them.
#   "How old would Albert Einstein be today if he were alive?"
#   "What is the population of Japan divided by the population of Australia?"
# Count the steps. Nobody told it to search, then check the date, then calculate.
