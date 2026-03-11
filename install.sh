#!/usr/bin/env bash
# OpenClaw System Template — Quick Installer
# Usage: bash <(curl -fsSL https://raw.githubusercontent.com/pageperfectco/openclaw-system-template/main/install.sh)

set -e

REPO="https://github.com/pageperfectco/openclaw-system-template.git"
TMP_DIR="/tmp/openclaw-system-template-install"
OPENCLAW_DIR="$HOME/.openclaw"
CONFIG_FILE="$OPENCLAW_DIR/openclaw.json"

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║   OpenClaw System Template — Quick Install   ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# ── 1. Check OpenClaw is installed ─────────────────────────────────────────
if ! command -v openclaw &>/dev/null; then
  echo "❌  OpenClaw not found. Install it first:"
  echo ""
  echo "    npm install -g openclaw"
  echo ""
  exit 1
fi
echo "✅  OpenClaw found: $(openclaw --version 2>/dev/null || echo 'installed')"

# ── 2. Clone the template repo ─────────────────────────────────────────────
echo ""
echo "📦  Cloning template repo..."
rm -rf "$TMP_DIR"
git clone --depth=1 "$REPO" "$TMP_DIR" 2>&1 | grep -v "^hint"

# ── 3. Copy workspace folders ──────────────────────────────────────────────
echo ""
echo "📂  Copying workspace files..."

WORKSPACES=(workspace workspace-dev workspace-kat workspace-alex workspace-pierce workspace-silas)

for ws in "${WORKSPACES[@]}"; do
  SRC="$TMP_DIR/$ws"
  DEST="$OPENCLAW_DIR/$ws"
  if [ -d "$DEST" ]; then
    echo "   ⚠️  $ws already exists — merging (existing files preserved)..."
    cp -rn "$SRC/." "$DEST/"  # -n = no-clobber: won't overwrite existing files
  else
    echo "   ✅  Installing $ws..."
    cp -r "$SRC" "$DEST"
  fi
done

# ── 4. Patch openclaw.json — add skipBootstrap ────────────────────────────
echo ""
echo "⚙️   Updating openclaw.json..."

mkdir -p "$OPENCLAW_DIR"

if [ ! -f "$CONFIG_FILE" ]; then
  echo '{}' > "$CONFIG_FILE"
fi

# Use node to safely merge the skipBootstrap flag (openclaw requires node anyway)
node -e "
const fs = require('fs');
const path = '$CONFIG_FILE';
let raw = fs.readFileSync(path, 'utf8').trim() || '{}';
// Strip JS-style comments for basic JSON5 compat
raw = raw.replace(/\/\/[^\n]*/g, '').replace(/\/\*[\s\S]*?\*\//g, '');
let cfg = {};
try { cfg = JSON.parse(raw); } catch(e) { console.error('Could not parse openclaw.json — skipping patch. Edit manually.'); process.exit(0); }
if (!cfg.agent) cfg.agent = {};
cfg.agent.skipBootstrap = true;
fs.writeFileSync(path, JSON.stringify(cfg, null, 2));
console.log('   ✅  skipBootstrap: true added to agent config');
"

# ── 5. Cleanup ─────────────────────────────────────────────────────────────
rm -rf "$TMP_DIR"

# ── 6. Done ────────────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅  Workspace files installed."
echo ""
echo "👉  Next steps:"
echo "    1. Open ~/.openclaw/openclaw.json and configure your agents, model keys, and channels"
echo "    2. Read INSTALL.md for the full setup guide (Steps 2–14):"
echo "       cat ~/.openclaw/workspace/INSTALL.md | less"
echo "    3. Restart the gateway:"
echo "       openclaw gateway restart"
echo "    4. Message Felix: \"Start your bootstrap sequence.\""
echo ""
echo "🔗  Full guide: https://github.com/pageperfectco/openclaw-system-template/blob/main/INSTALL.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
