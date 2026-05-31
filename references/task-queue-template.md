# task_queue.json — 实时任务队列模板（v2）

复制此文件到 `~/AI_Team_Office/task_queue.json` 后使用。

```json
{
  "version": 2,
  "last_updated": "YYYY-MM-DDTHH:MM:SS+03:00",
  "description": "主智能体↔秘书 实时任务队列 v2",
  "tasks": [],
  "verification_rules": {
    "status_flow": "pending → in_progress → verify → done",
    "verification_states": {
      "pending": "待验证",
      "verified": "验证通过",
      "rejected": "验证不通过"
    },
    "checklist_rule": "每项必须全部打勾才能标记 verified",
    "evidence_rule": "evidence 字段必须包含可验证的证据路径"
  }
}
```

### 添加任务示例

```json
{
  "id": "T-001",
  "from": "主智能体",
  "to": "秘书",
  "title": "任务标题",
  "body": "任务描述",
  "priority": "P0",
  "status": "pending",
  "verification": "pending",
  "checklist": ["条件1", "条件2"],
  "evidence": "",
  "created_at": "YYYY-MM-DDTHH:MM:SS+03:00",
  "assigned_at": null,
  "verified_at": null,
  "completed_at": null
}
```

### 任务字段说明

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| id | string | 任务唯一标识 T-YYYYMMDD-NNN |
| from | string | 任务来源（主智能体 或 秘书） |
| to | string | 任务接收方 |
| title | string | 任务标题 |
| body | string | 任务描述 |
| priority | string | P0/P1/P2 |
| status | string | pending→in_progress→verify→done |
| verification | string | pending→verified→rejected |
| checklist | array | 验收条件列表 |
| evidence | string | 证据路径（文件路径/返回值摘要） |
| created_at | string | ISO 时间戳 |
| assigned_at | string|null | 认领时间 |
| verified_at | string|null | 验证时间 |
| completed_at | string|null | 完成时间 |
