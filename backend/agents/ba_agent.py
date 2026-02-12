from __future__ import annotations

from backend.agents.base import BaseAgent
from backend.core.models import A2AMessage, MessageType


class BAAgent(BaseAgent):
    async def handle(self, msg: A2AMessage) -> None:
        if msg.message_type == MessageType.HANDSHAKE_REQUEST and msg.phase == "requirements_breakdown":
            design = {
                "file": "Business_Detail_Design.md",
                "business_flow": ["需求录入", "方案设计", "开发", "评审", "测试"],
                "data_dictionary": {"session_id": "string", "agent_id": "string", "status": "enum"},
            }
            self.write_memory(msg.session_id, f"## BA Design\n{design}")
            ack = self._new_message(
                session_id=msg.session_id,
                project_id=msg.project_id,
                from_agent=self.agent_id,
                to_agent=msg.from_agent,
                message_type=MessageType.HANDSHAKE_ACK,
                phase=msg.phase,
                payload={"accepted": True},
                correlation_id=msg.message_id,
            )
            self.send_message(ack)
            for target in ["Dev-1", "Dev-2", "QA"]:
                notice = self._new_message(
                    session_id=msg.session_id,
                    project_id=msg.project_id,
                    from_agent=self.agent_id,
                    to_agent=target,
                    message_type=MessageType.CONTENT,
                    phase="it_design_review",
                    payload=design,
                )
                self.send_message(notice)
