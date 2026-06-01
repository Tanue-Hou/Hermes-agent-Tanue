#!/usr/bin/env python3
"""监控 reports/ 目录的新汇报文件。no_agent 模式，零 token 消耗。
发现新汇报时输出通知，通过 cron deliver 推送给霏娜/侯总。

用法: python3 watch_reports.py
状态文件: ~/.hermes/scripts/reports_last_check.txt
"""
import os, json, time, re

REPORTS_DIR = os.path.expanduser("~/AI_Team_Office/reports")
STATE_FILE = os.path.expanduser("~/.hermes/scripts/reports_last_check.txt")

SKIP_PREFIXES = ("responses", "思远通知", "思远给")
SKIP_SUFFIXES = ("_response.md",)

def get_report_files():
    """获取 reports/ 下所有汇报文件（排除 responses 目录和思远的通知）"""
    if not os.path.isdir(REPORTS_DIR):
        return []
    files = []
    for f in os.listdir(REPORTS_DIR):
        fpath = os.path.join(REPORTS_DIR, f)
        if not os.path.isfile(fpath):
            continue
        # 跳过非汇报文件
        if any(f.startswith(p) for p in SKIP_PREFIXES):
            continue
        if any(f.endswith(s) for s in SKIP_SUFFIXES):
            continue
        files.append((f, os.path.getmtime(fpath), fpath))
    return sorted(files, key=lambda x: x[1])  # 按修改时间排序

def main():
    reports = get_report_files()
    if not reports:
        return  # 无汇报文件，静默退出

    # 读取上次检查时间
    last_check = 0.0
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                last_check = float(f.read().strip())
        except (ValueError, OSError):
            pass

    # 找出上次检查后的新汇报
    new_reports = [r for r in reports if r[1] > last_check]

    if not new_reports:
        return  # 无新汇报，静默退出

    # 更新状态文件
    now = time.time()
    with open(STATE_FILE, 'w') as f:
        f.write(str(now))

    # 输出通知
    print(f"📬 检测到 {len(new_reports)} 份新汇报")
    print(f"---")
    for fname, mtime, fpath in new_reports:
        # 读取汇报文件前5行获取摘要
        summary = ""
        try:
            with open(fpath) as f:
                lines = f.readlines()
                for line in lines[:8]:
                    stripped = line.strip()
                    if stripped and not stripped.startswith("#") and not stripped.startswith("---"):
                        summary += stripped[:80] + " "
                        if len(summary) > 120:
                            break
        except:
            pass
        
        mtime_str = time.strftime("%m-%d %H:%M", time.localtime(mtime))
        print(f"  📄 {fname}")
        print(f"    时间: {mtime_str}")
        print(f"    摘要: {summary[:150] if summary else '(无)'}")
        print(f"  ---")

    print(f"请侯总查看或霏娜通知侯总。思远将在下次活跃时处理。")

if __name__ == "__main__":
    main()
