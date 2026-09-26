# STEP 1 — Talk to the model
# An LLM is a function: text in → text out. No memory. No hands. That's it.
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))  # lets us import llm.py
from llm import client, MODEL

question = " ".join(sys.argv[1:]) or "In two sentences: what is an AI agent?"

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a friendly tutor. Keep answers short."},
        {"role": "user", "content": question},
    ],
)

print(response.choices[0].message.content)

# 🧪 TRY IT — these show what the model CAN'T do on its own:
#   python module1_single_agent/step1_talk.py "What is today's date?"
#   python module1_single_agent/step1_talk.py "What is 48213 * 9217?"
# It guesses. Confidently. Agents fix this by giving the model TOOLS.
