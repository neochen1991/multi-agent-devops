import React from 'react';

type Props = {
  selectedAgent: string;
  modelName: string;
  logs: string[];
  memoryContent: string;
};

export const InfoPanel: React.FC<Props> = ({ selectedAgent, modelName, logs, memoryContent }) => (
  <aside className="info-panel">
    <h3>Agent 概览</h3>
    <p>{selectedAgent} - model: {modelName}</p>
    <h3>实时日志/终端</h3>
    <pre>{logs.join('\n')}</pre>
    <h3>记忆文档预览</h3>
    <pre>{memoryContent}</pre>
  </aside>
);
