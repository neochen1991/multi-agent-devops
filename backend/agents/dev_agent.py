from __future__ import annotations

from pathlib import Path

from backend.agents.base import BaseAgent
from backend.core.git_worktree import GitWorktreeManager
from backend.core.models import A2AMessage, MessageType
from backend.core.skill_loader import SkillLoader


class DevAgent(BaseAgent):
    def __init__(self, *args, git: GitWorktreeManager, skills: SkillLoader, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.git = git
        self.skills = skills

    async def handle(self, msg: A2AMessage) -> None:
        if msg.phase != "it_design_review" or msg.message_type != MessageType.CONTENT:
            return
        self.assert_no_pending_handshake(msg.session_id)
        worktree = self.git.create_for_agent(self.agent_id, msg.session_id)
        self._write_design(worktree)
        self._write_code(worktree)
        self.git.commit_all(worktree, f"{self.agent_id}: implement feature for {msg.session_id}")
        review_msg = self._new_message(
            session_id=msg.session_id,
            project_id=msg.project_id,
            from_agent=self.agent_id,
            to_agent="Review",
            message_type=MessageType.CONTENT,
            phase="code_review",
            payload={"worktree": str(worktree), "branch": f"{self.agent_id}/{msg.session_id}"},
        )
        self.send_message(review_msg)

    def _write_design(self, worktree: Path) -> None:
        (worktree / "IT_Detail_Design.md").write_text(
            "# API Design\n- POST /sessions\n\n# Class Diagram\nAgent -> SkillLoader\n", encoding="utf-8"
        )

    def _write_code(self, worktree: Path) -> None:
        src = worktree / f"generated_{self.agent_id.lower().replace('-', '_')}.py"
        src.write_text("def generated():\n    return 'ok'\n", encoding="utf-8")
