# Facilitator Guide — Live Demo Run-of-Show

**Length:** ~3 hours (Module 1 ≈ 80 min, break, Module 2 ≈ 90 min). You can split it into two sessions at the break.
**Format:** you run each step live on the projector → students run the same file → a lab at the end of each module.

## Before the session (the day before)

- [ ] `python check_setup.py` passes on **your** laptop, using the provider you'll demo with
- [ ] Use a **cloud model** (gpt-4o-mini or better) for the live demo. Local 7B models work, but
      they make math slips, forget tools, and sometimes write tool calls as plain text
- [ ] Run every step once. Clear `workspace/` afterwards
- [ ] Terminal font ≥ 18pt, dark theme; the colours (yellow = tool call, grey = result) carry the story
- [ ] Share the folder with students (zip / GitHub) + ask them to run `check_setup.py` **before** class
- [ ] Have a fallback key or Ollama ready for students whose setup fails. Pair them up, don't debug live

## Run-of-show

| Time | What you run | What to say (the one line that matters) |
|---|---|---|
| 0:00 | *(slides/whiteboard)* | "Today you build an agent with no framework. Just a loop you'll write yourself." |
| 0:05 | `step1_talk.py` then `"What is 48213 * 9217?"` | "Check it on a calculator. It's confident, and it's wrong. It has no hands." |
| 0:15 | `step2_memory.py` | Tell it your name, ask it back. "Memory is just a Python list we re-send." |
| 0:25 | `step3_first_tool.py` | Pause on the yellow **order slip**. "The model didn't run anything. **We** did." |
| 0:35 | `step4_agent_loop.py` ⭐ | Count steps out loud. "Nobody told it the plan. **This loop is an agent.**" Draw the THINK→ACT→OBSERVE loop on the board |
| 0:50 | `step5_real_tools.py` | Answer **n** once at the approval prompt. "The model decides. **Your code holds the power.**" |
| 1:00 | `agent.py` | "Everything we did is now one class. A new agent takes 5 lines." Show `tool_schema` → no more JSON |
| 1:05 | **Lab 1** (20 min) | Walk around. Common bug: forgetting the docstring |
| 1:25 | ☕ **Break** | |
| 1:35 | *(board)* the 4 shapes | Pipeline · Reflection · Router · Orchestrator |
| 1:40 | `m2 step1_pipeline.py "Chandrayaan-3"` | "Three small agents beat one big prompt, and you can see who broke what." |
| 1:50 | `m2 step2_critic_loop.py` | "The critic speaks JSON, so our code can read the verdict." |
| 2:00 | `m2 step3_router.py` | Take topics from the audience. "Fewer tools per agent = fewer wrong choices." |
| 2:10 | `m2 step4_orchestrator.py` ⭐ | Point at `as_tool`. "An agent is a tool for another agent. Now the **model** picks who works." |
| 2:20 | `m2 step5_dev_team.py` 🚀 | Open `workspace/` after. "Don't trust the agent's 'done'. Our code runs the tests." |
| 2:35 | **Lab 2** (30 min) | |
| 3:05 | README → "After this course" table | "LangGraph, CrewAI, OpenAI Agents SDK are all the loop you just wrote." |

## Live-coding moves that land well

- **Break it on purpose.** In step 4, remove `get_current_time` from the menu and ask
  *"How many years ago was the Eiffel Tower built?"* It guesses the year. Put the tool back and it checks.
- **Bad description.** In step 3, change the description to `"does stuff"`. It stops using the tool reliably.
  "The description is a prompt."
- **Remove the brake.** Set `MAX_STEPS = 1` in step 4. It stops mid-task. "Every loop needs an exit."
- **Audience-driven.** Let students shout questions into step 4 and topics into step 1.

## When things go wrong live (they will; use it)

| Symptom | What's happening | Say |
|---|---|---|
| Final answer has wrong math even with the calculator | model wrote the wrong *expression* | "Tools give correct results for the wrong question too. This is why we verify." |
| Output shows `{"name": "wiki_search", ...}` as text | small model wrote the call as text instead of making it | "Smaller models are worse at tool use. Model choice matters." |
| Agent says "Done! I marked it" but no 🔧 line | it claimed an action it didn't take | "Never trust an agent's word. Check the tool log." (Lab 1 hint) |
| Capstone ends "still failing" | the test or the code is wrong | "That's why a human stays in the loop." Open both files together |
| `No API key found` | `.env` missing | `cp .env.example .env` and fill it in |
| `wiki_search` errors | no internet / proxy | Everything else still works. Skip to the math questions |

## Rehearsed-demo mode

`AUTO_APPROVE=1 python module1_single_agent/step5_real_tools.py` skips the y/N prompts.
Keep the prompts ON for the first demo, since the audience needs to see the human gate.
