---
name: multi-agent-orchestration-v2
description: 侯总 AI 团队完整编排体系 v2 — 8人层级结构、双向通信协议、实时同步机制、verify→iterate 验证执行循环
tags: [team, orchestration, communication, verification, real-time, multi-agent]
---

# 多智能体团队编排 v2

> 版本：v2.0 | 更新：2026-06-01
> 适用：Hermes Agent 任意版本（纯 Skill 方案，零外部依赖）

## 概览

当 Hermes Agent 加载此 Skill 后，你将学会如何搭建并运行一个 **8 人多智能体团队**，包含：

- 层级结构（单协调器 + 7 个子智能体）
- 双向实时通信协议（delegate_task + 文件通道双轨）
- 实时同步机制（shared_memory 时间戳 + cron 轮询）
- verify→iterate 验证执行循环（执行→checklist 验证→通过/退回）

---

## 一、团队层级结构

```
用户 — 最终决策者
  └── 主智能体（思远）— 团队大脑、总控、唯一调度者
        ├── 秘书-agent — 微信/消息入口，日程管理（Gateway 独立进程）
        ├── 审计-agent — 验证执行循环的守门人
        ├── 科研-agent — 文献/选题
        ├── 论文-agent — 论文编辑/审稿
        ├── 编程-agent — 代码/调试
        ├── 求职-agent — 求职规划
        └── 科普-agent — 科普写作
```

**铁则：**
- 主智能体是**唯一调度者**，所有任务由其拆解、分配、验收
- 子智能体不得跨级汇报、不得擅自行动
- 文件管理统一由主智能体执行（子智能体不自行创建文件）

---

## 二、通信协议

### 通道矩阵

| 方向 | 通道 | 延迟 | 适用 |
|:-----|:-----|:----:|:-----|
| 主→子 | `delegate_task` | 实时 | 任务派发+执行 |
| 子→主 | `reports/{名}_{日期}.md` | 异步 | 工作汇报 |
| 主→子(回复) | `reports/responses/{名}_{日期}_response.md` | 异步 | 审批回复 |
| 主↔秘书 | `shared_memory.md` | ~1min | 信息同步 |
| 主→秘书 | `task_queue.json` | ~1min | 任务派发 |
| 秘书→主 | `delegate_task` | 实时 | 秘书调用主智能体 |
| 紧急 | 用户直接传话 | 实时 | 任何通道失效时 |

### 基础设施文件

```
~/AI_Team_Office/
├── shared_commands.md     # 团队共享指令+通信协议
├── shared_memory.md       # 主↔秘书 共享工作记忆
├── task_queue.json        # 实时任务队列（v2 验证版）
├── reports/               # 子智能体→主智能体 汇报
│   └── responses/         # 主智能体→子智能体 回复
```

### 实时同步机制（主↔秘书）

秘书在独立 Gateway 进程上运行，不能直接 `delegate_task` 给主智能体时：

1. **shared_memory.md 时间戳标记：** 双方更新后追加 `<!-- 更新者 @ 时间 -->`
2. **cron 轮询：** 每 10 分钟检查 shared_memory.md 修改时间（no_agent 脚本，零 token）
3. **任务队列：** `task_queue.json` 每 1 分钟 cron 轮询（no_agent 脚本）
4. **同步标记：** 新决策/紧急变更分别在文件顶部加标记

---

## 三、任务生命周期（v2 验证版）

```
主智能体派任务（含 checklist + 验收标准）
  │
  ├── [子智能体] delegate_task（实时）
  └── [秘书] task_queue.json + shared_memory（~1min轮询）
        │
        ▼
  执行
        │
        ▼
  审计验证（checklist 逐项打勾 + evidence 检查）
  ├── ✅ 全部通过 → verification = verified → 标记 done
  └── ❌ 不通过 → verification = rejected + 退回原因 → 重做
       └── 最多 3 次 → 仍不通过 → 主智能体裁决
```

### 状态四态

| 状态 | 含义 | 设置者 |
|:-----|:-----|:-------|
| `pending` | 待领取 | 主智能体 |
| `in_progress` | 执行中 | 执行者 |
| `verify` | 待验证 | 审计 |
| `done` | 已完成 | 主智能体确认 |

### Verification 三态

| 状态 | 含义 |
|:-----|:-----|
| `verified` | 验证通过 — checklist 全部打勾，evidence 完整 |
| `rejected` | 验证不通过 — 附退回原因，退回重做 |
| `pending` | 暂未验证 |

---

## 四、task_queue.json v2 格式

```json
{
  "version": 2,
  "tasks": [
    {
      "id": "T-001",
      "from": "主智能体",
      "to": "秘书",
      "title": "任务标题",
      "body": "任务描述",
      "priority": "P0",
      "status": "pending",
      "verification": "pending",
      "checklist": ["条件1", "条件2", "条件3"],
      "evidence": "证据文件路径",
      "created_at": "ISO 时间戳",
      "completed_at": null
    }
  ],
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

---

## 五、验证报告模板

```markdown
## 验证报告: [任务ID]

### 交付物检查
- [ ] 交付物存在（文件路径可访问）
- [ ] 内容完整（无截断/空字段）
- [ ] 格式合规

### 逻辑检查
- [ ] 数据来源真实可追溯
- [ ] 结论合理（无夸大/虚假）
- [ ] 代码逻辑自洽

### 协议合规
- [ ] 未违反文件管理规则
- [ ] 未擅自修改配置/记忆
- [ ] 汇报协议已遵循

### 结论
- [✅ verified] 验证通过 | [❌ rejected] 退回重做
- 退回原因：...
```

---

## 六、汇报与回复模板

### 子智能体汇报格式

```markdown
# 汇报：[标题]
汇报人：[智能体名]
日期：YYYY-MM-DD
汇报对象：主智能体

## 工作完成
- [任务1]: [状态]

## 遇到的问题
- [需要主智能体协助的问题]

## 下一步计划
- [计划1]
```

### 主智能体回复格式

```markdown
# 回复：[汇报标题]

收件人：[智能体名]
日期：YYYY-MM-DD

## 确认
[回复内容]
```

---

## 七、防撒谎机制

| 验证方式 | 适用场景 | 规则 |
|:---------|:---------|:-----|
| delegate_task 返回值 | 子智能体→主智能体实时任务 | 必须返回具体结果（成功/失败+证据路径） |
| shared_memory.md 时间戳 | 任何信息更新 | `<!-- 更新者 @ 时间 -->` 不可伪造 |
| task_queue.json 状态链 | 任务派发 | pending→in_progress→verify→done 不可跳级 |
| reports/ 文件 | 工作汇报 | 历史文件不可删除 |

**撒谎后果：** 三次撒谎直接降级。

---

## 八、快速部署

### 1. 创建基础设施目录

```bash
mkdir -p ~/AI_Team_Office/reports/responses
```

### 2. 初始化 shared_commands.md（写入通信协议）

### 3. 初始化 shared_memory.md（写入项目状态+决策记录）

### 4. 初始化 task_queue.json（v2 格式）

### 5. 设置 cron 轮询

```bash
# 秘书任务板轮询（每1分钟，no_agent）
hermes cron create --name "秘书任务板轮询" --schedule "every 1m" \
  --no-agent --script check_task_queue.py --profile <秘书-profile名>

# 同步检查（每10分钟，no_agent）
hermes cron create --name "同步检查" --schedule "every 10m" \
  --no-agent --script check_faina_sync.py
```

### 6. 通知所有子智能体

通过 `delegate_task` 通知每个子智能体通信协议，要求写测试汇报验证。

### 7. 验证全链路

用 `delegate_task` 对每个子智能体做一次双向通信测试。

---

## 九、模型隔离规则

| 用途 | Provider | 模型 |
|:-----|:---------|:-----|
| 主智能体对话 | deepseek | deepseek-v4-pro |
| 秘书对话 | deepseek | deepseek-v4-flash |
| 所有后台 auxiliary | **xiaomi** | **mimo-v2.5** |
| delegate_task 子智能体 | **xiaomi** | **mimo-v2.5-pro** |
| 多模态/识图 | **xiaomi** | **mimo-v2.5** |
| 网页搜索（原生 web_search） | ddgs | 无需 API key |

**铁律：** provider/模型/base_url 三件套必须完全匹配。不允许 `provider: auto`。每个 service 必须显式声明。
