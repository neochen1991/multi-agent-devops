from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime, timezone
from typing import Callable, Dict
from uuid import uuid4

from backend.core.memory import MarkdownMemoryStore
from backend.core.models import A2AMessage, LLMConfig, MessageType


class AgentStateError(RuntimeError):
    pass


class BaseAgent(ABC):
    def __init__(
        self,
        agent_id: str,
        role: str,
        llm: LLMConfig,
        memory: MarkdownMemoryStore,
        send_message: Callable[[A2AMessage], None],
    ) -> None:
        self.agent_id = agent_id
        self.role = role
        self.llm = llm
        self.memory = memory
        self.send_message = send_message
        self.pending_acks: Dict[str, set[str]] = defaultdict(set)
        self.paused = False

    def _new_message(self, **kwargs: object) -> A2AMessage:
        return A2AMessage(
            message_id=str(uuid4()),
            ts=datetime.now(timezone.utc).isoformat(),
            **kwargs,
        )

    def request_handshake(self, session_id: str, project_id: str, to_agent: str, phase: str, payload: dict) -> str:
        msg = self._new_message(
            session_id=session_id,
            project_id=project_id,
            from_agent=self.agent_id,
            to_agent=to_agent,
            message_type=MessageType.HANDSHAKE_REQUEST,
            phase=phase,
            payload=payload,
            requires_ack=True,
        )
        self.pending_acks[session_id].add(msg.message_id)
        self.send_message(msg)
        return msg.message_id

    def on_ack(self, session_id: str, correlation_id: str) -> None:
        self.pending_acks[session_id].discard(correlation_id)

    def assert_no_pending_handshake(self, session_id: str) -> None:
        if self.pending_acks[session_id]:
            raise AgentStateError(
                f"{self.agent_id} cannot continue: waiting for ACK {self.pending_acks[session_id]}"
            )

    def write_memory(self, session_id: str, text: str) -> None:
        self.memory.append(self.agent_id, session_id, text)

    @abstractmethod
    async def handle(self, msg: A2AMessage) -> None:
        raise NotImplementedError
