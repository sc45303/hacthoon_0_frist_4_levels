# 📧 Gmail Watcher - README

## What You've Built

You now have a **Gmail Watcher** that monitors your inbox and creates tasks automatically!

## Files Created

1. **watchers/gmail_watcher.py** - Main watcher script
2. **GMAIL_WATCHER_SETUP.md** - Complete setup guide
3. **start_gmail_watcher.sh** - Quick start script
4. **test_gmail_setup.py** - Setup verification script
5. **credentials/** - Directory for Gmail API credentials

## Quick Start

### Step 1: Install Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Get Gmail Credentials
1. Go to: https://console.cloud.google.com/
2. Create project → Enable Gmail API → Create OAuth2 credentials
3. Download as `gmail_credentials.json`
4. Place in: `credentials/gmail_credentials.json`

**Detailed instructions:** See `GMAIL_WATCHER_SETUP.md`

### Step 3: Test Setup
```bash
python test_gmail_setup.py
```

### Step 4: Run Watcher
```bash
# Option 1: Quick start script
./start_gmail_watcher.sh

# Option 2: Direct
python watchers/gmail_watcher.py
```

### Step 5: Test It
1. Send yourself an email
2. Mark it as important (star it)
3. Check `Needs_Action/` for task file

## What It Does

- ✅ Monitors Gmail inbox every 2 minutes
- ✅ Detects unread + important emails
- ✅ Creates task files in Needs_Action/
- ✅ Tracks processed emails (no duplicates)
- ✅ Extracts: sender, subject, date, content
- ✅ Determines priority based on keywords
- ✅ Runs continuously in background

## Task File Format

```markdown
---
type: email
from: sender@example.com
subject: Important message
received: Mon, 12 Feb 2026 10:30:00
priority: high
gmail_id: 18d4f2a1b3c5e6f7
---

# Email Task: Important message

**From:** sender@example.com
**Date:** Mon, 12 Feb 2026 10:30:00
**Priority:** high

## Email Content
[Email snippet here]

## Suggested Actions
- [ ] Read full email
- [ ] Draft reply
- [ ] Forward if needed
- [ ] Archive after handling
```

## Configuration

### Change Check Interval
Edit `watchers/gmail_watcher.py`:
```python
watcher = GmailWatcher(vault_path, check_interval=120)  # 2 minutes
```

### Change Email Filter
Edit `check_inbox()` method:
```python
q='is:unread is:important'  # Current
q='is:unread'               # All unread
q='is:unread from:boss@company.com'  # Specific sender
```

## Troubleshooting

### "gmail_credentials.json not found"
- Download from Google Cloud Console
- Place in `credentials/gmail_credentials.json`

### "Access blocked"
- Add your email to "Test users" in OAuth consent screen

### Not detecting emails
- Check email is unread
- Check email is marked important (starred)
- Wait for check interval (2 minutes)

## Security

**What's stored:**
- `credentials/gmail_credentials.json` - OAuth2 credentials (private)
- `credentials/gmail_token.pickle` - Access token (private)
- `Memory/processed_emails.json` - Email IDs (safe)

**Permissions:**
- Read-only access to Gmail
- Cannot send, delete, or modify emails

**Git safety:**
- credentials/ is in .gitignore
- Credentials never committed to Git

## Next Steps

After Gmail Watcher is working:

1. **Build Email MCP Server** - To send replies
2. **Build WhatsApp Watcher** - Monitor WhatsApp messages
3. **Build LinkedIn Watcher** - Auto-post to LinkedIn
4. **Integrate with Executor** - Auto-process email tasks
5. **Complete Silver Tier** - Full external integration

## Status

- ✅ Gmail Watcher script created
- ✅ Setup guide created
- ✅ Test script created
- ✅ Dependencies updated
- ✅ .gitignore updated
- ⏳ Waiting for: Gmail API credentials
- ⏳ Waiting for: First authentication
- ⏳ Waiting for: Test email

## Support

- **Setup Guide:** `GMAIL_WATCHER_SETUP.md`
- **Silver Tier Spec:** `SILVER_TIER_SPEC.md`
- **Master Roadmap:** `MASTER_ROADMAP.md`

---

**Gmail Watcher Ready!**
**Next:** Get Gmail API credentials and test it!
