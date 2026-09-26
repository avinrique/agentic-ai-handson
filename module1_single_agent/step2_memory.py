# STEP 2 — Memory is just a list
# The model forgets everything between calls. "Memory" = we re-send the whole
# conversation every single time. Watch the list grow.
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from llm import client, MODEL, paint

messages = [{"role": "system", "content": "You are a friendly tutor. Keep answers short."}]

print(paint("Chat with the model. Type 'quit' to stop.", "gray"))
while True:
    user = input(paint("\nYou: ", "green"))
    if user.strip().lower() in {"quit", "exit"}:
        break

    messages.append({"role": "user", "content": user})          # 1. add what you said
    response = client.chat.completions.create(model=MODEL, messages=messages)
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})    # 2. add what it said

    print(paint("AI: ", "cyan") + reply)
    print(paint(f"   (we just sent {len(messages) - 1} messages to get that reply)", "gray"))

# 🧪 TRY IT: say "My name is Priya", then ask "What's my name?"
# Then comment out line 2's append and try again — the memory is gone.
