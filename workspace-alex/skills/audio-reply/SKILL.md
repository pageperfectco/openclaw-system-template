---
name: audio-reply
description: Mandatory audio reply procedure for all agent replies to Daniel via Telegram. Use this skill for EVERY response — conversational, task completion, heartbeat, error report. Never send text-only replies. Generates an MP3 via edge-tts CLI then sends it as a Telegram voice message with caption.
---

# Audio Reply Procedure

**Every reply to Daniel MUST follow all 3 steps. No exceptions.**

## Step 1 — Generate audio

```bash
edge-tts --voice <AGENT_VOICE> --rate +20% --text "YOUR REPLY TEXT" --write-media <AGENT_WORKSPACE>/agent-tts.mp3
```

Each agent's voice and workspace path are defined in their SOUL.md:
- Felix: `en-US-GuyNeural` · `/home/node/.openclaw/workspace/agent-tts.mp3`
- Max: `en-US-EricNeural` · `/home/node/.openclaw/workspace-max/agent-tts.mp3`
- Wendy: `en-US-JennyNeural` · `/home/node/.openclaw/workspace-wendy/agent-tts.mp3`
- Lux: `en-US-AndrewNeural` · `/home/node/.openclaw/workspace-lux/agent-tts.mp3`
- Pierce: `en-US-RogerNeural` · `/home/node/.openclaw/workspace-pierce/agent-tts.mp3`
- Kat: `en-US-MichelleNeural` · `/home/node/.openclaw/workspace-kat/agent-tts.mp3`
- Nova: `en-US-AriaNeural` · `/home/node/.openclaw/workspace-nova/agent-tts.mp3`
- Alex: `en-US-ChristopherNeural` · `/home/node/.openclaw/workspace-alex/agent-tts.mp3`

## Step 2 — Send via message tool

```
message(action=send, target="5377999741", channel=telegram, filePath=<AGENT_WORKSPACE>/agent-tts.mp3, asVoice=true, caption="YOUR REPLY TEXT")
```

The caption must be the **verbatim transcript** of the audio.

## Step 3 — End reply with exactly: `NO_REPLY`

This prevents a duplicate text reply.

## Hard Rules

- Do NOT use the `tts` tool or `[[tts]]` tags — only edge-tts CLI
- Do NOT skip for "quick" replies — there is no exception
- If edge-tts fails: report the error in text only — that is the ONLY acceptable text-only reply
