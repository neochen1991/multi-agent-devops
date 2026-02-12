from __future__ import annotations

from typing import Any, Dict, List


class MCPToolClient:
    """Thin wrapper for MCP server tool discovery + invocation."""

    def __init__(self) -> None:
        self.tools: Dict[str, Dict[str, Any]] = {}

    async def connect(self, endpoint: str) -> None:
        # Replace with real MCP transport initialization.
        self.endpoint = endpoint

    async def load_tools(self, tool_defs: List[Dict[str, Any]]) -> None:
        for t in tool_defs:
            self.tools[t["name"]] = t

    async def call_tool(self, name: str, **kwargs: Any) -> Dict[str, Any]:
        if name not in self.tools:
            raise KeyError(f"Tool {name} is not registered")
        return {"tool": name, "args": kwargs, "status": "simulated"}
