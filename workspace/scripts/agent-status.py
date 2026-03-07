#!/usr/bin/env python3
"""
Agent status tracker. Felix updates this when dispatching/completing tasks.
Used to auto-queue tasks when target agent is busy.

Usage:
  agent-status.py set <agent> busy "task description"
  agent-status.py set <agent> idle
  agent-status.py show [agent]
  agent-status.py is-busy <agent>   # exits 0 if busy, 1 if idle
"""

import json, sys
from datetime import datetime, timezone
from pathlib import Path

STATUS_FILE = Path.home() / '.openclaw/workspace/agent-status.json'

def load():
    return json.loads(STATUS_FILE.read_text())

def save(data):
    STATUS_FILE.write_text(json.dumps(data, indent=2))

def set_status(agent, status, task=None):
    data = load()
    data['agents'][agent] = {
        'status': status,
        'task': task,
        'since': datetime.now(timezone.utc).isoformat() if status == 'busy' else None
    }
    save(data)
    if status == 'busy':
        print(f"{agent} → busy: {task}")
    else:
        print(f"{agent} → idle")

def show(agent=None):
    data = load()
    agents = {agent: data['agents'][agent]} if agent else data['agents']
    for name, info in agents.items():
        status = info['status']
        task = f": {info['task']}" if info.get('task') else ''
        since = f" (since {info['since'][:16]})" if info.get('since') else ''
        print(f"{name:10} {status:6}{task}{since}")

def is_busy(agent):
    data = load()
    info = data['agents'].get(agent, {})
    return info.get('status') == 'busy'

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        show()
    elif args[0] == 'set' and len(args) >= 3:
        agent, status = args[1], args[2]
        task = args[3] if len(args) > 3 else None
        set_status(agent, status, task)
    elif args[0] == 'show':
        show(args[1] if len(args) > 1 else None)
    elif args[0] == 'is-busy':
        busy = is_busy(args[1])
        print('busy' if busy else 'idle')
        sys.exit(0 if busy else 1)
    else:
        print(__doc__)
