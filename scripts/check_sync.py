#!/usr/bin/env python3
"""shared_memory.md 同步检查脚本 — 检测秘书是否有新更新时间戳。
使用 no_agent 模式，零 token 消耗。

安装:
  hermes cron create --name "同步检查" --schedule "every 10m" \\
    --no-agent --script check_sync.py
"""
import os, re, sys

MEMORY_FILE = os.path.expanduser("~/AI_Team_Office/shared_memory.md")
STATE_FILE = os.path.expanduser("~/.hermes/scripts/sync_last_check.txt")

if not os.path.exists(MEMORY_FILE):
    sys.exit(0)

with open(MEMORY_FILE) as f:
    content = f.read()

matches = re.findall(r'<!-- 秘书更新 @ (.+?) -->', content)
if not matches:
    sys.exit(0)

latest = matches[-1].strip()

last_checked = ""
if os.path.exists(STATE_FILE):
    with open(STATE_FILE) as f:
        last_checked = f.read().strip()

if latest == last_checked:
    sys.exit(0)

with open(STATE_FILE, 'w') as f:
    f.write(latest)

print(f"【同步】检测到秘书新更新 @ {latest}")
log_section = re.search(r'\| 时间.*?\|(.*?)<!--', content, re.DOTALL)
if log_section:
    log_lines = log_section.group(1).strip().split('\n')
    recent = [l.strip() for l in log_lines if l.strip()][-3:]
    for line in recent:
        print(f"  {line}")
