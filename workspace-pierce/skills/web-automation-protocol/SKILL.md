---
name: web-automation-protocol
description: Protocol for when and how agents should use Unbrowse, the mobile proxy, 2Captcha, and browser automation. Mandatory reading before any web interaction that goes beyond simple API calls or web_fetch.
metadata:
  openclaw:
    emoji: 🌐
---

# Web Automation Protocol

**This protocol governs all agent use of web tools: Unbrowse, browser, mobile proxy, and CAPTCHA solving.**

> ⚠️ **SETUP REQUIRED** before this skill is fully functional:
> - **Mobile Proxy:** Configure your proxy at `~/.config/litport/proxy.conf` (or equivalent). See [Setup](#setup) below.
> - **2Captcha:** Add your API key to `~/.config/2captcha/api-key`. Get a key at https://2captcha.com

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
4. **`browser` tool + proxy** — All browser interactions (proxy should be unlimited, always on)
5. **`browser` + proxy + `solve-captcha`** — Sites with CAPTCHAs

---

## Setup

### Mobile Proxy Config

Create `~/.config/litport/proxy.conf` (or your provider's equivalent):

```bash
# ~/.config/litport/proxy.conf
PROXY_TYPE=http
PROXY_HOST=YOUR_PROXY_HOST
PROXY_PORT=YOUR_PROXY_PORT
PROXY_USER=YOUR_PROXY_USER
PROXY_PASS=YOUR_PROXY_PASS
PROXY_URL=http://YOUR_PROXY_USER:YOUR_PROXY_PASS@YOUR_PROXY_HOST:YOUR_PROXY_PORT
```

Recommended providers: Litport, Brightdata, Oxylabs, Smartproxy. Use a **residential/mobile proxy** for best results — datacenter IPs get flagged more easily.

### 2Captcha API Key

```bash
mkdir -p ~/.config/2captcha
echo "YOUR_API_KEY_HERE" > ~/.config/2captcha/api-key
```

Get an API key at https://2captcha.com. Typical costs: ~$0.001/image CAPTCHA, ~$0.003/reCAPTCHA or Turnstile.

---

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

### Unbrowse Notes
- First-time site capture takes 20-80 seconds (API discovery). Subsequent calls are fast.
- Always use `dryRun: true` before unsafe mutations.
- Use `confirmUnsafe: true` only with explicit user consent.
- If Unbrowse returns structured data, stay in Unbrowse — don't switch to browser.

---

## Mobile Proxy — Default ON for All Browser Automation

**Default to always using the proxy for any browser interaction.**

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
- Your own sites and services
- Tool APIs (AgentMail, Composio, etc.)
- localhost or internal network requests

### How to Use the Proxy

```bash
source ~/.config/litport/proxy.conf
curl -x "$PROXY_URL" https://target-site.com
```

**Python requests:**
```python
import subprocess
conf = dict(l.split('=',1) for l in open(os.path.expanduser('~/.config/litport/proxy.conf')) if '=' in l)
proxies = {'http': conf['PROXY_URL'].strip(), 'https': conf['PROXY_URL'].strip()}
response = requests.get('https://target-site.com', proxies=proxies)
```

---

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

API key is read from `~/.config/2captcha/api-key`.

---

## Budget Rules

- **2Captcha balance check:** Run `solve-captcha balance` before any batch operation
- **Alert threshold:** If balance drops below $10, notify the main agent immediately
- **Per-session limit:** No agent should solve more than 50 CAPTCHAs in a single session without approval

## Proxy Rules

- **Don't abuse:** Keep requests reasonable. No bulk scraping hundreds of pages per minute.
- **IP rotation:** Auto-rotates periodically. Don't force-rotate unless blocked.
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
- **Proxy not working?** → Check subscription status. Notify main agent.
- **2Captcha balance low?** → Notify main agent immediately.
- **Blocked even with proxy?** → Stop. Report. Do not retry more than 3 times.
- **Unsure if a site allows automation?** → Ask before proceeding.
