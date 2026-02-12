# A2A Multi-Agent DevOps System

## 1) 系统技术架构图

```mermaid
flowchart LR
  U[User / Product Owner] --> FE[React UI\nDiscord-like Console]
  FE <-->|WebSocket| API[FastAPI A2A Gateway]
  API --> ORCH[Agent Orchestrator\nHandshake State Machine]

  ORCH --> PM[PM Agent]
  ORCH --> BA[BA Agent]
  ORCH --> D1[Dev Agent 1]
  ORCH --> D2[Dev Agent 2]
  ORCH --> RV[Review Agent]
  ORCH --> QA[QA Agent]

  D1 --> GIT[Git Worktree Manager]
  D2 --> GIT
  RV --> GIT

  PM --> MEM[(Markdown Memory)]
  BA --> MEM
  D1 --> MEM
  D2 --> MEM
  RV --> MEM
  QA --> MEM

  ORCH --> MCP[MCP Tool Client]
  ORCH --> SK[Skill Loader\n(plugin .py)]
```

## 2) A2A 握手协议详细设计

- Schema 文件：`backend/schemas/a2a_message.schema.json`
- 强制机制：
  - 任何需要跨阶段推进的动作都必须先发 `HANDSHAKE_REQUEST`。
  - 只有收到 `HANDSHAKE_ACK` 后对应 Agent 才可推进阶段。
  - `HANDSHAKE_REJECT` 将中断流程并写入反馈。

核心字段：
- `message_type`: `HANDSHAKE_REQUEST | HANDSHAKE_ACK | HANDSHAKE_REJECT | CONTENT | STATUS | HEARTBEAT | INTERRUPT`
- `requires_ack`: `HANDSHAKE_REQUEST` 必须是 `true`
- `correlation_id`: ACK/REJECT 必须回填原请求 `message_id`

## 3) 后端核心实现

- `SkillLoader`：动态扫描 `backend/skills/*.py` 并加载 `@skill` 标记函数。
- `GitWorktreeManager`：为每个 Dev Agent 创建独立分支 + worktree，支持 commit/merge/cleanup。
- Agent 特性：
  - PM：输入解析 + 需求拆解 + 发起给 BA 的握手。
  - BA：产出 `Business_Detail_Design` 结构 + ACK PM + 通知 Dev/QA 评审。
  - Dev：在 worktree 下生成 IT 设计与代码，提交后发 Review。
  - Review：执行审查结果判定，通过则 merge dev，否则 REJECT 回退。
  - QA：生成用例，执行测试 skill，写报告到 memory。
- 防止“自行开动”：`BaseAgent.assert_no_pending_handshake()` 在开发前强校验。

## 4) 前端核心实现

- 组件：
  - `Sidebar`: Session 列表 + Agent 在线状态灯
  - `ChatArea`: Markdown 消息流、颜色区分、握手徽章、用户干预、Mermaid 进度图
  - `InfoPanel`: Agent 概览、日志、记忆文档预览
- WebSocket：`useAgentSocket` 接收消息、状态心跳、向后端发送 START/FORCE_PAUSE/RESUME。

## 5) 完整工作流演示

1. 用户在前端输入需求，发送 `START`。
2. PM 接收并拆解需求，写 memory，向 BA 发 `HANDSHAKE_REQUEST`。
3. BA 生成业务详细设计，回 `HANDSHAKE_ACK` 给 PM，并广播 IT 评审给 Dev/QA。
4. Dev-1/Dev-2 并行创建 worktree，产出设计+代码，提交后发给 Review。
5. Review 审查通过则 merge 到 `dev`；拒绝则返回 `HANDSHAKE_REJECT` + 修改意见。
6. QA 基于需求生成测试用例，调用测试 skill 执行，产出测试报告。
7. 前端全程实时展示消息流、状态、日志、记忆文件内容。
