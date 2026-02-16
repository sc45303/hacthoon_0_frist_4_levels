# Personal AI Employee - Quick Reference Card

**🚀 Your AI Employee at a Glance**

---

## ✅ What's Working RIGHT NOW
 
```
✅ Gmail Watcher      - Running via cron every 2 minutes
✅ Email MCP Server   - Ready to send emails via Claude
✅ Cron Automation    - Active 24/7
```

---

## 🎯 Current Tier: SILVER (60% Working)

**Bronze** ✅ → **Silver** ✅ (60%) → Gold ❌ → Platinum ❌

---

## 📧 Send Email (via Claude)

```
Say: "Send email to test@example.com with subject 'Hello'
and body 'This is a test from my AI Employee'"
```

---

## 🔗 Post to LinkedIn

**Method 1: Queue**
```bash
cat > Posts_Queue/my_post.md << 'EOF'
---
type: text
visibility: PUBLIC
---
Your post content here #hashtags
EOF

python watchers/linkedin_poster.py
```

**Method 2: Via Claude (after auth)**
```
Say: "Post to LinkedIn: Your message here"
```

---

## 🔍 Check Status

```bash
# Gmail watcher running?
ps aux | grep gmail_watcher

# View detected emails
ls -lh Needs_Action/

# Check logs
tail -f Memory/cron_logs/*.log

# View cron jobs
crontab -l
```

---

## 🔐 Re-authenticate

**Gmail:**
```bash
rm credentials/gmail_token.pickle
python watchers/gmail_watcher.py
```

**LinkedIn:**
```bash
rm credentials/linkedin_token.json
python authenticate_linkedin_openid.py
```

---

## 🧪 Test Components

**Test Gmail Watcher:**
```bash
python watchers/gmail_watcher.py
# Send yourself an email marked as important
```

**Test Email MCP:**
```
In Claude: "Send email to your_email@example.com
with subject 'Test' and body 'Testing MCP'"
```

**Test LinkedIn Poster:**
```bash
echo "---
type: text
---
Test post" > Posts_Queue/test.md

python watchers/linkedin_poster.py
```

---

## 📁 Important Locations

```
Needs_Action/     - New tasks (input)
Plans/            - Generated plans
Approvals/        - Approval requests
Done/             - Completed tasks
Logs/             - Execution logs
Memory/           - Task history & logs
Posts_Queue/      - LinkedIn post queue
credentials/      - API credentials
```

---

## 🔑 API Keys & Credentials

```
.env                              - Gemini API key
credentials/gmail_credentials.json    - Gmail OAuth app
credentials/gmail_token.pickle        - Gmail auth (Python)
credentials/gmail_token.json          - Gmail auth (Node.js)
credentials/linkedin_credentials.json - LinkedIn OAuth app
credentials/linkedin_token.json       - LinkedIn auth token
```

---

## 🤖 Which AI is Used?

**Google Gemini 2.5 Flash** - AI brain for planning
**NOT Claude** - Claude Code is just the dev assistant

---

## 🔄 Is It Running 24/7?

**YES!** Via cron:
- Gmail watcher: Every 2 minutes
- LinkedIn poster: Every hour
- Log cleanup: Daily

**BUT:** Tasks require your approval before execution

---

## 🛠️ Common Commands

```bash
# Activate environment
source venv/bin/activate

# Run Gmail watcher
python watchers/gmail_watcher.py

# Run LinkedIn poster
python watchers/linkedin_poster.py

# Run AI employee
python main.py

# View logs
tail -f Memory/cron_logs/*.log

# Check cron
crontab -l
```

---

## 🐛 Troubleshooting

**Gmail watcher not working?**
```bash
pkill -f gmail_watcher
./run_gmail_watcher.sh
```

**Email MCP not working?**
```bash
cd mcp_servers/email_mcp
node test.js
```

**Cron not running?**
```bash
sudo service cron start
crontab -l
```

---

## 📖 Full Documentation

Read the complete guides:
1. `understand_project.md` - Overview
2. `understand_project_architecture.md` - Technical details
3. `understand_project_howto.md` - How to run
4. `understand_project_apis.md` - APIs explained
5. `understand_project_capabilities.md` - What it can/cannot do

---

## 🎯 Next Steps

1. ✅ Test Email MCP (restart Claude Code first)
2. ⚠️ Authenticate LinkedIn (if not done)
3. ⚠️ Test LinkedIn posting
4. 🎉 Submit to hackathon!

---

**Quick Help:** Read `understand_project.md` for complete overview
**Emergency:** Check logs in `Memory/cron_logs/`
**Support:** All documentation in project root

---

**Your AI Employee is Ready!** 🚀
