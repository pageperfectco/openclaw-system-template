#!/bin/bash
# backup-workspaces.sh — Sync all agent workspaces to the backup repo and push.
# Run from Felix heartbeat or manually.
#
# Setup: Create a private GitHub repo and clone it to ~/.openclaw/workspaces-backup
#   gh repo create openclaw-workspaces-backup --private
#   git clone https://github.com/[your-username]/openclaw-workspaces-backup ~/.openclaw/workspaces-backup

BACKUP_DIR="$HOME/.openclaw/workspaces-backup"
WORKSPACES=(workspace workspace-dev workspace-kat workspace-alex workspace-pierce)

# Skip if backup dir isn't initialized yet
if [ ! -d "$BACKUP_DIR/.git" ]; then
  echo "Backup dir not initialized. Skipping. Run INSTALL.md Step 6 to set up."
  exit 0
fi

# Sync each workspace (excluding .env, secrets, and build artifacts)
for ws in "${WORKSPACES[@]}"; do
  SRC="$HOME/.openclaw/$ws/"
  DEST="$BACKUP_DIR/$ws/"
  if [ -d "$SRC" ]; then
    mkdir -p "$DEST"
    rsync -a --delete \
      --exclude='.env' \
      --exclude='*.env' \
      --exclude='.env.*' \
      --exclude='node_modules/' \
      --exclude='__pycache__/' \
      --exclude='*.pyc' \
      --exclude='.next/' \
      --exclude='dist/' \
      --exclude='build/' \
      --exclude='.git/' \
      --exclude='*.jpg' \
      --exclude='*.png' \
      --exclude='*.jpeg' \
      --exclude='*.mp3' \
      --exclude='*.mp4' \
      "$SRC" "$DEST"
  fi
done

# Commit and push
cd "$BACKUP_DIR"
git add -A

if git diff --cached --quiet; then
  echo "No changes to backup."
else
  TIMESTAMP=$(date -u '+%Y-%m-%d %H:%M UTC')
  git commit -m "backup: $TIMESTAMP"
  git push origin main && echo "Backup pushed: $TIMESTAMP" || echo "Push failed — check remote"
fi
