from __future__ import annotations

import subprocess
from pathlib import Path


class GitWorktreeManager:
    """Allocate isolated git worktrees for parallel Dev agents."""

    def __init__(self, repo_path: str, root_worktree_dir: str = ".worktrees") -> None:
        self.repo_path = Path(repo_path)
        self.root_worktree_dir = self.repo_path / root_worktree_dir
        self.root_worktree_dir.mkdir(parents=True, exist_ok=True)

    def create_for_agent(self, agent_id: str, session_id: str, base_branch: str = "dev") -> Path:
        branch = f"{agent_id}/{session_id}"
        target = self.root_worktree_dir / branch.replace("/", "_")
        self._run(["git", "worktree", "add", "-b", branch, str(target), base_branch])
        return target

    def commit_all(self, worktree: Path, msg: str) -> None:
        self._run(["git", "-C", str(worktree), "add", "."])
        self._run(["git", "-C", str(worktree), "commit", "-m", msg])

    def merge_to_dev(self, source_branch: str) -> None:
        self._run(["git", "checkout", "dev"])
        self._run(["git", "merge", "--no-ff", source_branch])

    def cleanup(self, worktree: Path) -> None:
        self._run(["git", "worktree", "remove", str(worktree), "--force"])

    def _run(self, cmd: list[str]) -> None:
        subprocess.run(cmd, cwd=self.repo_path, check=True)
