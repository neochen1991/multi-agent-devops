from __future__ import annotations

from backend.agents.base import BaseAgent
from backend.core.git_worktree import GitWorktreeManager
from backend.core.models import A2AMessage, MessageType


class ReviewAgent(BaseAgent):
    def __init__(self, *args, git: GitWorktreeManager, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.git = git

    async def handle(self, msg: A2AMessage) -> None:
        if msg.phase != "code_review" or msg.message_type != MessageType.CONTENT:
            return
        branch = msg.payload["branch"]
        approved = True
        if approved:
            self.git.merge_to_dev(branch)
            feedback = {"approved": True, "merged_branch": branch}
            kind = MessageType.HANDSHAKE_ACK
        else:
            feedback = {"approved": False, "comment": "请修复类型注解与测试覆盖率"}
            kind = MessageType.HANDSHAKE_REJECT

        response = self._new_message(
            session_id=msg.session_id,
            project_id=msg.project_id,
            from_agent=self.agent_id,
            to_agent=msg.from_agent,
            message_type=kind,
            phase="code_review",
            payload=feedback,
            correlation_id=msg.message_id,
        )
        self.send_message(response)
