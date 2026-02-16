# 🏆 Hackathon Demo Script - Personal AI Employee

## 📋 Pre-Demo Checklist

Before your demo, verify:
```bash
bash status.sh
```

Ensure:
- ✅ Gmail Watcher is running
- ✅ Cron jobs are active (3 jobs)
- ✅ Credentials authenticated (Gmail + LinkedIn)
- ✅ At least 1 completed task in Done/

---

## 🎬 Demo Flow (7 minutes total)

### **Opening (30 seconds)**

"Hi! I built a Personal AI Employee - a complete autonomous system that handles real work 24/7. Let me show you how it works."

---

### **Part 1: Email Monitoring (2 minutes)**

**Show the watcher:**
```bash
ps aux | grep gmail_watcher
tail -5 Memory/cron_logs/gmail_watcher.log
```

**Explain:**
"The system monitors my Gmail every 2 minutes. When it finds unread emails, it automatically creates task files."

**Show existing tasks:**
```bash
ls -lh Needs_Action/
cat Needs_Action/[pick_one].md
```

**Explain:**
"Each email becomes a structured task with metadata, content, and suggested actions."

---

### **Part 2: AI Planning (1.5 minutes)**

**Run the planner:**
```bash
source venv/bin/activate
python -m agent.bronze_planner
```

**Show the plan:**
```bash
cat Plans/[task_name].md
```

**Explain:**
"The Bronze level AI analyzes the task and creates a step-by-step execution plan using Gemini AI. This is the 'thinking' layer."

---

### **Part 3: Human Approval (30 seconds)**

**Show approval file:**
```bash
cat Approvals/[task_name].md.approval.md
```

**Explain:**
"Human-in-the-loop: I review and approve plans before execution. This ensures control and safety."

**Approve it:**
```bash
# Change [ ] to [x] in the approval file
```

---

### **Part 4: AI Execution (1.5 minutes)**

**Run the executor:**
```bash
python -m agent.silver_executor
```

**Show results:**
```bash
cat Done/[task_name].md
cat Logs/[task_name].md.execution.log
```

**Explain:**
"The Silver level AI executes the approved plan, logs every step, and moves completed tasks to Done. Look at this detailed execution log - it shows exactly what the AI did."

---

### **Part 5: LinkedIn Integration (1 minute)**

**Show the quick post:**
```bash
./quick_post.sh "Live demo of my AI Employee! Built for the hackathon. #AI #automation"
```

**Explain:**
"The system can also post to LinkedIn automatically. I can create posts via command line, or they're posted hourly via cron. This post just went live on my profile."

**Show on LinkedIn:**
Open your LinkedIn profile and show the post.

---

### **Part 6: Claude MCP Integration (30 seconds)**

**Open Claude Code and demonstrate:**
```
Send an email to [your_email] with subject "Demo Email"
and body "This email was sent by my AI Employee through Claude!"
```

**Explain:**
"I built an MCP server that lets Claude send emails directly. This bridges conversational AI with real-world actions."

---

### **Closing (30 seconds)**

**Show the stats:**
```bash
echo "Real usage stats:"
echo "- Emails processed: $(cat Memory/processed_emails.json | grep -o '19[a-z0-9]*' | wc -l)"
echo "- Tasks completed: $(ls Done/ | wc -l)"
echo "- LinkedIn posts: $(ls Posts_Queue/posted/ | wc -l)"
echo "- Running 24/7 with 3 cron jobs"
```

**Final statement:**
"This is a true Digital FTE - an AI employee that monitors, plans, executes, and communicates autonomously. It's not just a chatbot - it's a complete autonomous agent system with human oversight."

---

## 🎯 Key Points to Emphasize

1. **4 Levels Implemented:**
   - 🥉 Bronze: AI Planner (strategic thinking)
   - 🥈 Silver: AI Executor (takes action)
   - 🥇 Gold: Gmail Integration (monitors inbox)
   - 💎 Platinum: LinkedIn Integration (social presence)

2. **Real Automation:**
   - Runs 24/7 via cron
   - Processes real emails
   - Posts to real LinkedIn
   - Maintains logs and history

3. **Human-in-the-Loop:**
   - Approval system for safety
   - You control what gets executed
   - Transparent logging

4. **Production-Ready:**
   - Error handling
   - Credential management
   - Duplicate detection
   - Log rotation

---

## 🐛 Troubleshooting During Demo

**If Gmail watcher isn't running:**
```bash
./run_gmail_watcher.sh
```

**If no tasks in Needs_Action:**
```bash
# Create a simple test task
cat > Needs_Action/demo_task.md << 'EOF'
Write a haiku about artificial intelligence.
EOF
```

**If LinkedIn post fails:**
- Check: `cat credentials/linkedin_token.json`
- Re-authenticate if needed

**If executor finds no tasks:**
- Ensure task file is in Needs_Action/
- Ensure approval file has [x] checked

---

## 📸 Screenshots to Prepare

1. System status dashboard
2. Email task file example
3. AI-generated plan
4. Execution log
5. LinkedIn post live
6. Claude MCP email sending

---

## 🎤 Q&A Preparation

**Q: How does it handle errors?**
A: Each component has try-catch blocks, logs errors, and continues running. Failed tasks stay in Needs_Action for retry.

**Q: Is it secure?**
A: Yes - credentials are stored locally, OAuth tokens are used, and there's human approval before execution.

**Q: Can it scale?**
A: Absolutely - it's stateless, uses APIs, and can process unlimited tasks. Just add more cron jobs or run multiple instances.

**Q: What's the cost?**
A: Minimal - Gemini API is cheap, Gmail/LinkedIn APIs are free tier, runs on any Linux machine.

**Q: What else could it do?**
A: Anything with an API - Slack, GitHub, calendar, databases, file systems, web scraping, etc.

---

## ✅ Post-Demo

After the demo, share:
- GitHub repository link
- Live LinkedIn post
- Documentation files
- Demo video (if recorded)

Good luck! 🚀
