from __future__ import annotations

import json

from fastapi import FastAPI, WebSocket

from backend.orchestrator import AgentOrchestrator

app = FastAPI(title="A2A Multi-Agent DevOps")
orchestrator = AgentOrchestrator(repo_path=".")


@app.websocket("/ws")
async def ws_stream(ws: WebSocket) -> None:
    await ws.accept()
    while True:
        raw = await ws.receive_text()
        cmd = json.loads(raw)
        if cmd["type"] == "START":
            await orchestrator.emit_user_request(cmd["session_id"], cmd["project_id"], cmd["text"])
        elif cmd["type"] == "FORCE_PAUSE":
            for a in orchestrator.agent_index.values():
                a.paused = True
        elif cmd["type"] == "RESUME":
            for a in orchestrator.agent_index.values():
                a.paused = False

        processed = await orchestrator.run_once()
        await ws.send_text(json.dumps(processed.__dict__, default=str))
