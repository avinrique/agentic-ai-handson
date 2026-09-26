# Module 2 — Multi-Agent Systems

**Why more than one agent?** Same reason a company isn't one person:

- **Focus.** A short, specific prompt beats one giant "do everything" prompt.
- **Fewer tools each.** An agent with 3 tools picks right more often than one with 30.
- **Checks and balances.** One agent reviewing another catches mistakes.
- **Debuggable.** When it breaks, you can see *which* agent broke it.

There are only **four shapes** you need to know. Everything else is a mix of them.

```
1. PIPELINE        A ─► B ─► C                  your code fixes the order
2. REFLECTION      A ⇄ Critic                    loop until it's good
3. ROUTER          Router ─► A | B | C           pick the right expert
4. ORCHESTRATOR    Boss ─► (A, B, …) as tools    the MODEL decides who works
```

Every agent here is the `Agent` class from module 1. Nothing new under the hood.

---

## Step 1 · Pipeline — `step1_pipeline.py`

```
topic ─► Researcher (wiki_search) ─► Writer ─► Editor ─► LinkedIn post
```

Each agent's output becomes the next one's input: `facts = researcher.run(...)`,
`draft = writer.run(facts)`, `final = editor.run(draft)`. That's it.

🧪 **Try:** `python module2_multi_agent/step1_pipeline.py "ISRO's Chandrayaan-3"`
Then add a 4th agent, a Translator. It takes 4 lines.

> **Use when:** the steps are always the same, in the same order.

---

## Step 2 · Reflection (Writer ⇄ Critic) — `step2_critic_loop.py`

```
Writer ─► draft ─► Critic ─► approved? ─ yes ─► done
  ▲                              │ no
  └────────── feedback ◄─────────┘        (max 3 rounds)
```

New trick: the critic replies in **JSON** (`response_format={"type": "json_object"}`) so
**our code** can read `verdict["approved"]` and decide whether to loop.

🧪 **Try:** add a rule to `CRITIC_RULES` ("must rhyme") and watch the rounds go up.

> **Use when:** quality matters and "good" can be written down as rules.

---

## Step 3 · Router — `step3_router.py`

```
             ┌─► Math Tutor    (calculate)
question ─► Router ─► History Buff  (wiki_search)
             └─► Code Helper   (write_file, run_python)
```

The router is one cheap JSON call. It **never answers**, it only picks. Each specialist gets
only the tools it needs.

🧪 **Try:** *"What is 17% of 2340?"* · *"Who was Ashoka?"* · *"Write code to reverse a string"*.
Then add a "science" specialist.

> **Use when:** questions come in different kinds (customer support, helpdesks, tutors).

---

## Step 4 · Orchestrator (boss + workers) — `step4_orchestrator.py`

```python
manager = Agent("Manager", tools=[
    researcher.as_tool("Ask the Researcher to look up facts."),
    analyst.as_tool("Ask the Analyst to do math."),
])
```

**Agents are tools for other agents.** The manager's loop is the same agent loop from
module 1. Its "tools" just happen to be whole agents. Now the **model** decides who works,
in what order, and how many times.

| | Pipeline (step 1) | Orchestrator (step 4) |
|---|---|---|
| Who decides the order? | your code | the model |
| Predictable? | very | less |
| Handles surprises? | no | yes |

🧪 **Try:** add a Writer worker and tell the manager to finish with a tweet.

> **Use when:** you can't know the steps in advance.

---

## Step 5 · CAPSTONE: a dev team — `step5_dev_team.py`

```
request ─► Planner ─► spec ─► Coder ─► solution.py
                                ▲          │
                                │     Tester writes test_solution.py
                                │          │
                                └─ fail ◄─ OUR CODE runs the tests ─► pass ─► 🚀
```

It uses everything: pipeline + feedback loop + real tools + sandbox. Plus two new rules for real systems:

1. **Don't trust, verify.** Agents say "done!" when they aren't. Our code runs the tests
   itself and believes the **exit code**, not the agent.
2. **Send feedback to whoever can fix it.** Missing test file → Tester. Tests never ran →
   Tester. An assert failed → Coder. Blaming the wrong agent makes it loop forever.

🧪 **Try:** `python module2_multi_agent/step5_dev_team.py "A function that converts Roman numerals to integers"`
Open `workspace/` afterwards and read what the team wrote.

---

## 🛠 Lab 2 — Trip-planning team (`lab_trip_team.py`, ~30 min)

```
request ─► Planner ─► itinerary ─► Budget Checker ─► over? ─ yes ─► back to Planner
```

A pipeline plus a reflection loop: a Planner agent (with `wiki_search`) and a JSON Budget Checker.

**Checklist**
- [ ] Planner lists a ₹ cost for **every** item (otherwise the checker can't add it up)
- [ ] Budget checker returns `{"total", "within_budget", "advice"}`
- [ ] Loop stops when within budget **or** after 3 rounds
- [ ] ⭐ Bonus: make the checker an `Agent` with the `calculate` tool. Is the total more accurate?

Answer: `solutions/lab_trip_team.py`

---

## Cheat sheet: which shape do I need?

| Your problem | Shape |
|---|---|
| Same steps every time | Pipeline |
| Output must meet a quality bar | Reflection |
| Different kinds of requests | Router |
| Steps unknown until you start | Orchestrator |
| Real software (it has to *actually* work) | Pipeline + Reflection + **verification in code** |
