# Run this FIRST:  python check_setup.py
# It checks that Python, the openai package, your .env and the model all work.
import sys

print("1. Python version ...", sys.version.split()[0], "✅" if sys.version_info >= (3, 9) else "❌ need 3.9+")
try:
    import openai
    print("2. openai package ...", openai.__version__, "✅")
except ImportError:
    sys.exit("2. openai package ... ❌  run: pip install -r requirements.txt")

from llm import client, MODEL, PROVIDER
print(f"3. Provider/model ... {PROVIDER} / {MODEL}")

try:
    reply = client.chat.completions.create(
        model=MODEL, messages=[{"role": "user", "content": "Say 'ready' and nothing else."}]
    ).choices[0].message.content
    print("4. Model replied  ...", reply.strip(), "✅")
except Exception as error:
    sys.exit(f"4. Model call     ... ❌  {error}")

try:
    from toolbox import wiki_search
    wiki_search("Python programming language")
    print("5. Internet tools ... ✅")
except Exception as error:
    print(f"5. Internet tools ... ⚠️  {error} (wiki_search won't work, everything else will)")

print("\nAll set. Start with:  python module1_single_agent/step1_talk.py")
