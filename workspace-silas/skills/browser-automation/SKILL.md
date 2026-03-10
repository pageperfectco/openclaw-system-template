---
name: browser
description: Automate web browser interactions using natural language via CLI commands. Use when the user asks to browse websites, navigate web pages, extract data from websites, take screenshots, fill forms, click buttons, or interact with web applications.
allowed-tools: Bash
---

# Browser Automation

Automate browser interactions using Stagehand CLI with Claude.

### First: Environment Selection (Local vs Remote)

The skill automatically selects between local and remote browser environments:
- **If Browserbase API keys exist** (BROWSERBASE_API_KEY and BROWSERBASE_PROJECT_ID in .env file): Uses remote Browserbase environment
- **If no Browserbase API keys**: Falls back to local Chrome browser
- **No user prompting**: The selection happens automatically based on available configuration

## Setup (First Time Only)

Check `setup.json` in this directory. If `setupComplete: false`:

```bash
npm install    # Install dependencies
npm link       # Create global 'browser' command
```

## Commands

All commands work identically in both modes:

```bash
browser navigate <url>                    # Go to URL
browser act "<action>"                    # Natural language action
browser extract "<instruction>" ['{}']    # Extract data (optional schema)
browser observe "<query>"                 # Discover elements
browser screenshot                        # Take screenshot
browser close                             # Close browser
```

## Quick Example

```bash
browser navigate https://example.com
browser act "click the Sign In button"
browser extract "get the page title"
browser close
```

## Mode Comparison

| Feature | Local | Browserbase |
|---------|-------|-------------|
| Speed | Faster | Slightly slower |
| Setup | Chrome required | API key required |
| Stealth mode | No | Yes |
| Proxy/CAPTCHA | No | Yes |
| Best for | Development | Production/scraping |

## Best Practices

1. **Always use the mobile proxy** — Litport is unlimited, residential IPs are cleaner. No reason not to.
2. **Always navigate first** before interacting
3. **Take screenshots internally** after each command to verify page state — but **NEVER forward screenshots to the user** unless they explicitly ask. They are internal verification only.
4. **Be specific** in action descriptions
5. **Close browser** when done

### Proxy Config
```bash
# Read from config file — never hardcode credentials
source ~/.config/litport/proxy.conf
# Provides: $PROXY_URL, $PROXY_HOST, $PROXY_PORT, $PROXY_USER, $PROXY_PASS
```

For OpenClaw `browser` tool: the proxy is applied at the network level — no special flags needed in tool calls. For curl/Python, read `~/.config/litport/proxy.conf` and pass `$PROXY_URL` explicitly.

## Troubleshooting

- **Chrome not found**: Install Chrome or use Browserbase mode
- **Action fails**: Use `browser observe` to discover available elements
- **Browserbase fails**: Verify API key and project ID are set

For detailed examples, see [EXAMPLES.md](EXAMPLES.md).
For API reference, see [REFERENCE.md](REFERENCE.md).

---

## 🔑 Advanced: React SPA Internal API Pattern

**When to use:** Form submit buttons stay disabled due to React state (Cloudflare Turnstile, reCAPTCHA, client-side validation) and standard UI interaction fails.

**Key insight:** Modern SPAs bundle their entire API layer in one JS file. You can import it directly from the browser context and call API functions without touching the UI at all.

### Step 1 — Find the bundle URL

```javascript
// In browser evaluate:
Array.from(document.querySelectorAll('script[src]')).map(s => s.src)
// Look for: /assets/index-HASH.js, /static/js/main.HASH.js, etc.
```

### Step 2 — Import and search for the function you need

```javascript
const mod = await import('/assets/index-BNpPNWD8.js')

// Search by URL pattern in function body
const loginFns = Object.entries(mod).filter(([k, v]) =>
  typeof v === 'function' && v.toString().includes('user/login')
)
// => [['on', function(e,t,n,r,o) => ...]]

// Inspect the signature
console.log(mod.on.toString())
// => async(e,t,n,r,o)=>...,url:"user/login",data:{email:e,password:t,...}
```

### Step 3 — Call the function directly

```javascript
const result = await mod.on(
  'email@example.com',
  'password123',
  false,     // remember_me
  undefined, // event_id
  {}         // mixpanelProps
)
// => { data: { fresh_login: false }, status: 200 }
```

The function runs inside the app's own axios instance with correct baseURL, credentials, and headers — no need to know the full API URL or auth headers.

### Step 4 — Verify session

```javascript
document.cookie  // Check for session cookie (often 'id', 'token', 'session')
// Then navigate to the authenticated route to confirm
```

### Common search patterns

| What you want | Search string |
|--------------|--------------|
| Login | `'user/login'` or `'/login'` |
| Registration | `'email'` + `'password'` + `'baseURL'` |
| Data fetch | `url` + relevant endpoint name |
| Invite/signup | `'/mu/signup'` or `'code'` + `'password'` |

### Why this works

- The function uses the app's own axios instance — cookies, CORS, baseURL all handled
- Bypasses React state entirely (no Turnstile gate, no disabled button)
- `withCredentials: true` means session cookies are set automatically
- Works on any bundled SPA (React, Vue, Angular, Svelte)

### When it won't work

- Server actively validates Turnstile token (check: does the API return `invalid_token` without it?)
- Function requires headers generated by other app internals (`X-UBS-APP`, fingerprint tokens) — in that case, find and call those generators too before calling the main function
- API is on a different domain with strict CORS (try direct curl instead)

### Discovered applications

| App | Bundle | Login fn | Notes |
|-----|--------|----------|-------|
| Ubersuggest (app.neilpatel.com) | `/assets/index-BNpPNWD8.js` | `mod.on(email, pass, false, undefined, {})` | Turnstile on UI only, not server-validated for login |

---

## 🔒 Cloudflare Turnstile — Bypass Decision Tree

1. **Try UI click first** — sometimes it auto-passes with a non-headless profile
2. **Check if server actually validates it** — call the API endpoint directly (curl/XHR) without a token; if it works, skip Turnstile entirely
3. **If server requires it** — solve with 2captcha (`TurnstileTaskProxyless`, sitekey from JS bundle: grep `TURNSTILE_SITE_KEY`)
4. **Inject token into React state** — use the SPA Internal API pattern above to call the login function directly (token in data payload)
5. **Last resort** — use proxy + 2captcha + real browser (Litport → solve → inject)
