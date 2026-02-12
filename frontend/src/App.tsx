import React, { useMemo, useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatArea } from './components/ChatArea';
import { InfoPanel } from './components/InfoPanel';
import { useAgentSocket } from './hooks/useAgentSocket';

export default function App() {
  const { messages, status, send } = useAgentSocket('ws://localhost:8000/ws');
  const [selectedAgent] = useState('PM');

  const logs = useMemo(() => messages.map((m) => `${m.from_agent}: ${m.phase}`), [messages]);

  return (
    <div className="layout">
      <Sidebar sessions={['project-alpha/session-001']} agents={['PM', 'BA', 'Dev-1', 'Dev-2', 'Review', 'QA']} status={status} />
      <ChatArea
        messages={messages}
        onIntervene={(text) => send({ type: 'START', session_id: 'session-001', project_id: 'project-alpha', text })}
      />
      <InfoPanel selectedAgent={selectedAgent} modelName="gpt-4o-mini" logs={logs} memoryContent={'# memory preview'} />
      <div className="controls">
        <button onClick={() => send({ type: 'FORCE_PAUSE' })}>强制暂停</button>
        <button onClick={() => send({ type: 'RESUME' })}>继续执行</button>
      </div>
    </div>
  );
}
