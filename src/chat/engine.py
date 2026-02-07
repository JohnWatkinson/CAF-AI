"""
Chat engine — manages conversation with Claude API and tool execution.
"""

import json
import logging
import anthropic
from .prompts import SYSTEM_PROMPT
from .tools import TOOLS, execute_tool

log = logging.getLogger(__name__)

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
        log.info("User [%d msgs]: %s", len(self.messages), user_message[:200])

        while True:
            try:
                response = self.client.messages.create(
                    model=MODEL,
                    max_tokens=1024,
                    system=SYSTEM_PROMPT,
                    tools=TOOLS,
                    messages=self.messages,
                )
            except anthropic.APIError as e:
                log.error("Claude API error: %s", e)
                raise

            # Collect the full response
            self.messages.append({"role": "assistant", "content": response.content})

            # If no tool use, we're done — extract text
            if response.stop_reason == "end_turn":
                text = self._extract_text(response.content)
                log.info("Assistant: %s", text[:200])
                return text

            # Handle tool use
            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        log.info("Tool call: %s(%s)", block.name, json.dumps(block.input, ensure_ascii=False)[:200])
                        try:
                            result = execute_tool(block.name, block.input)
                        except Exception as e:
                            log.error("Tool %s failed: %s", block.name, e)
                            result = {"error": str(e)}
                        log.info("Tool result: %s", json.dumps(result, ensure_ascii=False)[:200])
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
