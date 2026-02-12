import React from 'react';
import { AgentStatus } from '../types';

type Props = {
  sessions: string[];
  agents: string[];
  status: Record<string, AgentStatus>;
};

const statusColor: Record<AgentStatus, string> = {
  online: '#3ba55c',
  busy: '#faa61a',
  offline: '#747f8d'
};

export const Sidebar: React.FC<Props> = ({ sessions, agents, status }) => (
  <aside className="sidebar">
    <h3>Sessions</h3>
    {sessions.map((s) => <div key={s}>{s}</div>)}
    <h3>Agents</h3>
    {agents.map((agent) => (
      <div key={agent} className="agent-item">
        <span className="dot" style={{ backgroundColor: statusColor[status[agent] || 'offline'] }} />{agent}
      </div>
    ))}
  </aside>
);
