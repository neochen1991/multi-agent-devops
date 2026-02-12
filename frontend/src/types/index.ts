export type AgentStatus = 'online' | 'busy' | 'offline';

export type A2AMessage = {
  message_id: string;
  session_id: string;
  project_id: string;
  from_agent: string;
  to_agent: string;
  message_type:
    | 'HANDSHAKE_REQUEST'
    | 'HANDSHAKE_ACK'
    | 'HANDSHAKE_REJECT'
    | 'CONTENT'
    | 'STATUS'
    | 'HEARTBEAT'
    | 'INTERRUPT';
  phase: string;
  payload: Record<string, unknown>;
  correlation_id?: string;
};
