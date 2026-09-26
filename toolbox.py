"""
toolbox.py — the "hands" we give our agents.

A tool is just a normal Python function. The model never runs it —
the model only ASKS for it, and our code decides whether to run it.

Two kinds of tools live here:
  1. Read-only tools  (calculate, get_current_time, wiki_search)  → always safe
  2. Action tools     (write_file, run_python)                    → can change things,
     so they are locked inside ./workspace and can ask a human first.
"""
import ast
import datetime
import json
import operator
import os
import pathlib
import subprocess
import sys
import urllib.parse
import urllib.request

from llm import ROOT, paint

# ---------------------------------------------------------------------------
# 1. Read-only tools
# ---------------------------------------------------------------------------

_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod, ast.Pow: operator.pow, ast.USub: operator.neg,
}


def calculate(expression: str):
    """Evaluate a math expression like '48213 * 9217' or '(3 + 4) ** 2'. Use this for ANY arithmetic."""
    def ev(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.operand))
        raise ValueError("only numbers and + - * / // % ** are allowed")
    # Safe on purpose: we parse the math ourselves instead of calling eval()
    return ev(ast.parse(expression, mode="eval").body)


def get_current_time():
    """Get today's date and the current local time."""
    return datetime.datetime.now().strftime("%A %d %B %Y, %H:%M")


def wiki_search(query: str):
    """Look up a person, place or thing on Wikipedia (e.g. 'Eiffel Tower') and return a short summary."""
    headers = {"User-Agent": "agentic-ai-handson-course/1.0"}
    search_url = ("https://en.wikipedia.org/w/api.php?action=query&list=search&srlimit=1&format=json&srsearch="
                  + urllib.parse.quote(query))
    with urllib.request.urlopen(urllib.request.Request(search_url, headers=headers), timeout=10) as r:
        hits = json.load(r)["query"]["search"]
    if not hits:
        return f"No Wikipedia page found for '{query}'. Try a shorter query, like just the name."
    summary_url = ("https://en.wikipedia.org/api/rest_v1/page/summary/"
                   + urllib.parse.quote(hits[0]["title"].replace(" ", "_")))
    with urllib.request.urlopen(urllib.request.Request(summary_url, headers=headers), timeout=10) as r:
        page = json.load(r)
    return f"{page['title']}: {page.get('extract', '(no summary)')}"


# ---------------------------------------------------------------------------
# 2. Action tools — sandboxed to ./workspace, with a human approval gate
# ---------------------------------------------------------------------------

WORKSPACE = ROOT / "workspace"
WORKSPACE.mkdir(exist_ok=True)

# Set AUTO_APPROVE=1 to skip the y/N prompts (handy for a rehearsed demo)
AUTO_APPROVE = os.getenv("AUTO_APPROVE") == "1"


def _safe_path(filename):
    """Guardrail #1: the agent can only touch files inside ./workspace."""
    filename = filename.removeprefix("./").removeprefix("workspace/")  # models often add this prefix
    path = (WORKSPACE / filename).resolve()
    if WORKSPACE.resolve() not in path.parents:
        raise ValueError(f"'{filename}' is outside the workspace — not allowed")
    return path


def _approve(action):
    """Guardrail #2: a human says yes before anything changes."""
    if AUTO_APPROVE:
        return True
    answer = input(paint(f"   ✋ Agent wants to {action}. Allow? [y/N] ", "red"))
    return answer.strip().lower() == "y"


def list_files():
    """List the files in the workspace folder."""
    files = sorted(p.name for p in WORKSPACE.iterdir() if p.is_file())
    return "\n".join(files) or "(workspace is empty)"


def read_file(filename: str):
    """Read a text file from the workspace folder."""
    return _safe_path(filename).read_text()


def write_file(filename: str, content: str):
    """Create or overwrite a text file in the workspace folder."""
    path = _safe_path(filename)
    if not _approve(f"write {len(content)} chars to workspace/{filename}"):
        return "The human said NO. Do not write this file."
    path.write_text(content)
    return f"Wrote workspace/{filename}"


def run_python(filename: str):
    """Run a Python file from the workspace folder and return what it printed."""
    path = _safe_path(filename)
    if not _approve(f"run workspace/{filename}"):
        return "The human said NO. Do not run this file."
    try:
        result = subprocess.run([sys.executable, path.name], cwd=WORKSPACE,
                                capture_output=True, text=True, timeout=20)  # Guardrail #3: time limit
    except subprocess.TimeoutExpired:
        return "Error: the program ran longer than 20 seconds and was stopped."
    return (f"exit code {result.returncode}\n"
            f"--- output ---\n{result.stdout[-2000:]}\n--- errors ---\n{result.stderr[-2000:]}")
