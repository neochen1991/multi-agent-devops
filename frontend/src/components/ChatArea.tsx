import React from 'react';
import ReactMarkdown from 'react-markdown';
import { A2AMessage } from '../types';

type Props = { messages: A2AMessage[]; onIntervene: (text: string) => void };

const colorMap: Record<string, string> = { PM: '#9b59b6', BA: '#3498db', 'Dev-1': '#2ecc71', 'Dev-2': '#27ae60', Review: '#f39c12', QA: '#e74c3c' };

export const ChatArea: React.FC<Props> = ({ messages, onIntervene }) => (
  <main className="chat-area">
    {messages.map((m) => (
      <div key={m.message_id} className="bubble" style={{ borderLeft: `4px solid ${colorMap[m.from_agent] || '#95a5a6'}` }}>
        <div><strong>{m.from_agent}</strong> → {m.to_agent}</div>
        {m.message_type === 'HANDSHAKE_REQUEST' && <span className="badge">等待确认...</span>}
        <ReactMarkdown>{JSON.stringify(m.payload, null, 2)}</ReactMarkdown>
      </div>
    ))}
    <button onClick={() => onIntervene('请优先完成测试并反馈')}>用户干预</button>
    <ReactMarkdown>{'```mermaid\nflowchart LR\nA[需求分解]-->B[详细设计]-->C[开发中]-->D[评审]-->E[测试]\n```'}</ReactMarkdown>
  </main>
);
