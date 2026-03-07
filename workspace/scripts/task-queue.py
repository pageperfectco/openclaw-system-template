#!/usr/bin/env python3
"""
Felix Task Queue — manage pending tasks for agent delivery.

Usage:
  task-queue.py add --agent lux --task "Do X" [--after "lux:prd"]
  task-queue.py list
  task-queue.py ready           # show tasks with no unmet dependencies
  task-queue.py complete <id>   # mark task done
  task-queue.py cancel <id>     # remove task
"""

import json, sys, argparse, uuid
from datetime import datetime, timezone
from pathlib import Path

QUEUE_FILE = Path.home() / '.openclaw/workspace/task-queue.json'

def load():
    return json.loads(QUEUE_FILE.read_text())

def save(data):
    QUEUE_FILE.write_text(json.dumps(data, indent=2))

def add(agent, task, after=None, note=None):
    data = load()
    t = {
        'id': str(uuid.uuid4())[:8],
        'agent': agent,
        'task': task,
        'status': 'pending',
        'queued_at': datetime.now(timezone.utc).isoformat(),
        'after': after,   # dependency label e.g. "lux:prd"
        'note': note
    }
    data['tasks'].append(t)
    save(data)
    print(f"Queued [{t['id']}] for {agent}: {task[:60]}")
    return t

def list_tasks():
    data = load()
    tasks = data['tasks']
    if not tasks:
        print("Queue is empty.")
        return
    for t in tasks:
        dep = f" [after: {t['after']}]" if t.get('after') else ''
        print(f"[{t['id']}] {t['status']:10} → {t['agent']:10} | {t['task'][:60]}{dep}")

def ready():
    """Tasks with no unmet dependencies (after=None or after dependency is done)."""
    data = load()
    done_labels = {t.get('after_label') for t in data['tasks'] if t['status'] == 'done'}
    result = []
    for t in data['tasks']:
        if t['status'] != 'pending':
            continue
        if not t.get('after') or t['after'] in done_labels:
            result.append(t)
    return result

def complete(task_id):
    data = load()
    for t in data['tasks']:
        if t['id'] == task_id:
            t['status'] = 'done'
            t['completed_at'] = datetime.now(timezone.utc).isoformat()
            save(data)
            print(f"Marked [{task_id}] done.")
            return
    print(f"Task {task_id} not found.")

def cancel(task_id):
    data = load()
    data['tasks'] = [t for t in data['tasks'] if t['id'] != task_id]
    save(data)
    print(f"Cancelled [{task_id}].")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='cmd')

    a = sub.add_parser('add')
    a.add_argument('--agent', required=True)
    a.add_argument('--task', required=True)
    a.add_argument('--after', default=None)
    a.add_argument('--note', default=None)

    sub.add_parser('list')
    sub.add_parser('ready')

    c = sub.add_parser('complete')
    c.add_argument('id')

    x = sub.add_parser('cancel')
    x.add_argument('id')

    args = parser.parse_args()

    if args.cmd == 'add':
        add(args.agent, args.task, args.after, args.note)
    elif args.cmd == 'list':
        list_tasks()
    elif args.cmd == 'ready':
        tasks = ready()
        if not tasks:
            print("No ready tasks.")
        for t in tasks:
            print(f"[{t['id']}] → {t['agent']}: {t['task'][:80]}")
    elif args.cmd == 'complete':
        complete(args.id)
    elif args.cmd == 'cancel':
        cancel(args.id)
    else:
        parser.print_help()
