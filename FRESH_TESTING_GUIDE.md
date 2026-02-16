# 🧪 Fresh Testing Guide - Start from Scratch

**Your project is now clean! All old test files deleted.**

---

## ✅ Current Status

```
Needs_Action: 0 files (clean)
Plans: 0 files (clean)
Approvals: 0 files (clean)
Done: 0 files (clean)
Logs: 0 files (clean)
Posts_Queue: 0 files (clean)
```

**Everything is ready for fresh testing!**

---

## 🎯 Test 1: Send Email via MCP (Easiest Test)

This is the **fastest way** to see your AI employee in action!

### Step 1: Restart Claude Code

```bash
# Exit Claude Code (Ctrl+D or type 'exit')
# Then restart it
claude-code
```

### Step 2: Send a Test Email

In Claude Code, say:

```
Send an email to YOUR_EMAIL@example.com with subject "AI Employee Test"
and body "This is a test email from my Personal AI Employee! It works!"
```

**Replace YOUR_EMAIL@example.com with your actual email address!**

### Step 3: What Happens?

1. **Claude receives your command**
2. **Claude calls Email MCP Server** (the tool we built)
3. **MCP Server authenticates** with Gmail using your token
4. **MCP Server creates email** in proper format
5. **MCP Server sends via Gmail API**
6. **You get confirmation**: "✅ Email sent! Message ID: 19c5..."
7. **Check your inbox** - email should arrive within seconds!

### Expected Result:

```
✅ Email sent successfully!

To: your_email@example.com
Subject: AI Employee Test
Message ID: 19c5abc123def456
```

**This proves:**
- ✅ Your AI employee can send emails
- ✅ MCP integration works
- ✅ Gmail API is connected
- ✅ Authentication is working

---

## 🎯 Test 2: Create a Task and Watch the Workflow

This shows the **complete workflow** from task creation to execution.

### Step 1: Create a Simple Task

```bash
cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault

# Create a simple task
cat > Needs_Action/my_first_task.md << 'EOF'
Write a short haiku about artificial intelligence.
EOF
```

### Step 2: Run the Planner

```bash
# Activate virtual environment
source venv/bin/activate

# Run Bronze Planner
python -m agent.bronze_planner
```

### Step 3: What Happens?

1. **Planner detects** the task file in Needs_Action/
2. **Planner reads** the task content
3. **Planner sends to Gemini AI**: "Create a plan for this task"
4. **Gemini generates** a step-by-step plan
5. **Planner saves** the plan to Plans/my_first_task.md
6. **Planner creates** approval request in Approvals/my_first_task.md.approval.md
7. **Planner updates** Memory/task_history.json

### Step 4: Check the Generated Plan

```bash
# View the plan
cat Plans/my_first_task.md

# View the approval request
cat Approvals/my_first_task.md.approval.md
```

**You'll see:**
- A detailed execution plan created by AI
- An approval request waiting for your decision

### Step 5: Approve the Task

```bash
# Approve the task (change [ ] to [x])
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/my_first_task.md.approval.md

# Verify approval
cat Approvals/my_first_task.md.approval.md | grep Approved
```

### Step 6: Execute the Task

```bash
# Run Silver Executor
python -m agent.silver_executor
```

### Step 7: What Happens?

1. **Executor detects** approved task
2. **Executor reads** the plan
3. **Executor executes** the task (writes the haiku)
4. **Executor moves** task to Done/my_first_task.md
5. **Executor creates** log in Logs/my_first_task.md.execution.log
6. **Executor updates** memory

### Step 8: Check the Results

```bash
# View completed task
cat Done/my_first_task.md

# View execution log
cat Logs/my_first_task.md.execution.log

# View task history
cat Memory/task_history.json
```

**You'll see:**
- ✅ The haiku written by AI
- ✅ Complete execution log
- ✅ Task moved to Done folder
- ✅ History updated

---

## 🎯 Test 3: Gmail Watcher (Automatic Detection)

This tests **automatic email monitoring**.

### Step 1: Check if Gmail Watcher is Running

```bash
# Check if running
ps aux | grep gmail_watcher

# If not running, start it
./run_gmail_watcher.sh
```

### Step 2: Send Yourself a Test Email

1. **Open Gmail** (from another device or browser)
2. **Send email to yourself**:
   - To: your_email@gmail.com
   - Subject: "URGENT: Test for AI Employee"
   - Body: "This is a test email to check if my AI employee detects it."
3. **Mark as Important** (click the star or importance marker)
4. **Keep it Unread**

### Step 3: Wait and Watch

```bash
# Watch for new tasks (updates every 5 seconds)
watch -n 5 'ls -lh Needs_Action/'

# Or watch the logs
tail -f Memory/cron_logs/gmail_watcher.log
```

### Step 4: What Happens?

1. **Gmail Watcher checks inbox** (every 2 minutes)
2. **Watcher finds** your unread important email
3. **Watcher extracts** email details (from, subject, body)
4. **Watcher creates** task file: EMAIL_URGENT_Test_for_AI_Employee_[id].md
5. **Watcher saves** to Needs_Action/
6. **Watcher logs** the email ID to Memory/processed_emails.json

### Step 5: Check the Created Task

```bash
# List detected emails
ls -lh Needs_Action/EMAIL_*

# View the task file
cat Needs_Action/EMAIL_URGENT_Test_for_AI_Employee_*.md
```

**You'll see:**
- ✅ Task file created automatically
- ✅ Email metadata extracted (from, subject, date)
- ✅ Email body included
- ✅ Suggested actions listed

**This proves:**
- ✅ Gmail monitoring works
- ✅ Email detection works
- ✅ Task creation works
- ✅ Automation is running

---

## 🎯 Test 4: LinkedIn Posting (If Authenticated)

**Note:** This requires LinkedIn authentication first.

### Step 1: Authenticate LinkedIn (If Not Done)

```bash
source venv/bin/activate
python authenticate_linkedin_openid.py
# Follow the prompts
```

### Step 2: Create a Test Post

```bash
cat > Posts_Queue/test_post.md << 'EOF'
---
type: text
visibility: PUBLIC
---

Testing my Personal AI Employee! 🤖

Just built an AI system that:
✅ Monitors Gmail automatically
✅ Sends emails via AI commands
✅ Posts to LinkedIn

#AI #automation #testing
EOF
```

### Step 3: Run LinkedIn Poster

```bash
source venv/bin/activate
python watchers/linkedin_poster.py
```

### Step 4: What Happens?

1. **Poster scans** Posts_Queue/ folder
2. **Poster finds** test_post.md
3. **Poster parses** frontmatter and content
4. **Poster authenticates** with LinkedIn API
5. **Poster creates** API payload
6. **Poster sends** to LinkedIn
7. **Poster moves** file to Posts_Queue/posted/
8. **Poster logs** result to Memory/linkedin_posts.log

### Step 5: Check Results

```bash
# Check if post was moved
ls -lh Posts_Queue/posted/

# View log
cat Memory/linkedin_posts.log

# Check your LinkedIn profile
# The post should appear on your profile!
```

---

## 📊 Understanding What You Did

### Test 1: Email Sending
**What you did:** Gave a command to Claude
**What happened:**
- Claude → MCP Server → Gmail API → Email sent
- Direct action, no approval needed
- Instant result

### Test 2: Task Workflow
**What you did:** Created a task file
**What happened:**
- Task → Planner → AI generates plan → Approval request
- You approved → Executor runs → Task completed
- Full workflow with human-in-the-loop

### Test 3: Gmail Monitoring
**What you did:** Sent yourself an email
**What happened:**
- Gmail Watcher detected it automatically
- Created task file from email
- No manual intervention needed
- Runs 24/7 via cron

### Test 4: LinkedIn Posting
**What you did:** Created a post file
**What happened:**
- Poster found the file
- Posted to LinkedIn API
- Moved to archive
- Can run automatically via cron

---

## 🎓 Key Concepts

### 1. Two Ways to Use Your AI Employee

**Method A: Direct Commands (via MCP)**
- You tell Claude: "Send email..."
- Claude uses MCP tools
- Instant action
- No approval needed
- Good for: Quick actions you control

**Method B: Task Workflow (via Files)**
- You create task file
- AI generates plan
- You approve plan
- AI executes task
- Good for: Complex tasks, automation

### 2. What Runs Automatically?

**Already Running 24/7:**
- ✅ Gmail Watcher (every 2 minutes)
- ✅ LinkedIn Poster (every hour)
- ✅ Log Cleanup (daily)

**Requires Manual Trigger:**
- ⚠️ Task Planning (run: python -m agent.bronze_planner)
- ⚠️ Task Execution (run: python -m agent.silver_executor)
- ⚠️ Task Approval (you edit approval file)

### 3. Where Does AI Come In?

**Gemini AI is used for:**
- 🧠 Generating execution plans
- 🧠 Analyzing task complexity
- 🧠 Creating step-by-step instructions
- 🧠 Writing content (haikus, messages, etc.)

**AI is NOT used for:**
- ❌ Sending emails (direct API call)
- ❌ Posting to LinkedIn (direct API call)
- ❌ Monitoring Gmail (direct API call)
- ❌ File operations (Python code)

---

## 🔍 How to Verify Everything Works

### Check Gmail Watcher Status
```bash
ps aux | grep gmail_watcher
tail -f Memory/cron_logs/gmail_watcher.log
```

### Check Cron Jobs
```bash
crontab -l
```

### Check MCP Configuration
```bash
cat ~/.config/claude-code/mcp_config.json
```

### Check Credentials
```bash
ls -lh credentials/
```

### Check Task Folders
```bash
ls -lh Needs_Action/ Plans/ Approvals/ Done/ Logs/
```

---

## 🎉 Success Criteria

After running these tests, you should have:

✅ **Test 1 Success:** Email received in your inbox
✅ **Test 2 Success:** Haiku in Done/ folder, log in Logs/
✅ **Test 3 Success:** Email task in Needs_Action/
✅ **Test 4 Success:** Post on your LinkedIn profile

**If all tests pass, your AI Employee is fully operational!** 🚀

---

## 🐛 If Something Doesn't Work

### Email MCP Not Working?
```bash
cd mcp_servers/email_mcp
node test.js
```

### Gmail Watcher Not Detecting?
```bash
# Check if emails are marked as important
# Check if emails are unread
# Check logs: tail -f Memory/cron_logs/gmail_watcher.log
```

### Task Execution Fails?
```bash
# Check if task is approved
cat Approvals/*.md | grep "\[x\]"

# Check Gemini API key
cat .env | grep GEMINI_API_KEY
```

---

## 📚 Next Steps

After testing:

1. **Read the documentation** - understand_project.md
2. **Customize for your needs** - modify watchers, add features
3. **Set up LinkedIn** - if not done yet
4. **Create real tasks** - automate your actual work
5. **Submit to hackathon** - you're ready!

---

**Happy Testing!** 🧪✨
