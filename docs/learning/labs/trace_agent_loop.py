"""Run the real StayCode Agent loop with a scripted client and a pure tool.

No provider configuration, network request, shell tool, or API key is used.
Run from anywhere with StayCode's virtual-environment Python.
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT))

from pydantic import BaseModel
from staycode.agent import Agent, LoopComplete, ToolResultEvent
from staycode.client import LLMClient
from staycode.conversation import ConversationManager
from staycode.serialization import build_anthropic_messages
from staycode.tools import ToolRegistry
from staycode.tools.base import StreamEnd, TextDelta, Tool, ToolCallComplete, ToolResult


class AddParams(BaseModel):
    a: int
    b: int


class AddTool(Tool):
    name = "AddNumbers"
    description = "Return the sum of two integers. No side effects."
    params_model = AddParams
    category = "read"

    async def execute(self, params: AddParams) -> ToolResult:
        return ToolResult(output=str(params.a + params.b))


class ScriptedClient(LLMClient):
    def __init__(self):
        self.calls = 0

    async def stream(self, conversation, system, tools):
        self.calls += 1
        print(f"\nMODEL CALL {self.calls}: history={len(conversation.history)}")
        assert any(t["name"] == "AddNumbers" for t in tools)
        if self.calls == 1:
            yield TextDelta(text="I will call AddNumbers.")
            yield ToolCallComplete(
                tool_id="lab-call-1", tool_name="AddNumbers", arguments={"a": 19, "b": 23}
            )
            yield StreamEnd(stop_reason="tool_use", input_tokens=20, output_tokens=10)
        elif self.calls == 2:
            results = [r for m in conversation.history for r in m.tool_results]
            assert len(results) == 1
            assert results[0].tool_use_id == "lab-call-1"
            assert results[0].content == "42"
            yield TextDelta(text="The answer is 42.")
            yield StreamEnd(stop_reason="end_turn", input_tokens=40, output_tokens=8)
        else:
            raise AssertionError("The loop should stop after the second response")


async def main():
    registry = ToolRegistry()
    registry.register(AddTool())
    client = ScriptedClient()
    conversation = ConversationManager()
    conversation.add_user_message("What is 19 + 23? Use AddNumbers.")
    events = []
    with TemporaryDirectory(prefix="staycode-learning-") as work_dir:
        agent = Agent(
            client=client, registry=registry, protocol="anthropic",
            work_dir=work_dir, max_iterations=3, context_window=200_000,
        )
        async for event in agent.run(conversation):
            events.append(event)
            print(f"  {type(event).__name__}: {event}")

    assert client.calls == 2
    assert isinstance(events[-1], LoopComplete)
    assert events[-1].total_turns == 2
    assert any(isinstance(e, ToolResultEvent) and e.output == "42" for e in events)
    assert conversation.history[-1].content == "The answer is 42."
    print("\nINTERNAL MESSAGES (environment text omitted):")
    for message in conversation.history:
        if message.content.startswith("Current time:"):
            continue
        print(json.dumps({
            "role": message.role, "content": message.content,
            "tool_uses": [vars(x) for x in message.tool_uses],
            "tool_results": [vars(x) for x in message.tool_results],
        }, ensure_ascii=True))
    print("\nANTHROPIC SERIALIZATION:")
    for message in build_anthropic_messages(conversation.get_messages()):
        # The first user message may merge the environment and user input.
        print(json.dumps(message, ensure_ascii=True))
    print("\nPASS: real Agent loop, two scripted model responses, one paired tool result.")


if __name__ == "__main__":
    asyncio.run(main())
