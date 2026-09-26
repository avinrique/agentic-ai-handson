"""
llm.py — ONE place to configure the model. Every lesson imports from here.

Pick a provider in the .env file (copy .env.example → .env):

  OpenAI (default)      LLM_PROVIDER=openai   OPENAI_API_KEY=sk-...
  Ollama (free, local)  LLM_PROVIDER=ollama   (run `ollama pull qwen2.5` first)
  Any OpenAI-compatible LLM_BASE_URL=...  LLM_API_KEY=...  LLM_MODEL=...
  (Groq, Gemini, OpenRouter, LM Studio all speak this same API)
"""
import os
import pathlib
import sys

from openai import OpenAI

ROOT = pathlib.Path(__file__).resolve().parent


def _load_dotenv():
    """Tiny .env reader so students don't need an extra package."""
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

if PROVIDER == "ollama":
    client = OpenAI(
        base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
        api_key="ollama",  # Ollama ignores it, but the SDK wants something
    )
    MODEL = os.getenv("LLM_MODEL", "qwen2.5")
else:
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.exit("No API key found. Copy .env.example to .env and fill it in "
                 "(or set LLM_PROVIDER=ollama to run a free local model).")
    client = OpenAI(base_url=os.getenv("LLM_BASE_URL") or None, api_key=api_key)
    MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")


# --- Pretty terminal output, so the audience can SEE what the agent is doing ---
COLORS = {
    "red": 31, "green": 32, "yellow": 33, "blue": 34,
    "magenta": 35, "cyan": 36, "gray": 90, "bold": 1,
}


def paint(text, color):
    return f"\033[{COLORS[color]}m{text}\033[0m"


def short(text, limit=300):
    text = str(text).replace("\n", " ")
    return text if len(text) <= limit else text[:limit] + " …"
