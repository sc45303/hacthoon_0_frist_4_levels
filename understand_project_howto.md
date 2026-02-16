# Personal AI Employee - How to Run Everything

**Part 3 of 5** | [← Back to Architecture](understand_project_architecture.md) | [Next: APIs & Integrations →](understand_project_apis.md)

---

## 🚀 Quick Start Guide

### Prerequisites Check

Before running anything, verify you have:  

```bash
# Check Python version (need 3.8+)
python --version

# Check Node.js version (need 14+)
node --version

# Check if virtual environment exists
ls -la venv/

# Check if credentials exist
ls -la credentials/
```

---

## 📧 Running Gmail Watcher

### Method 1: Manual Run (Testing)

```bash
# Navigate to project
cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault

# Activate virtual environment
source venv/bin/activate

# Run watcher
python watchers/gmail_watcher.py
```

**What you'll see:**
```
============================================================
📧 Gmail Watcher Starting
============================================================
Vault: /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
Check interval: 120 seconds
Monitoring: Unread + Important emails
============================================================

✅ Gmail API authenticated successfully

👀 Watching Gmail inbox...
Press Ctrl+C to stop
```

**When email arrives:**
```
📧 Created task from email: URGENT: Test email
   From: sender@example.com
   Priority: urgent
```

### Method 2: Using Shell Script

```bash
# Make script executable (first time only)
chmod +x run_gmail_watcher.sh

# Run it
./run_gmail_watcher.sh
```

### Method 3: Automatic (Cron - Already Running)

The Gmail watcher is already running automatically via cron!

**Check if it's running:**
```bash
# View cron jobs
crontab -l

# Check logs
tail -f Memory/cron_logs/gmail_watcher.log

# See detected emails
ls -lh Needs_Action/EMAIL_*
```

**Stop automatic running:**
```bash
# Remove cron jobs
crontab -r

# Or edit to disable specific job
crontab -e
# Comment out the gmail_watcher line with #
```

---

## 📤 Sending Emails via MCP

### Step 1: Ensure MCP Server is Configured

```bash
# Check MCP configuration
cat ~/.config/claude-code/mcp_config.json

# Should show:
# {
#   "mcpServers": {
#     "email": {
#       "command": "node",
#       "args": ["/path/to/email_mcp/index.js"]
#     }
#   }
# }
```

### Step 2: Restart Claude Code

MCP servers load on startup, so you need to restart Claude Code after configuration changes.

```bash
# Exit Claude Code (Ctrl+D or type 'exit')
# Then restart it
claude-code
```

### Step 3: Send Email via Claude

In Claude Code, simply say:

```
Send an email to test@example.com with subject "Test from AI Employee" and body "This is a test email sent by my Personal AI Employee!"
```

**What happens:**
1. Claude calls the `send_email` MCP tool
2. Email MCP server authenticates with Gmail
3. Email is sent via your Gmail account
4. You get confirmation: "✅ Email sent! Message ID: 19c5..."

### Step 4: Verify Email Sent

Check your Gmail sent folder or the recipient's inbox.

---

## 🔗 Running LinkedIn Auto-Poster

### Prerequisites: LinkedIn Authentication

**First time setup:**

```bash
# Activate virtual environment
source venv/bin/activate

# Run authentication script
python authenticate_linkedin_openid.py
```

**Follow the prompts:**
1. Copy the authorization URL
2. Open in browser
3. Sign in to LinkedIn
4. Grant permissions
5. Copy the code from the redirect URL
6. Paste code back in terminal
7. Token saved to `credentials/linkedin_token.json`

### Method 1: Manual Run

```bash
# Activate virtual environment
source venv/bin/activate

# Run poster
python watchers/linkedin_poster.py
```

**What you'll see:**
```
============================================================
🚀 LinkedIn Auto-Poster
============================================================
✅ Token loaded for: Suhail Khan

📬 Found 1 post(s) in queue

📝 Processing: my_post.md
   📤 Posting to LinkedIn...
   ✅ Posted successfully! ID: urn:li:share:7427801729053913088
   📁 Moved to: Posts_Queue/posted/

============================================================
✅ Posted 1/1 successfully
============================================================
```

### Method 2: Using Shell Script

```bash
# Make executable (first time only)
chmod +x run_linkedin_poster.sh

# Run it
./run_linkedin_poster.sh
```

### Method 3: Automatic (Cron - Already Configured)

LinkedIn poster runs automatically every hour via cron.

**Check status:**
```bash
# View cron jobs
crontab -l | grep linkedin

# Check logs
tail -f Memory/cron_logs/linkedin_poster.log

# View post history
cat Memory/linkedin_posts.log
```

### Creating Posts

**Create a text post:**
```bash
cat > Posts_Queue/my_post.md << 'EOF'
---
type: text
visibility: PUBLIC
---

Excited to share my new Personal AI Employee project! 🤖

It monitors my Gmail, sends emails, and posts to LinkedIn automatically.

Built with Python, Node.js, and AI. #AI #automation #productivity
EOF
```

**Create an article post:**
```bash
cat > Posts_Queue/article_post.md << 'EOF'
---
type: article
visibility: PUBLIC
url: https://example.com/my-article
title: Building an AI Employee
description: How I built an autonomous AI assistant
---

Check out my latest article about building a Personal AI Employee! 📖

Learn how to automate your business with AI. Link in post.
EOF
```

**Run poster:**
```bash
python watchers/linkedin_poster.py
```

---

## 🤖 Running the AI Employee (Main System)

### Current Configuration

Check which tier is configured in `main.py`:

```bash
# View current level
grep "CURRENT_LEVEL" main.py

# Should show:
# CURRENT_LEVEL = "platinum"
```

### Running Different Tiers

**Bronze Tier (Planner only):**
```bash
# Edit main.py
# Change: CURRENT_LEVEL = "silver"

# Run
python main.py
```

**Silver Tier (Executor):**
```bash
# Edit main.py
# Change: CURRENT_LEVEL = "silver"

# Run
python main.py
```

**Gold Tier (Learner):**
```bash
# Edit main.py
# Change: CURRENT_LEVEL = "gold"

# Run
python main.py
```

**Platinum Tier (Collaborator):**
```bash
# Edit main.py
# Change: CURRENT_LEVEL = "platinum"

# Run
python main.py
```

### What Each Tier Does

**Bronze:** Watches Needs_Action/, generates plans, requests approval
**Silver:** Bronze + executes approved tasks
**Gold:** Silver + learns from feedback
**Platinum:** Gold + multi-agent coordination

---

## 🧪 Testing Each Component

### Test 1: Gmail Watcher

```bash
# Start watcher
python watchers/gmail_watcher.py

# In another terminal, send yourself an email
# Mark it as important in Gmail
# Wait up to 2 minutes

# Expected: Task file created in Needs_Action/
ls -lh Needs_Action/EMAIL_*
```

### Test 2: Email MCP

```bash
# In Claude Code
"Send an email to your_email@example.com with subject 'MCP Test' and body 'Testing Email MCP Server'"

# Expected: Email arrives in inbox
# Check your email
```

### Test 3: LinkedIn Poster

```bash
# Create test post
echo "---
type: text
visibility: PUBLIC
---

Test post from my AI Employee! #test" > Posts_Queue/test_post.md

# Run poster
python watchers/linkedin_poster.py

# Expected: Post appears on your LinkedIn profile
# Check: https://www.linkedin.com/in/your-profile/
```

### Test 4: Task Planning

```bash
# Create test task
echo "Write a haiku about artificial intelligence" > Needs_Action/test_task.md

# Run planner
python -m agent.bronze_planner

# Expected outputs:
# - Plans/test_task.md (execution plan)
# - Approvals/test_task.md.approval.md (approval request)

# Check results
cat Plans/test_task.md
cat Approvals/test_task.md.approval.md
```

### Test 5: Task Execution

```bash
# Approve the task
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/test_task.md.approval.md

# Run executor
python -m agent.silver_executor

# Expected outputs:
# - Done/test_task.md (completed task)
# - Logs/test_task.md.execution.log (execution log)

# Check results
cat Done/test_task.md
cat Logs/test_task.md.execution.log
```

---

## 🔍 Monitoring & Logs

### Check System Status

```bash
# Check if Gmail watcher is running
ps aux | grep gmail_watcher

# Check cron jobs
crontab -l

# View all logs
ls -lh Memory/cron_logs/

# View detected emails
ls -lh Needs_Action/

# View completed tasks
ls -lh Done/

# View execution logs
ls -lh Logs/
```

### Real-Time Monitoring

```bash
# Watch Gmail watcher logs
tail -f Memory/cron_logs/gmail_watcher.log

# Watch LinkedIn poster logs
tail -f Memory/cron_logs/linkedin_poster.log

# Watch all logs
tail -f Memory/cron_logs/*.log

# Watch for new tasks
watch -n 5 'ls -lh Needs_Action/'
```

### View Statistics

```bash
# Count detected emails
ls Needs_Action/EMAIL_* | wc -l

# Count completed tasks
ls Done/ | wc -l

# View task history
cat Memory/task_history.json | python -m json.tool

# View processed emails
cat Memory/processed_emails.json | python -m json.tool
```

---

## 🛠️ Common Operations

### Re-authenticate Gmail

```bash
# Remove old token
rm credentials/gmail_token.pickle
rm credentials/gmail_token.json

# Run watcher (will trigger auth flow)
python watchers/gmail_watcher.py

# Follow authentication prompts
```

### Re-authenticate LinkedIn

```bash
# Remove old token
rm credentials/linkedin_token.json

# Run authentication
python authenticate_linkedin_openid.py

# Follow authentication prompts
```

### Clear Processed Emails (Re-detect Old Emails)

```bash
# Backup current list
cp Memory/processed_emails.json Memory/processed_emails.json.backup

# Clear list
echo "[]" > Memory/processed_emails.json

# Next run will detect all unread important emails again
```

### Stop All Automation

```bash
# Remove all cron jobs
crontab -r

# Or edit to disable specific jobs
crontab -e
# Comment out lines with #
```

### Restart All Automation

```bash
# Re-install cron jobs
./setup_cron.sh

# Verify installation
crontab -l
```

---

## 🐛 Troubleshooting

### Gmail Watcher Not Detecting Emails

**Check:**
1. Is watcher running? `ps aux | grep gmail_watcher`
2. Are emails marked as important in Gmail?
3. Are emails unread?
4. Check logs: `tail -f Memory/cron_logs/gmail_watcher.log`

**Fix:**
```bash
# Restart watcher
pkill -f gmail_watcher
./run_gmail_watcher.sh
```

### Email MCP Not Working

**Check:**
1. Is MCP configured? `cat ~/.config/claude-code/mcp_config.json`
2. Does token exist? `ls -lh credentials/gmail_token.json`
3. Did you restart Claude Code?

**Fix:**
```bash
# Test MCP server manually
cd mcp_servers/email_mcp
node test.js

# If fails, re-authenticate
cd ../..
python watchers/gmail_watcher.py
```

### LinkedIn Poster Fails

**Check:**
1. Does token exist? `cat credentials/linkedin_token.json`
2. Is token valid? (tokens expire)
3. Check logs: `cat Memory/linkedin_posts.log`

**Fix:**
```bash
# Re-authenticate
python authenticate_linkedin_openid.py
```

### Cron Jobs Not Running

**Check:**
1. Is cron service running? `service cron status`
2. Are jobs installed? `crontab -l`
3. Check logs: `tail -f Memory/cron_logs/*.log`

**Fix:**
```bash
# Start cron service
sudo service cron start

# Re-install jobs
./setup_cron.sh
```

---

**Continue to: understand_project_apis.md**
