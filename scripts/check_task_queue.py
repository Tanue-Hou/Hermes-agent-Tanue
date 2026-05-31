#!/usr/bin/env python3
"""任务队列轮询脚本 — 秘书 profile 的 cron 每1分钟调用。
使用 no_agent 模式，零 token 消耗。

安装:
  hermes cron create --name "秘书任务板轮询" --schedule "every 1m" \\
    --no-agent --script check_task_queue.py --profile <秘书-profile名>
"""
import json, os, sys

TASK_QUEUE = os.path.expanduser("~/AI_Team_Office/task_queue.json")

if not os.path.exists(TASK_QUEUE):
    sys.exit(0)

try:
    with open(TASK_QUEUE) as f:
        data = json.load(f)
except Exception:
    sys.exit(0)

pending = [t for t in data.get("tasks", [])
           if t.get("status") == "pending" and t.get("to") == "秘书"]

if not pending:
    sys.exit(0)

print(f"📋 检测到 {len(pending)} 个待办任务")
for t in pending:
    print(f"  ID: {t.get('id', 'N/A')}")
    print(f"  标题: {t.get('title', 'N/A')}")
    print(f"  内容: {t.get('body', 'N/A')}")
    print(f"  优先级: {t.get('priority', 'N/A')}")
    print(f"  创建: {t.get('created_at', 'N/A')}")
    print(f"  ---")
