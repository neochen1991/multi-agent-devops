from __future__ import annotations

from backend.agents.base import BaseAgent
from backend.core.models import A2AMessage, MessageType
from backend.core.skill_loader import SkillLoader


class QAAgent(BaseAgent):
    def __init__(self, *args, skills: SkillLoader, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.skills = skills

    async def handle(self, msg: A2AMessage) -> None:
        if msg.phase != "it_design_review" or msg.message_type != MessageType.CONTENT:
            return
        cases = [
            "创建会话应返回200",
            "未握手禁止执行开发",
            "代码审查拒绝时禁止合并",
        ]
        report = {"cases": cases, "result": "pending"}
        self.write_memory(msg.session_id, f"## QA Cases\n{report}")
        if "run_pytest" in self.skills.registry:
            outcome = self.skills.registry["run_pytest"](".")
            self.write_memory(msg.session_id, f"## QA Run\n{outcome}")
