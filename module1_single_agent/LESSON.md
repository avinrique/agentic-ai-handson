# Module 1 — Build ONE Agent From Scratch

**By the end:** you'll have written a ~70-line `Agent` class that can search the web, do math,
write files and run code, with guardrails so it can't wreck your laptop.

---

## Step 1 · Talk to the model — `step1_talk.py`

An LLM is a function: **text in → text out.** You send a list of messages, it sends back one message.

```python
client.chat.completions.create(model=MODEL, messages=[
    {"role": "system", "content": "You are a friendly tutor."},   # how to behave
    {"role": "user",   "content": "What is an AI agent?"},       # what you ask
])
```

🧪 **Try:** `python module1_single_agent/step1_talk.py "What is 48213 * 9217?"`
Check the answer on a calculator. Then ask it today's date.

> **Takeaway:** the model is smart but has **no hands**. It can't look anything up, can't
> calculate reliably, and doesn't know what day it is. It just guesses, confidently.

---

## Step 2 · Memory is just a list — `step2_memory.py`

The model remembers **nothing** between calls. A chatbot "remembers" because we re-send the
whole conversation every time:

```python
messages.append({"role": "user", "content": user})         # what you said
reply = ...create(messages=messages)                         # send EVERYTHING
messages.append({"role": "assistant", "content": reply})    # what it said
```

🧪 **Try:** tell it your name, then ask for it. Then delete the second `append` and try again.

> **Takeaway:** memory = the `messages` list. Longer chat → more tokens sent → slower and pricier.

---

## Step 3 · The first tool — `step3_first_tool.py`

We give the model a **menu** (a JSON description of a function). The model doesn't run anything.
It writes an **order slip**:

```
function:  calculate
arguments: {"expression": "48213 * 9217"}
```

**Our code** runs the real Python function and sends the result back. Then the model answers.

```
You ──question + menu──► Model ──order slip──► YOUR CODE runs calculate()
                                                        │
You ◄──── final answer ──── Model ◄──── result ─────────┘
```

🧪 **Try:** ask "What is the capital of France?" It **doesn't** use the tool. The model decides.

> **Takeaway:** the `description` in the menu is how the model knows **when** to use a tool.
> Write it like you're briefing a new intern.

---

## Step 4 · THE AGENT LOOP ⭐ — `step4_agent_loop.py`

This is the whole course in one file. Step 3 did **one** tool call. Real questions need several,
and we don't know in advance how many. So we loop:

```
     ┌─────────► THINK   (model reads everything so far)
     │              │
     │        wants a tool? ── no ──► ANSWER, stop
     │              │ yes
     │            ACT     (our code runs the tool)
     │              │
     └──────── OBSERVE    (result goes back into messages)
```

```python
for step in range(MAX_STEPS):                  # a safety brake. ALWAYS have one
    message = create(messages, tools=MENU)     # THINK
    if not message.tool_calls: break           # done
    for call in message.tool_calls:
        result = TOOLS[call.function.name](**args)   # ACT
        messages.append({"role": "tool", ...})       # OBSERVE
```

🧪 **Try:** `"How many years older is the Taj Mahal than the Eiffel Tower?"`
Count the steps. Nobody told it to search twice and then calculate. **It planned that itself.**

> **Takeaway:** chatbot = one call. **Agent = a loop where the model picks the next step.**

---

## Step 5 · Real hands + guardrails — `step5_real_tools.py`

Now it can **write files and run code**. Powerful and risky, so we add the guardrails every real
agent needs (they're in `toolbox.py`):

| Guardrail | How | Why |
|---|---|---|
| Sandbox | files only inside `./workspace` | it can't touch your real files |
| Human approval | `y/N` prompt before writing/running | you stay in control |
| Limits | max steps + 20 s timeout | no infinite loops, no runaway code |
| Errors → model | `except` sends the error back as the tool result | it **fixes its own mistakes** |

🧪 **Try:** answer **n** at an approval prompt and watch the agent adapt. Ask it to
`"read ../llm.py"` and watch the sandbox block it.

> **Takeaway:** the model decides, **your code** holds the power. Every agent you build
> should have these four guardrails.

---

## Step 6 · Package it — `agent.py`

Steps 3–5 repeated the same loop by hand. `agent.py` writes it **once**:

```python
researcher = Agent(
    name="Researcher",
    instructions="Answer with facts. Never guess — use your tools.",
    tools=[wiki_search, calculate, get_current_time],
)
researcher.run("How tall is Mount Everest in feet?")
```

Two upgrades:
- **`tool_schema(fn)`** builds the JSON menu automatically from the function's name, type hints
  and docstring. No more hand-written JSON.
- **`as_tool()`** turns a whole agent into a tool for another agent. Module 2 is built on this.

---

## 🛠 Lab 1 — Your own To-Do agent (`lab_todo_agent.py`, ~20 min)

Write 3 tools (`add_task`, `list_tasks`, `complete_task`) and give them to an `Agent`.
Then chat: *"add buy milk and call mom"* → *"I bought the milk"* → *"what's left?"*

**Checklist**
- [ ] Each tool has a docstring (that's its description on the menu)
- [ ] `complete_task` returns an **error string** for a bad number instead of crashing
- [ ] `memory=True` so it remembers the conversation
- [ ] ⭐ Bonus: `delete_task`, then *"delete everything I've finished"*

Answer: `solutions/lab_todo_agent.py`
