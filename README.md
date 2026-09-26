# Build AI Agents From Scratch — Hands-On

> From "call an LLM" to "a team of agents that plans, codes and tests" in plain Python.
> No LangChain, no CrewAI, no magic. Every line is yours, so you understand what those frameworks do.

```
Module 1: ONE agent                            Module 2: MANY agents
────────────────────────                       ──────────────────────────────
1  talk to the model                           1  assembly line   (pipeline)
2  memory = a list                             2  writer ↔ critic (reflection)
3  the first tool                              3  router          (triage/handoff)
4  THE AGENT LOOP  ⭐                          4  boss + workers  (orchestrator)
5  real tools + guardrails                     5  CAPSTONE: a dev team that ships code
6  package it → Agent class ─────────────────► used by everything in module 2
🛠 Lab 1: your own To-Do agent                 🛠 Lab 2: a trip-planning team
```

## Setup (5 minutes)

```bash
cd agentic-ai-handson
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # then open .env and add your key
python check_setup.py              # should end with "All set"
```

**No API key?** Install [Ollama](https://ollama.com), run `ollama pull qwen2.5`, and put
`LLM_PROVIDER=ollama` in `.env`. It's free and runs on your laptop. It's slower, and small
models make more mistakes, so read every step's output. Spotting those mistakes teaches you a lot.

Run everything **from this folder** (the course root):

```bash
python module1_single_agent/step1_talk.py
python module1_single_agent/step4_agent_loop.py "your own question here"
```

## What's in here

| File | What it is |
|---|---|
| `llm.py` | One place that configures the model (OpenAI / Ollama / any compatible API) |
| `toolbox.py` | The tools (the agent's "hands"): calculator, clock, Wikipedia, sandboxed file + code tools |
| `check_setup.py` | Verifies your setup before class |
| `module1_single_agent/` | Build one agent, step by step. [LESSON.md](module1_single_agent/LESSON.md) |
| `module2_multi_agent/` | Combine agents into teams. [LESSON.md](module2_multi_agent/LESSON.md) |
| `*/lab_*.py` | Hands-on exercises with TODOs. Answers are in `*/solutions/` |
| `workspace/` | The only folder agents are allowed to write files and run code in |
| `FACILITATOR.md` | For the instructor: run-of-show, what to type live, what to say, what can go wrong |

## The one idea to remember

```
An agent is an LLM in a loop, with tools, deciding its own next step.

    while not done:
        think   → the model reads everything so far
        act     → if it asked for a tool, your code runs it
        observe → the result is added to the conversation
```

Multi-agent systems are **several of those loops, each with a small job**, wired together by
your code (pipeline, critic loop, router) or by another agent (orchestrator).

## After this course

You've now built the core of every agent framework yourself. When you pick one up, you'll recognise the pieces:

| Framework | What you'll recognise |
|---|---|
| OpenAI Agents SDK | `Agent(name, instructions, tools)` + handoffs = your step 6 + router |
| Claude Agent SDK | the agent loop + file/shell tools + permission prompts = your step 5 |
| LangGraph | your multi-agent flows, drawn as a graph with state |
| CrewAI | roles + tasks + a manager = your step 4 orchestrator |
