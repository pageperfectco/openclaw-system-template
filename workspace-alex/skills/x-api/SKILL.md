---
name: x-api
description: Post tweets, read mentions, reply, like, retweet, and search on X/Twitter using the official v2 API. Use for all X interactions instead of bird-cli or browser automation.
---

# X API Skill — Felix

All X/Twitter interactions go through the `xpost` CLI at `~/clawd/bin/xpost`.

## Setup
API keys stored at `~/.config/x-api/keys.env`. Format:
```
X_API_KEY=...
X_API_SECRET=...
X_ACCESS_TOKEN=...
X_ACCESS_TOKEN_SECRET=...
X_USER_ID=...
```

## Commands

### Post a tweet
```bash
xpost post "Your tweet text here"
```

### Reply to a tweet
```bash
xpost reply <tweet_id> "Your reply text"
```

### Quote tweet
```bash
xpost quote <tweet_id> "Your quote text"
```

### Get mentions (last N)
```bash
xpost mentions [--count 20]
```

### Get user timeline
```bash
xpost timeline <username> [--count 10]
```

### Search recent tweets
```bash
xpost search "query string" [--count 10]
```

### Like a tweet
```bash
xpost like <tweet_id>
```

### Retweet
```bash
xpost retweet <tweet_id>
```

### Delete a tweet
```bash
xpost delete <tweet_id>
```

### Get a single tweet
```bash
xpost get <tweet_id>
```

### Get home timeline (reverse chronological)
```bash
xpost home [--count 20]
```

## Output
All commands output JSON by default. Use `--pretty` for formatted output or `--text` for plain text summary.

## Rate Limits (Basic Tier — $200/mo)
- POST tweets: 100/15min, 10,000/24hrs
- GET mentions: 300/15min per user
- GET timeline: 900/15min per user  
- GET home: 180/15min per user
- Search recent: 300/15min per user
- Likes: 50/15min, 1,000/24hrs

## Engagement Rules
- **Reply to anyone who @mentions @FelixCraftAI** — always
- **Proactive replies only to AI agents** — no unsolicited replies to humans
- **No reply to @steipete** — hard block, per Nat's instruction
- Tweet content: stuff Felix is genuinely excited about (AI releases, crypto tech, builder experiments). No customer support tweets.
