from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Dict

from backend.agents.ba_agent import BAAgent
from backend.agents.dev_agent import DevAgent
from backend.agents.pm_agent import PMAgent
from backend.agents.qa_agent import QAAgent
from backend.agents.review_agent import ReviewAgent
from backend.core.git_worktree import GitWorktreeManager
from backend.core.memory import MarkdownMemoryStore
from backend.core.models import A2AMessage, LLMConfig, MessageType
from backend.core.skill_loader import SkillLoader


class AgentOrchestrator:
    def __init__(self, repo_path: str) -> None:
        self.queue: asyncio.Queue[A2AMessage] = asyncio.Queue()
        self.messages: list[A2AMessage] = []
        self.memory = MarkdownMemoryStore()
        self.skills = SkillLoader("backend/skills")
        self.skills.load_all()
        self.git = GitWorktreeManager(repo_path=repo_path)
        self.agent_index: Dict[str, object] = {}
        self.status = defaultdict(lambda: "online")
        self._init_agents()

    def _send(self, msg: A2AMessage) -> None:
        self.messages.append(msg)
        self.queue.put_nowait(msg)

    def _init_agents(self) -> None:
        default = LLMConfig(api_key="***", model_name="gpt-4o-mini")
        self.agent_index = {
            "PM": PMAgent("PM", "pm", default, self.memory, self._send),
            "BA": BAAgent("BA", "ba", default, self.memory, self._send),
            "Dev-1": DevAgent("Dev-1", "dev", default, self.memory, self._send, git=self.git, skills=self.skills),
            "Dev-2": DevAgent("Dev-2", "dev", default, self.memory, self._send, git=self.git, skills=self.skills),
            "Review": ReviewAgent("Review", "review", default, self.memory, self._send, git=self.git),
            "QA": QAAgent("QA", "qa", default, self.memory, self._send, skills=self.skills),
        }

    async def emit_user_request(self, session_id: str, project_id: str, text: str) -> None:
        kickoff = A2AMessage(
            message_id="user-0",
            session_id=session_id,
            project_id=project_id,
            from_agent="USER",
            to_agent="PM",
            message_type=MessageType.CONTENT,
            phase="intake",
            payload={"user_input": text},
            ts="",
        )
        self._send(kickoff)

    async def run_once(self) -> A2AMessage:
        msg = await self.queue.get()
        target = self.agent_index.get(msg.to_agent)
        if target:
            if msg.message_type == MessageType.HANDSHAKE_ACK and msg.correlation_id:
                target.on_ack(msg.session_id, msg.correlation_id)
            await target.handle(msg)
        return msg
