"""
Chat engine — manages conversation with Claude API and tool execution.
"""

import json
import anthropic
from .prompts import SYSTEM_PROMPT
from .tools import TOOLS, execute_tool

MODEL = "claude-sonnet-4-5-20250929"


class ChatEngine:
    """Manages a conversation session with the IMU assistant."""

    def __init__(self, api_key: str = None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.messages = []

    def send_message(self, user_message: str) -> str:
        """Send a user message and return the assistant's response.

        Handles tool use automatically — if Claude wants to call a tool,
        we execute it and send the result back until we get a text response.
        """
        self.messages.append({"role": "user", "content": user_message})

        while True:
            response = self.client.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=self.messages,
            )

            # Collect the full response
            self.messages.append({"role": "assistant", "content": response.content})

            # If no tool use, we're done — extract text
            if response.stop_reason == "end_turn":
                return self._extract_text(response.content)

            # Handle tool use
            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = execute_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result, ensure_ascii=False),
                        })

                # Send tool results back to Claude
                self.messages.append({"role": "user", "content": tool_results})

    def reset(self):
        """Clear conversation history."""
        self.messages = []

    def _extract_text(self, content) -> str:
        """Extract text from response content blocks."""
        parts = []
        for block in content:
            if hasattr(block, "text"):
                parts.append(block.text)
        return "\n".join(parts)
