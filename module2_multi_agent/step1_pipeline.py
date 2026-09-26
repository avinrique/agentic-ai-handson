# STEP 1 — The assembly line (sequential pipeline)
#
#   topic ─► Researcher ─► Writer ─► Editor ─► final post
#
# Why not one big agent? Same reason a newspaper has more than one person:
# a short, focused job → a short, focused prompt → better, easier-to-debug output.
# Here YOUR CODE decides the order. The agents just do their one job.
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from module1_single_agent.agent import Agent
from toolbox import wiki_search
from llm import paint

researcher = Agent(
    "Researcher", color="blue", tools=[wiki_search],
    instructions="Research the topic with wiki_search (1-3 searches). "
                 "Return 5 short bullet-point FACTS. No opinions, no intro.",
)
writer = Agent(
    "Writer", color="magenta",
    instructions="Write a 120-word LinkedIn post for college students using ONLY the facts given. "
                 "Hook in the first line. Friendly, clear, no hashtags spam (max 2).",
)
editor = Agent(
    "Editor", color="green",
    instructions="Edit the post: fix errors, cut fluff, keep it under 120 words. "
                 "Return ONLY the final post.",
)

topic = " ".join(sys.argv[1:]) or "the James Webb Space Telescope"

facts = researcher.run(f"Topic: {topic}")
draft = writer.run(f"Facts:\n{facts}")
final = editor.run(draft)

print(paint("\n═════════ FINAL POST ═════════\n", "bold") + final)

# 🧪 TRY IT: add a 4th agent — a "Translator" that turns the final post into Hindi.
#           How many lines did it take? That's the point of the Agent class.
