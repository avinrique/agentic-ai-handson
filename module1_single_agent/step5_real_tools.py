# STEP 5 — Real hands + guardrails
# Now the agent can create files and RUN code. That's powerful — and risky.
# So we add the three guardrails every real agent needs (see toolbox.py):
#   1. Sandbox   — it can only touch files in ./workspace
#   2. Approval  — a human says y/N before any file is written or run
#   3. Limits    — max steps, and a 20-second timeout on running code
# Plus: when a tool FAILS, we send the error back instead of crashing.
# The agent reads the error and fixes its own mistake. Watch for it.
import json
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from llm import client, MODEL, paint, short
from toolbox import list_files, read_file, write_file, run_python


def schema(name, description, **params):
    """Tiny helper so the menu is less typing. Every param is a string here."""
    return {"type": "function", "function": {
        "name": name, "description": description,
        "parameters": {"type": "object",
                       "properties": {p: {"type": "string", "description": d} for p, d in params.items()},
                       "required": list(params)}}}


TOOLS = {"list_files": list_files, "read_file": read_file, "write_file": write_file, "run_python": run_python}
MENU = [
    schema("list_files", "List files in the workspace."),
    schema("read_file", "Read a file from the workspace.", filename="e.g. notes.txt"),
    schema("write_file", "Create or overwrite a file in the workspace.",
           filename="e.g. primes.py", content="the full file content"),
    schema("run_python", "Run a Python file from the workspace and see its output.", filename="e.g. primes.py"),
]

task = " ".join(sys.argv[1:]) or ("Write a Python script that prints the first 15 prime numbers, "
                                  "run it, and tell me the output.")
messages = [
    {"role": "system", "content": "You are a coding agent working in a workspace folder. "
                                  "Write code to files, run it, read errors and fix them. "
                                  "Always run your code to check it before you say you're done."},
    {"role": "user", "content": task},
]
print(paint("You: ", "green") + task)

for step in range(1, 13):
    message = client.chat.completions.create(model=MODEL, messages=messages, tools=MENU).choices[0].message
    messages.append(message.model_dump(exclude_none=True))
    if not message.tool_calls:
        print(paint("\nAI: ", "cyan") + message.content)
        break

    for call in message.tool_calls:
        print(paint(f"\n[step {step}] 🔧 {call.function.name}({short(call.function.arguments, 120)})", "yellow"))
        try:
            result = TOOLS[call.function.name](**json.loads(call.function.arguments or "{}"))
        except Exception as error:               # a broken tool call must not crash the agent…
            result = f"Error: {error}"           # …the model reads the error and tries again
        print(paint(f"          ↳ {short(result, 200)}", "gray"))
        messages.append({"role": "tool", "tool_call_id": call.id, "content": str(result)})
else:
    print(paint("Stopped: hit the step limit.", "red"))

# 🧪 TRY IT:
#   "Make a file quiz.py with 3 multiple-choice questions about space and run it with the answers printed"
#   "Read ../llm.py"  → watch guardrail #1 block it
#   Answer 'n' at the approval prompt → watch the agent adapt
