from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class MessageType(str, Enum):
    HANDSHAKE_REQUEST = "HANDSHAKE_REQUEST"
    HANDSHAKE_ACK = "HANDSHAKE_ACK"
    HANDSHAKE_REJECT = "HANDSHAKE_REJECT"
    CONTENT = "CONTENT"
    STATUS = "STATUS"
    HEARTBEAT = "HEARTBEAT"
    INTERRUPT = "INTERRUPT"


@dataclass
class A2AMessage:
    message_id: str
    session_id: str
    project_id: str
    from_agent: str
    to_agent: str
    message_type: MessageType
    phase: str
    payload: Dict[str, Any] = field(default_factory=dict)
    requires_ack: bool = False
    correlation_id: Optional[str] = None
    ts: str = ""


@dataclass
class LLMConfig:
    api_key: str
    model_name: str
    base_url: str = "https://api.openai.com/v1"
    temperature: float = 0.2
