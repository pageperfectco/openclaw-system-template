---
name: web-automation-protocol
description: Protocol for when and how agents should use Unbrowse, the mobile proxy, 2Captcha, and browser automation. Mandatory reading before any web interaction that goes beyond simple API calls or web_fetch.
metadata:
  openclaw:
    emoji: 🌐
---

# Web Automation Protocol

**This protocol governs all agent use of web tools: Unbrowse, browser, mobile proxy, and CAPTCHA solving.**

## Decision Tree — Which Tool to Use

```
Need web data?
├── Is there a direct API? (GitHub, Stripe, Supabase, etc.)
│   └── YES → Use the API. Stop here.
│
├── Is it a simple page fetch? (public content, no JS required)
│   └── YES → Use `web_fetch`. No proxy needed.
│
├── Does the site need JS rendering OR you need structured data extraction?
│   └── YES → Use `unbrowse` (resolve action).
│       ├── Unbrowse discovers API endpoints? → Use them directly. Done.
│       └── Unbrowse falls back to DOM extraction? → Still fine, use the results.
│           └── Unbrowse fails entirely? → Fall back to `browser` tool.
│
├── Need pixel-level UI interaction? (drag/drop, canvas, visual QA, screenshots)
│   └── YES → Use OpenClaw `browser` tool ALWAYS WITH mobile proxy (unlimited plan).
│       └── CAPTCHA appears? → Use `solve-captcha` CLI.
│
└── Need to log in to a site for the first time?
    └── Use `unbrowse login --url <site>` to bootstrap auth.
        └── Then use `unbrowse resolve/execute` for ongoing data access.
```

## Tool Priority (highest to lowest)
1. **Direct API** — Always prefer if available
2. **`web_fetch`** — Simple public page content
3. **`unbrowse`** — Structured data extraction, API discovery, authenticated reads
4. **`browser` tool + proxy** — All browser interactions (proxy is unlimited, always on)
5. **`browser` + proxy + `solve-captcha`** — Sites with CAPTCHAs

## Unbrowse — Primary Web Tool

Unbrowse reverse-engineers site APIs from browser traffic. Instead of clicking through pages, it discovers API endpoints and calls them directly — 100x faster than browser automation.

### When to Use Unbrowse
- "Get data from a site"
- "Search this site"
- "Extract listings / posts / products / profiles / prices"
- "Find the API behind this page"
- "Use my logged-in session if possible"
- Any structured data extraction task

### When NOT to Use Unbrowse (use browser instead)
- Visual QA / screenshots / pixel inspection
- Drag/drop interactions
- Canvas-heavy apps
- File upload/download flows
- Pure login flows where no API exists

### Unbrowse Call Patterns

**Discover + extract data from a site:**
```json
{
  "action": "resolve",
  "intent": "describe the task in plain English",
  "url": "https://target-site.example"
}
```

**Search for existing skills (pre-discovered API patterns):**
```json
{
  "action": "search",
  "intent": "what you're looking for"
}
```

**Execute a known skill endpoint:**
```json
{
  "action": "execute",
  "skillId": "skill_id_from_resolve",
  "endpointId": "endpoint_id_from_resolve"
}
```

**Bootstrap auth for a site:**
```json
{
  "action": "login",
  "url": "https://target-site.example"
}
```

**Check health:**
```json
{
  "action": "health"
}
```

### Unbrowse Notes
- First-time site capture takes 20-80 seconds (API discovery). Subsequent calls are fast.
- Always use `dryRun: true` before unsafe mutations.
- Use `confirmUnsafe: true` only with explicit user consent.
- If Unbrowse returns structured data, stay in Unbrowse — don't switch to browser.

## Mobile Proxy — Default ON for All Browser Automation

**The Litport proxy is an unlimited plan. Default to always using it for any browser interaction.**

### ✅ ALWAYS USE PROXY for:
- All `browser` tool usage — no exceptions
- Any curl/requests call to third-party sites
- Account creation, login flows
- Social media, e-commerce, any bot-protected site
- Even "friendly" sites — residential IP is cleaner than datacenter IP

### ❌ DO NOT USE PROXY for:
- Internal APIs (Supabase, Vercel, Stripe, GitHub)
- `web_fetch` of public documentation or blogs
- `unbrowse` calls (Unbrowse manages its own browser traffic)
- Our own sites (verilux.vercel.app, msc-inventory.vercel.app, etc.)
- AgentMail, Composio, or other tool APIs
- localhost or internal network requests

### How to Use the Proxy

**Environment variable (for curl, Python requests, etc.):**
```bash
source ~/.config/litport/proxy.conf
curl -x $PROXY_URL https://target-site.com
```

**Python requests:**
```python
import os
proxy_url = open(os.path.expanduser('~/.config/litport/proxy.conf')).read()
for line in proxy_url.split('\n'):
    if line.startswith('PROXY_URL='):
        proxy = line.split('=', 1)[1]
proxies = {'http': proxy, 'https': proxy}
response = requests.get('https://target-site.com', proxies=proxies)
```

**OpenClaw browser tool with proxy:** Launch Chrome with proxy flags:
```bash
chromium --proxy-server="http://hub-us-7.litport.net:1337"
```

## When to Use 2Captcha

### ✅ USE 2CAPTCHA for:
- reCAPTCHA v2/v3 challenges during legitimate workflows
- hCaptcha on sites you have permission to access
- Cloudflare Turnstile challenges
- Image CAPTCHAs blocking agent access

### ❌ DO NOT USE 2CAPTCHA for:
- Bypassing access controls on unauthorized sites
- Mass account creation on platforms that prohibit it
- Scraping sites that explicitly block automated access (check ToS)
- Testing — use 2Captcha's sandbox mode instead

### How to Use 2Captcha

```bash
# Image CAPTCHA
solve-captcha image captcha.png

# reCAPTCHA v2
TOKEN=$(solve-captcha -q recaptcha2 -s SITEKEY -u https://target-site.com)

# Cloudflare Turnstile
TOKEN=$(solve-captcha -q turnstile -s SITEKEY -u https://target-site.com)

# Check balance
solve-captcha balance
```

API key is pre-configured at `~/.config/2captcha/api-key`. No setup needed.

## Budget Rules

- **2Captcha balance check:** Run `solve-captcha balance` before any batch operation
- **Alert threshold:** If balance drops below $10, notify Felix immediately
- **Per-session limit:** No agent should solve more than 50 CAPTCHAs in a single session without Felix approval
- **Cost awareness:** Image CAPTCHAs ~$0.001, reCAPTCHA ~$0.003, Turnstile ~$0.003

## Proxy Rules

- **Shared resource:** One connection at a time gets best performance.
- **Don't abuse:** Keep requests reasonable. No bulk scraping hundreds of pages per minute.
- **IP rotation:** Auto-rotates every 2 min to 12 hours. Don't force-rotate unless blocked.
- **Speed limit:** 5 Mbps max, 100 threads.
- **If blocked:** Wait 5 minutes for IP rotation, then retry. Don't hammer the target.

## Logging Requirements

Every use of proxy, 2Captcha, or Unbrowse for sensitive operations MUST be logged in daily notes:
```
- [HH:MM] Used unbrowse resolve on [site] — discovered [N] endpoints
- [HH:MM] Used mobile proxy for [site] — [reason]
- [HH:MM] Solved [type] CAPTCHA on [site] — cost: $X.XXX
```

## Escalation

- **Unbrowse fails?** → Fall back to browser tool. Log the failure.
- **Proxy not working?** → Check if Litport subscription is active. Notify Felix.
- **2Captcha balance low?** → Notify Felix immediately.
- **Blocked even with proxy?** → Stop. Report to Felix. Do not retry more than 3 times.
- **Unsure if a site allows automation?** → Ask Felix before proceeding.
