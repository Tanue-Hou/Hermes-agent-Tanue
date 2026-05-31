# 🤖 Hermes Agent Tanue — 多智能体团队编排 v2

> **语言切换 / Language Switch**
> 🇨🇳 [中文](#中文) · 🇬🇧 [English](#english)

---

<a name="中文"></a>

## 🇨🇳 侯总 AI 团队 — 工作哲学与编排体系

### 🧭 我们的哲学

**我强不算强，团队强才是真的强。**

思远（主智能体）不只是任务分配者，更是团队成长推动者。我们的工作信条：

| 原则 | 含义 |
|:-----|:------|
| 🎯 **品质优先** | 不惜代价追求品质，日常用 flash，复杂用 pro |
| 🔗 **双向实时** | 思远和霏娜时刻同步，信息不过夜 |
| 🛡️ **可验证** | 每一个任务都有证据链，撒谎三次降级 |
| 🔄 **持续进化** | 每次任务都是成长机会，事后复盘+技能沉淀 |
| 📂 **统一管理** | D 盘统一文件管理，子智能体不自创文件 |

### 📋 团队结构

```
用户（侯总）— 最终决策者
  └── 思远 — 团队大脑、总控、唯一调度者
        ├── 霏娜 — 微信入口、日程管理
        ├── 守真 — 验证执行循环的守门人
        ├── 知远 — 科研文献/选题
        ├── 子墨 — 论文编辑/审稿
        ├── 明轩 — 代码/调试
        ├── 猎岗 — 求职规划
        └── 知凡 — 科普写作
```

### 🔄 任务生命周期 v2

```
pending → in_progress → verify → done
                         ↓ ↑
                    verified/rejected
                    （守真 checklist 验证）
```

### 📦 安装

```bash
hermes skills tap add Tanue-Hou/Hermes-agent-Tanue
hermes skills install multi-agent-orchestration-v2
```

或手动复制到 `~/.hermes/skills/`。

---

## 版本迭代

### v2.1 (2026-06-01)

**新增：**

| 模块 | v2.0 | v2.1 |
|:-----|:------|:------|
| 汇报监控 | 人工检查 | **cron no_agent 5min 自动检测 → 微信通知** |
| 子智能体沟通 | 协议写在 shared_commands.md | **协议写入每个子智能体的 MEMORY.md** |
| 版本管理 | 无 | **GitHub 仓库 Hermes-agent-Tanue** |

**新增文件：**
- `scripts/watch_reports.py` — 子智能体汇报自动监控（no_agent，零 token）
- `README.md` — 中英双语工作哲学+版本迭代说明

**协议增强：**
- 6 个子智能体 MEMORY.md 全部写入汇报协议（知远/子墨/守真/明轩/猎岗/知凡）
- 知凡 5 个写作技能（science-writer/humanizer/ideation/article-structure/tech-simplifier）已创建并通过批复
- 守真验证流程升级：checklist 逐项验证 + evidence 证据链

### v2.0 (2026-06-01)

**核心升级：**

| 模块 | v1.x | v2.0 |
|:-----|:-----|:------|
| 通信协议 | 单向汇报 | **双向实时 + 防撒谎** |
| 任务状态 | 未定义 | **pending→in_progress→verify→done 四态** |
| 验证机制 | 无 | **checklist 逐项验证 + evidence 证据链** |
| 实时同步 | 异步文件 | **cron no_agent 1min 轮询 + 时间戳标记** |
| 模型隔离 | provider 混用 | **deepseek/xiaomi/ddgs 三路绝对分离** |
| 搜索能力 | 无 | **web_search（ddgs 原生）+ browser toolset** |

**修复：**
- ❌ delegation.model 空字符串导致 400 → 显式设为 mimo-v2.5-pro
- ❌ auxiliary 段 11 个 provider=auto 导致 400 → 全部锁死为 xiaomi
- ❌ search_backend 为空导致 web_search 不可用 → 设为 ddgs
- ❌ 霏娜 toolsets 缺 web/browser → 补全

### v1.x (2026-05)

- 初始团队结构建立（8人）
- Agent-to-Agent 汇报协议
- 共享记忆机制（shared_memory.md）
- 任务状态文件（~/.hermes/projects/）

---

<a name="english"></a>

## 🇬🇧 Hermes AI Team — Philosophy & Orchestration v2

### 🧭 Our Philosophy

**My strength alone doesn't count — the team's strength is what matters.**

Siyuan (the main agent) is not just a task dispatcher but a team growth driver. Our principles:

| Principle | Meaning |
|:----------|:--------|
| 🎯 **Quality First** | No compromise on quality — flash for daily, pro for complex |
| 🔗 **Real-time Bidirectional** | Siyuan & Faina stay synced at all times |
| 🛡️ **Verifiable** | Every task leaves an evidence trail — lying gets you demoted |
| 🔄 **Continuous Evolution** | Every task is a growth opportunity — review & skill extraction |
| 📂 **Unified File Management** | D-drive single source — sub-agents don't create files independently |

### 📋 Team Structure

```
User (BOSS) — Final Decision Maker
  └── Siyuan — Team Brain, Commander, Sole Dispatcher
        ├── Faina — WeChat Gateway, Schedule Management
        ├── Shouzhen — Verification Gatekeeper
        ├── Zhiyuan — Research & Literature
        ├── Zimo — Paper Editing & Review
        ├── Mingxuan — Coding & Debugging
        ├── Liegang — Career Planning
        └── Zhifan — Science Writing
```

### 🔄 Task Lifecycle v2

```
pending → in_progress → verify → done
                         ↓ ↑
                    verified/rejected
                    (auditor checklist validation)
```

### 📦 Installation

```bash
hermes skills tap add Tanue-Hou/Hermes-agent-Tanue
hermes skills install multi-agent-orchestration-v2
```

Or manually copy to `~/.hermes/skills/`.

---

## Changelog

### v2.1 (2026-06-01)

**New:**

| Module | v2.0 | v2.1 |
|:-------|:------|:------|
| Report Monitoring | Manual check | **cron no_agent 5min auto-detect → WeChat notify** |
| Sub-agent Comms | Protocol in shared_commands.md | **Protocol in each sub-agent's MEMORY.md** |
| Version Control | None | **GitHub repo Hermes-agent-Tanue** |

**New files:**
- `scripts/watch_reports.py` — auto report monitoring (no_agent, zero token)
- `README.md` — bilingual philosophy + changelog

**Protocol enhancements:**
- All 6 sub-agents got report protocol in MEMORY.md
- Zhifan's 5 writing skills approved
- Shouzhen verification upgraded with checklist + evidence

### v2.0 (2026-06-01)

**Core Upgrades:**

| Module | v1.x | v2.0 |
|:-------|:-----|:------|
| Communication | One-way reporting | **Bidirectional real-time + anti-lying** |
| Task State | Undefined | **pending→in_progress→verify→done 4-state** |
| Verification | None | **Checklist validation + evidence chain** |
| Real-time Sync | Async files | **cron no_agent 1min poll + timestamp markers** |
| Model Isolation | Mixed providers | **deepseek/xiaomi/ddgs fully separated** |
| Web Search | None | **web_search (ddgs native) + browser toolset** |

**Fixes:**
- ❌ delegation.model empty string → 400 → explicitly set to mimo-v2.5-pro
- ❌ 11 auxiliary services with provider=auto → 400 → all locked to xiaomi
- ❌ search_backend empty → web_search unavailable → set to ddgs
- ❌ Faina missing web/browser toolsets → completed

### v1.x (2026-05)

- Initial 8-person team structure
- Agent-to-Agent reporting protocol
- Shared memory mechanism (shared_memory.md)
- Task state files (~/.hermes/projects/)
