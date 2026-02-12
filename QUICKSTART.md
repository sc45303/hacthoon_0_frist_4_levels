# 🚀 Personal AI Employee - Quick Start Guide

**Silver Tier Implementation - Ready to Use!**

---

## 🎯 What You Have Now

Your Personal AI Employee can:
- ✅ Monitor Gmail inbox automatically (every 2 minutes)
- ✅ Send emails via Claude using MCP
- ✅ Post to LinkedIn automatically (needs credentials)
- ✅ Run on automated schedule with cron
- ✅ Create tasks from important emails
- ✅ Log all operations

---

## ⚡ Quick Start (5 Minutes)

### 1. Gmail Monitoring (Already Working!)

**Start the watcher:**
```bash
./run_gmail_watcher.sh
```

**Test it:**
- Send yourself an email with "URGENT" in the subject
- Check `Needs_Action/` for the created task file

### 2. Send Email via Claude (Already Working!)

**In Claude Code, say:**
```
Send an email to [email] with subject "Test" and body "Hello from my AI Employee!"
```

The Email MCP server will send it via Gmail.

### 3. LinkedIn Setup (15 Minutes)

**Step 1: Create LinkedIn App**
- Visit: https://www.linkedin.com/developers/apps
- Follow: `LINKEDIN_APP_SETUP.md`
- Get Client ID and Secret

**Step 2: Save Credentials**
```bash
cp credentials/linkedin_credentials.json.template credentials/linkedin_credentials.json
nano credentials/linkedin_credentials.json
# Add your Client ID and Secret
```

**Step 3: Authenticate**
```bash
python authenticate_linkedin.py
```

**Step 4: Test Auto-Poster**
```bash
python watchers/linkedin_poster.py
```

**Step 5: Test MCP Server**
- Restart Claude Code
- Say: "Post to LinkedIn: Just launched my AI Employee! 🚀"

### 4. Enable Automation (Optional)

**Install cron jobs:**
```bash
crontab -l > /tmp/current_cron 2>/dev/null || true
cat crontab_entries.txt >> /tmp/current_cron
crontab /tmp/current_cron
rm /tmp/current_cron
```

**Verify:**
```bash
crontab -l
```

---

## 📁 Project Structure

```
AI_Employee_Vault/
├── watchers/
│   ├── gmail_watcher.py          # Gmail monitoring
│   └── linkedin_poster.py        # LinkedIn auto-posting
├── mcp_servers/
│   ├── email_mcp/                # Email MCP server
│   └── linkedin_mcp/             # LinkedIn MCP server
├── credentials/                  # API credentials
├── Posts_Queue/                  # LinkedIn post queue
├── Needs_Action/                 # Tasks from emails
└── Memory/                       # Logs and history
```

---

## 🔧 Common Commands

### Gmail
```bash
# Start watcher
./run_gmail_watcher.sh

# View logs
tail -f Memory/cron_logs/gmail_watcher.log
```

### LinkedIn
```bash
# Authenticate
python authenticate_linkedin.py

# Post from queue
python watchers/linkedin_poster.py

# View logs
tail -f Memory/cron_logs/linkedin_poster.log
```

### Cron
```bash
# View scheduled jobs
crontab -l

# View logs
tail -f Memory/cron_logs/*.log
```

---

## 📚 Documentation

| Component | Guide |
|-----------|-------|
| Gmail Watcher | `GMAIL_WATCHER_README.md` |
| Email MCP | `EMAIL_MCP_COMPLETE.md` |
| LinkedIn Auto-Poster | `LINKEDIN_POSTER_GUIDE.md` |
| LinkedIn MCP | `mcp_servers/linkedin_mcp/README.md` |
| Cron Scheduling | `CRON_SCHEDULING_GUIDE.md` |
| Complete Status | `SILVER_TIER_COMPLETE.md` |

---

## 🎯 Next Steps

### Option 1: Complete LinkedIn Testing (15 min) ⭐
- Create LinkedIn app
- Test auto-poster
- Test MCP server

### Option 2: Start Using It!
- Gmail monitoring is already working
- Email MCP is ready to use
- Add LinkedIn when ready

### Option 3: Move to Gold Tier
- Learning system
- Accounting integration
- Advanced automation

---

## 🆘 Troubleshooting

### Gmail Not Working
```bash
# Re-authenticate
./run_gmail_watcher.sh
```

### LinkedIn Authentication Failed
```bash
# Check credentials
cat credentials/linkedin_credentials.json

# Re-authenticate
python authenticate_linkedin.py
```

### Cron Jobs Not Running
```bash
# Check cron service
service cron status

# Start if needed
sudo service cron start
```

---

## ✅ Success Checklist

- [ ] Gmail watcher running
- [ ] Email MCP tested
- [ ] LinkedIn app created
- [ ] LinkedIn authenticated
- [ ] LinkedIn auto-poster tested
- [ ] LinkedIn MCP tested
- [ ] Cron jobs installed (optional)

---

**Your Personal AI Employee is Ready!** 🎉

For detailed documentation, see `SILVER_TIER_COMPLETE.md`
