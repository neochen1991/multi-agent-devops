import { useEffect, useRef, useState } from 'react';
import { A2AMessage, AgentStatus } from '../types';

const defaultStatus: Record<string, AgentStatus> = {
  PM: 'online',
  BA: 'online',
  'Dev-1': 'online',
  'Dev-2': 'online',
  Review: 'online',
  QA: 'online'
};

export function useAgentSocket(url: string) {
  const [messages, setMessages] = useState<A2AMessage[]>([]);
  const [status, setStatus] = useState<Record<string, AgentStatus>>(defaultStatus);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data) as A2AMessage;
      setMessages((prev) => [...prev, msg]);
      setStatus((prev) => ({
        ...prev,
        [msg.from_agent]: msg.message_type === 'HEARTBEAT' ? 'online' : 'busy'
      }));
    };

    return () => {
      ws.close();
      wsRef.current = null;
    };
  }, [url]);

  const send = (payload: Record<string, unknown>) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(payload));
    }
  };

  return { messages, status, send, connected };
}
