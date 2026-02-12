from __future__ import annotations

from pathlib import Path


class MarkdownMemoryStore:
    def __init__(self, root: str = "./memory") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def file_for(self, agent_id: str, session_id: str) -> Path:
        return self.root / f"{agent_id}_{session_id}.md"

    def append(self, agent_id: str, session_id: str, text: str) -> Path:
        file = self.file_for(agent_id, session_id)
        with file.open("a", encoding="utf-8") as f:
            f.write(text + "\n")
        return file

    def read(self, agent_id: str, session_id: str) -> str:
        file = self.file_for(agent_id, session_id)
        return file.read_text(encoding="utf-8") if file.exists() else ""
