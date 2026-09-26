# STEP 3 — Give the model ONE tool
# The model does NOT run code. It writes an "order slip" (a tool call) saying
# which function it wants and with what arguments. OUR code runs it.
import json
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from llm import client, MODEL, paint
from toolbox import calculate  # a normal Python function — open toolbox.py and look!

# The MENU: describes the tool to the model. The description is how it
# decides WHEN to use it — write it like you're briefing a new intern.
tools = [{
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Evaluate a math expression. Use this for ANY arithmetic.",
        "parameters": {
            "type": "object",
            "properties": {"expression": {"type": "string", "description": "e.g. '48213 * 9217'"}},
            "required": ["expression"],
        },
    },
}]

question = " ".join(sys.argv[1:]) or "What is 48213 * 9217?"
messages = [{"role": "user", "content": question}]
print(paint("You: ", "green") + question)

# --- Call 1: send the question + the menu ---
message = client.chat.completions.create(model=MODEL, messages=messages, tools=tools).choices[0].message

if not message.tool_calls:
    print(paint("AI (no tool needed): ", "cyan") + message.content)
    sys.exit()

call = message.tool_calls[0]
print(paint("\n📝 The model wrote an order slip:", "yellow"))
print(paint(f"   function:  {call.function.name}\n   arguments: {call.function.arguments}", "yellow"))

# --- WE run the real function ---
args = json.loads(call.function.arguments)
result = calculate(**args)
print(paint(f"\n🔧 Our Python ran it → {result}", "magenta"))

# --- Call 2: hand the result back so the model can answer ---
messages.append(message.model_dump(exclude_none=True))
messages.append({"role": "tool", "tool_call_id": call.id, "content": str(result)})
final = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
print(paint("\nAI: ", "cyan") + final.choices[0].message.content)

# 🧪 TRY IT: ask "What is the capital of France?" — it skips the tool. IT decides.
