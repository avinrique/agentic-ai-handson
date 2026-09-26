# STEP 6 — Package it: the Agent class
# Steps 3-5 repeated the same loop by hand. Here it is ONCE, in ~70 lines.
# An agent = a name + instructions (system prompt) + tools + the loop.
# Module 2 builds every multi-agent system out of this one class.
import inspect
import json
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from llm import client, MODEL, paint, short

PY_TO_JSON = {str: "string", int: "integer", float: "number", bool: "boolean"}


def tool_schema(fn):
    """Build the tool MENU entry from the function itself: its name, type hints and docstring.
    No more hand-writing JSON like in step 4."""
    params = inspect.signature(fn).parameters
    return {"type": "function", "function": {
        "name": fn.__name__,
        "description": inspect.getdoc(fn) or fn.__name__,
        "parameters": {
            "type": "object",
            "properties": {name: {"type": PY_TO_JSON.get(p.annotation, "string")} for name, p in params.items()},
            "required": [name for name, p in params.items() if p.default is inspect.Parameter.empty],
        },
    }}


class Agent:
    def __init__(self, name, instructions, tools=(), color="cyan", max_steps=10, memory=False):
        self.name = name
        self.instructions = instructions
        self.tools = {fn.__name__: fn for fn in tools}
        self.color = color
        self.max_steps = max_steps
        self.memory = memory  # False = every run() starts fresh; True = remembers past runs
        self.messages = []

    def run(self, task):
        if not self.memory or not self.messages:
            self.messages = [{"role": "system", "content": self.instructions}]
        self.messages.append({"role": "user", "content": task})
        print(paint(f"\n▶ {self.name}", self.color) + paint(f"  ← {short(task, 140)}", "gray"))

        menu = [tool_schema(fn) for fn in self.tools.values()]
        for _ in range(self.max_steps):
            request = {"model": MODEL, "messages": self.messages}
            if menu:
                request["tools"] = menu
            message = client.chat.completions.create(**request).choices[0].message   # THINK
            self.messages.append(message.model_dump(exclude_none=True))

            if not message.tool_calls:                                               # DONE
                print(paint(f"◀ {self.name}: ", self.color) + short(message.content, 400))
                return message.content

            for call in message.tool_calls:                                          # ACT
                result = self._use_tool(call)
                self.messages.append({"role": "tool", "tool_call_id": call.id,       # OBSERVE
                                      "content": str(result)})
        return f"({self.name} stopped: reached max_steps={self.max_steps})"

    def _use_tool(self, call):
        print(paint(f"   🔧 {self.name} → {call.function.name}({short(call.function.arguments, 120)})", "yellow"))
        fn = self.tools.get(call.function.name)
        try:
            if fn is None:
                raise ValueError(f"there is no tool called {call.function.name}")
            result = fn(**json.loads(call.function.arguments or "{}"))
        except Exception as error:
            result = f"Error: {error}"  # the model reads this and can fix its mistake
        print(paint(f"      ↳ {short(result, 160)}", "gray"))
        return result

    def as_tool(self, description):
        """Turn this whole agent into a TOOL another agent can call.
        This one method is the door to multi-agent systems (module 2, step 4)."""
        def delegate(task: str):
            return self.run(task)
        delegate.__name__ = "ask_" + self.name.lower().replace(" ", "_")
        delegate.__doc__ = description
        return delegate


if __name__ == "__main__":
    from toolbox import calculate, get_current_time, wiki_search

    # A full research agent is now 5 lines:
    researcher = Agent(
        name="Researcher",
        instructions=("You answer questions with facts. Never guess — use your tools. "
                      "You do NOT know today's date; call get_current_time when it matters. "
                      "Do every calculation with the calculate tool."),
        tools=[wiki_search, calculate, get_current_time],
    )
    researcher.run(" ".join(sys.argv[1:]) or "How tall is Mount Everest in feet? (1 metre = 3.28084 feet)")
