import { useEffect, useMemo, useState } from 'react';
import { A2AMessage, AgentStatus } from '../types';

export function useAgentSocket(url: string) {
  const [messages, setMessages] = useState<A2AMessage[]>([]);
  const [status, setStatus] = useState<Record<string, AgentStatus>>({
    PM: 'online', BA: 'online', 'Dev-1': 'online', 'Dev-2': 'online', Review: 'online', QA: 'online'
  });

  const ws = useMemo(() => new WebSocket(url), [url]);

  useEffect(() => {
    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data) as A2AMessage;
      setMessages((prev) => [...prev, msg]);
      setStatus((prev) => ({ ...prev, [msg.from_agent]: msg.message_type === 'HEARTBEAT' ? 'online' : 'busy' }));
    };
    return () => ws.close();
  }, [ws]);

  const send = (payload: Record<string, unknown>) => ws.send(JSON.stringify(payload));

  return { messages, status, send };
}
