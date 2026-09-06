# -*- coding: utf-8 -*-
"""
全钒液流电池研学内容 — 自动 Git 同步脚本
每次运行：将 days/ 下所有 .md 变动 add → commit → push
"""
import subprocess
import os
import sys
from datetime import datetime

REPO = r"C:\Users\Administrator\.qclaw\workspace\vrb-study"
SSH_KEY = r"C:\Users\Administrator\.ssh\id_ed25519_github"

env = os.environ.copy()
env["GIT_SSH_COMMAND"] = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no'

today = datetime.now().strftime("%Y-%m-%d")

def run(cmd, **kwargs):
    r = subprocess.run(cmd, cwd=REPO, env=env,
                      capture_output=True, text=True,
                      encoding='utf-8', errors='replace', **kwargs)
    return r.returncode, r.stdout, r.stderr

# 1. 检查是否有变化
rc, out, err = run(["git", "status", "--porcelain"])
if rc != 0:
    print(f"git status 失败: {err}")
    sys.exit(1)

if not out.strip():
    print(f"[{today}] 今日无变化，跳过提交")
    sys.exit(0)

# 2. Add 所有变更
rc, out, err = run(["git", "add", "."])
if rc != 0:
    print(f"git add 失败: {err}")
    sys.exit(1)

# 3. Commit，消息含日期
msg = f"每日研学更新 {today}"
rc, out, err = run(["git", "commit", "-m", msg])
if rc != 0:
    print(f"git commit 失败: {err}")
    sys.exit(1)

# 4. Push
rc, out, err = run(["git", "push", "origin", "master"])
if rc != 0:
    print(f"git push 失败: {err}")
    sys.exit(1)

print(f"[{today}] 同步完成 → GitHub")
print(out)
