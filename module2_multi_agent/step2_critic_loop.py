# STEP 2 — Writer ↔ Critic (reflection loop)
#
#   Writer ─► draft ─► Critic ─► approved? ── yes ──► done
#     ▲                              │ no
#     └───────── feedback ◄──────────┘
#
# One agent grading ANOTHER agent's work catches mistakes a single agent misses.
# The trick: the critic answers in JSON, so our code can read the verdict.
import json
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from module1_single_agent.agent import Agent
from llm import client, MODEL, paint

writer = Agent(
    "Writer", color="magenta", memory=True,  # memory: it remembers its drafts + the feedback
    instructions="You write short product taglines and fix them based on feedback. "
                 "Reply with ONLY the tagline.",
)

CRITIC_RULES = """You are a strict marketing critic. Judge the tagline against these rules:
1. At most 8 words
2. Mentions a concrete benefit to the customer
3. No clichés like "revolutionary", "game-changer", "next level"
Reply in JSON: {"approved": true/false, "feedback": "what to fix, one sentence"}"""


def critique(tagline):
    """The critic is a single LLM call with JSON output — not every agent needs tools."""
    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},  # forces valid JSON back
        messages=[{"role": "system", "content": CRITIC_RULES},
                  {"role": "user", "content": f"Tagline: {tagline}"}],
    )
    verdict = json.loads(response.choices[0].message.content)
    mark = paint("✅ APPROVED", "green") if verdict.get("approved") else paint("❌ REJECTED", "red")
    print(f"   🧐 Critic: {mark} — {verdict.get('feedback', '')}")
    return verdict


product = " ".join(sys.argv[1:]) or "a water bottle that reminds you to drink every hour"
tagline = writer.run(f"Write a tagline for: {product}")

for round_number in range(1, 4):  # max 3 rounds — loops between agents need a brake too
    verdict = critique(tagline)
    if verdict.get("approved"):
        break
    tagline = writer.run(f"The critic rejected it. Feedback: {verdict.get('feedback')}. Try again.")

print(paint("\n═════════ FINAL TAGLINE ═════════\n", "bold") + tagline)

# 🧪 TRY IT: make the critic stricter (add rule 4: "must rhyme") and watch the rounds go up.
