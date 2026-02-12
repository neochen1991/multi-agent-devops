from __future__ import annotations

from backend.agents.base import BaseAgent
from backend.core.models import A2AMessage, MessageType


class PMAgent(BaseAgent):
    async def handle(self, msg: A2AMessage) -> None:
        if msg.message_type != MessageType.CONTENT:
            return
        requirements = msg.payload.get("user_input", "")
        result = {
            "business_requirements": [
                "用户管理与鉴权",
                "多 Agent 并行开发",
                "质量评审与自动化测试",
            ],
            "source": requirements,
        }
        self.write_memory(msg.session_id, f"## PM Breakdown\n{result}")
        self.request_handshake(
            msg.session_id,
            msg.project_id,
            "BA",
            phase="requirements_breakdown",
            payload=result,
        )
