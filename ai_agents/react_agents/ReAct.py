"""
react_agent.py
--------------
A minimal ReAct (Reasoning + Acting) agent built from scratch.

The loop:
    Thought  →  Action  →  Observation  →  repeat until Answer

No frameworks. No LangChain. Just the raw pattern.
Requires: pip install anthropic
"""

import anthropic
import json
import math

# ── 1. TOOLS ──────────────────────────────────────────────────────────────────
# Tools are just Python functions. The agent will decide which to call.

def search(query: str) -> str:
    """Simulated web search. Replace with a real search API in production."""
    fake_results = {
        "population of paris":     "Paris city proper population: ~2.1 million (2024).",
        "population of rome":      "Rome city proper population: ~2.8 million (2024).",
        "f1 champion 2024":        "Max Verstappen won the 2024 F1 World Championship with Red Bull Racing.",
        "capital of australia":    "The capital of Australia is Canberra, not Sydney.",
    }
    query_lower = query.lower()
    for key, result in fake_results.items():
        if key in query_lower:
            return result
    return f"No results found for: {query}"


def calculate(expression: str) -> str:
    """Safe math evaluator. Handles basic arithmetic and math functions."""
    try:
        # Only allow safe names — no builtins, just math functions
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        result = eval(expression, {"__builtins__": {}}, allowed)
        return str(round(result, 4))
    except Exception as e:
        return f"Calculation error: {e}"


# ── 2. TOOL REGISTRY ──────────────────────────────────────────────────────────
# Tell the agent what tools exist. Claude reads these descriptions to decide
# which tool to call and what arguments to pass.

TOOLS = [
    {
        "name": "search",
        "description": "Search the web for current information. Use this when you need facts that might be outdated in your training data.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query, e.g. 'population of Tokyo 2024'"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculate",
        "description": "Evaluate a math expression. Use Python syntax, e.g. '2.8 / 2.1' or 'sqrt(144)'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A Python math expression to evaluate."
                }
            },
            "required": ["expression"]
        }
    }
]


# ── 3. TOOL DISPATCHER ────────────────────────────────────────────────────────
# When the agent calls a tool, we route it to the right function here.

def run_tool(name: str, inputs: dict) -> str:
    if name == "search":
        return search(inputs["query"])
    elif name == "calculate":
        return calculate(inputs["expression"])
    else:
        return f"Unknown tool: {name}"


# ── 4. THE REACT LOOP ─────────────────────────────────────────────────────────
# This is the heart of the agent. It's simpler than you'd expect:
#   - Send the conversation to Claude
#   - If Claude wants to use a tool → run it, append the result, loop again
#   - If Claude gives a text answer → we're done

def react_agent(question: str, max_loops: int = 10) -> str:
    client = anthropic.Anthropic()

    # The conversation history grows with each loop iteration
    messages = [{"role": "user", "content": question}]

    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}")

    for loop_num in range(1, max_loops + 1):
        print(f"\n── Loop {loop_num} ──────────────────────────────")

        # Ask Claude what to do next
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages
        )

        # Claude's response can contain text blocks and/or tool_use blocks
        for block in response.content:

            if block.type == "text" and block.text.strip():
                print(f"[Thought] {block.text.strip()}")

            elif block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input
                print(f"[Action ] {tool_name}({json.dumps(tool_input)})")

                # Run the tool and get the result
                observation = run_tool(tool_name, tool_input)
                print(f"[Observe] {observation}")

        # stop_reason tells us why Claude stopped generating:
        #   "tool_use"   → it wants to call a tool, keep looping
        #   "end_turn"   → it's done, extract the final answer
        if response.stop_reason == "end_turn":
            # Find the last text block — that's the final answer
            final = next(
                (b.text for b in reversed(response.content) if b.type == "text"),
                "No answer generated."
            )
            print(f"\n{'='*60}")
            print(f"[Answer] {final}")
            print(f"{'='*60}\n")
            return final

        # Append Claude's response to the conversation (required by the API)
        messages.append({"role": "assistant", "content": response.content})

        # Append each tool result as a "user" message (this is the Observation step)
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": run_tool(block.name, block.input)
                })

        if tool_results:
            messages.append({"role": "user", "content": tool_results})

    return "Max loops reached without a final answer."


# ── 5. RUN IT ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    react_agent(
        "What is the population of Paris, and how does it compare to Rome? "
        "Which city is bigger and by what factor?"
    )