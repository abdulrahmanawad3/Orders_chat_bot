from states import States
import json
from tools import menu,today_deals
from langchain_core.messages import AIMessage

TOOLS = {
    "menu": menu,
    "today_deals":today_deals
}

def run_judge(question: str, answer: str) -> dict:
    raw = States.judge_chain.invoke({"inputs": question, "outputs": answer})
    cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"score": None, "comment": raw.strip()}
    


def handle_tool_calls(message: AIMessage) -> str:


    if not message.tool_calls:
        return message.content

    results = []
    for tool_call in message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call.get("args", {})

        if tool_name not in TOOLS:
            results.append(f"[Unknown tool: {tool_name}]")
            continue

        tool_fn = TOOLS[tool_name]

        output = tool_fn.invoke(tool_args)
        results.append(output)

    return "\n\n".join(results)
