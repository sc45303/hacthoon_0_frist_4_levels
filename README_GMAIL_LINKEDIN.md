# 🤖 Personal AI Employee - Digital FTE System

> A complete autonomous AI agent system that monitors emails, plans tasks, executes actions, and manages social media - all running 24/7.

[![Status](https://img.shields.io/badge/status-production-success)]()
[![AI](https://img.shields.io/badge/AI-Gemini-blue)]()
[![Automation](https://img.shields.io/badge/automation-24%2F7-orange)]()
[![Levels](https://img.shields.io/badge/Levels-4%2F4-blue)]()

**Hackathon:** Personal AI Employee - Building Autonomous FTEs in 2026
**Status:** All 4 Levels Complete ✅

---

## 🎯 What It Does

This is a **true Digital Full-Time Employee (FTE)** - an AI system that handles real work autonomously:

- 📧 **Monitors Gmail** every 2 minutes for important emails
- 🧠 **Plans tasks** using Gemini AI with strategic thinking
- ⚡ **Executes actions** autonomously after human approval
- 🔗 **Posts to LinkedIn** automatically on schedule
- 📝 **Maintains logs** of every action taken
- 🔄 **Runs 24/7** via cron automation
- 💬 **Claude MCP integration** for conversational email sending

---

## 🏆 Four Levels Implemented

### 🥉 Bronze Level - The Planner
**What it does:**
- Analyzes incoming tasks from Needs_Action folder
- Creates step-by-step execution plans using Gemini AI
- Generates approval requests for human review
- Saves plans to Plans/ folder

**Example:**
```bash
python -m agent.bronze_planner
# Creates plan and approval request for all tasks in Needs_Action/
```

### 🥈 Silver Level - The Executor
**What it does:**
- Executes approved plans autonomously
- Logs every action in detail
- Moves completed tasks to Done/ folder
- Maintains execution history

**Example:**
```bash
python -m agent.silver_executor
# Executes all approved tasks and creates detailed logs
```

### 🥇 Gold Level - Gmail Integration
**What it does:**
- Monitors Gmail inbox automatically (every 2 minutes)
- Detects unread emails
- Creates structured task files in Needs_Action/
- Prevents duplicate processing with email ID tracking
- Runs 24/7 via cron job

**Example:**
```bash
python watchers/gmail_watcher.py
# Starts monitoring Gmail inbox
```

**Real stats:** 31 emails processed automatically ✅

### 💎 Platinum Level - LinkedIn Integration
**What it does:**
- Auto-posts content to LinkedIn on schedule
- Manages post queue in Posts_Queue/
- Archives published content
- Supports text posts with hashtags
- Runs hourly via cron job

**Example:**
```bash
# Create post
cat > Posts_Queue/my_post.md << 'EOF'
---
type: text
visibility: PUBLIC
---

Your post content here #hashtags
EOF

# Post immediately
python watchers/linkedin_poster.py
```

**Real stats:** 2 posts published to LinkedIn ✅

---

## 📊 Real Usage Statistics

- ✅ **31 emails** processed automatically
- ✅ **4 tasks** completed by AI
- ✅ **2 LinkedIn posts** published
- ✅ **3 cron jobs** running 24/7
- ✅ **100% uptime** since deployment

---

## 🛠️ Tech Stack

- **Python** - Core automation and AI agents
- **Node.js** - MCP server for Claude integration
- **Gemini AI** - Task planning and execution
- **Gmail API** - Email monitoring and sending
- **LinkedIn API** - Social media automation
- **Claude MCP** - Conversational AI integration
- **Cron** - 24/7 scheduling

---

## 🚀 Quick Start

### Prerequisites
```bash
- Python 3.8+
- Node.js 16+
- Gmail API credentials
- LinkedIn API credentials
- Gemini API key
```

### Installation
```bash
# 1. Clone repository
cd AI_Employee_Vault

# 2. Install Python dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Install Node.js dependencies (MCP server)
cd mcp_servers/email_mcp
npm install
cd ../..

# 4. Configure credentials
cp .env.example .env
# Edit .env with your API keys
```

### Setup
```bash
# Authenticate Gmail
python watchers/gmail_watcher.py
# Follow the authentication prompts

# Authenticate LinkedIn
python authenticate_linkedin_openid.py
# Follow the authentication prompts

# Setup cron jobs
./setup_cron.sh

# Start Gmail watcher
./run_gmail_watcher.sh
```

---

## 💡 How It Works

### Complete Workflow Example

1. **Email arrives** → Gmail Watcher detects it (within 2 minutes)
2. **Task created** → Structured file saved to `Needs_Action/EMAIL_subject_id.md`
3. **AI plans** → Bronze Planner creates execution strategy
4. **Human approves** → Review and approve the plan in `Approvals/`
5. **AI executes** → Silver Executor completes the task
6. **Logged & archived** → Detailed log saved, task moved to `Done/`

### Architecture Diagram

```
┌─────────────┐
│ Gmail API   │──┐
└─────────────┘  │
                 ├──> Watcher ──> Task Files ──> Planner (AI)
┌─────────────┐  │                                    │
│ User Input  │──┘                                    ▼
└─────────────┘                              Approval Request
                                                      │
                                                      ▼
                                              Executor (AI)
                                                      │
                                                      ▼
                                              Done + Logs
                                                      │
┌─────────────┐                                      │
│LinkedIn API │◄─── Poster ◄─── Post Queue ◄─────────┘
└─────────────┘
```

---

## 📁 Project Structure

```
AI_Employee_Vault/
├── agent/                  # AI agents (Bronze, Silver)
│   ├── bronze_planner.py   # Task planning with Gemini
│   ├── silver_executor.py  # Task execution
│   └── gemini_brain.py     # LLM integration
├── watchers/              # Monitoring services
│   ├── gmail_watcher.py    # Email monitoring
│   └── linkedin_poster.py  # Social media posting
├── mcp_servers/           # Claude MCP integration
│   └── email_mcp/         # Email sending via Claude
├── Needs_Action/          # Incoming tasks
├── Plans/                 # AI-generated plans
├── Approvals/             # Human approval requests
├── Done/                  # Completed tasks
├── Logs/                  # Execution logs
├── Posts_Queue/           # LinkedIn post queue
│   └── posted/            # Published posts archive
├── Memory/                # System memory & history
│   ├── processed_emails.json
│   ├── task_history.json
│   └── cron_logs/         # Automation logs
└── credentials/           # API credentials
```

---

## 🎬 Demo

See `DEMO_SCRIPT.md` for complete walkthrough.

### Quick Demo

```bash
# 1. Check system status
bash status.sh

# 2. Create a test task
echo "Write a haiku about AI" > Needs_Action/test.md

# 3. Run the workflow
source venv/bin/activate
python -m agent.bronze_planner

# 4. Approve the plan
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/test.md.approval.md

# 5. Execute
python -m agent.silver_executor

# 6. Check results
cat Done/test.md
cat Logs/test.md.execution.log
```

### Live Email Detection Demo

```bash
# Start watcher
./run_gmail_watcher.sh

# Send yourself an email
# Watch it appear in Needs_Action/ within 2 minutes

# Monitor in real-time
watch -n 5 'ls -lh Needs_Action/'
```

### LinkedIn Posting Demo

```bash
# Quick post
./quick_post.sh "Demo of my AI Employee! #hackathon #AI"

# Check your LinkedIn profile - post is live!
```

---

## 🔐 Security

- OAuth 2.0 for Gmail and LinkedIn
- Credentials stored locally in `credentials/`
- Human-in-the-loop approval system
- No sensitive data in logs
- Token refresh handled automatically
- Email IDs tracked to prevent duplicates

---

## 📚 Documentation

- `DEMO_SCRIPT.md` - Complete demo walkthrough
- `FRESH_TESTING_GUIDE.md` - Step-by-step testing
- `QUICK_REFERENCE.md` - Quick commands
- `EMAIL_SENDING_GUIDE.md` - MCP email setup
- `LINKEDIN_POSTER_GUIDE.md` - LinkedIn integration

---

## 🧪 Testing

### Test Complete Workflow

```bash
# 1. Create task
echo "Create a professional email signature" > Needs_Action/demo.md

# 2. Generate plan
source venv/bin/activate
python -m agent.bronze_planner

# 3. View plan
cat Plans/demo.md

# 4. Approve
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/demo.md.approval.md

# 5. Execute
python -m agent.silver_executor

# 6. Check results
cat Done/demo.md
cat Logs/demo.md.execution.log
```

---

## 🤖 MCP Integration

Send emails via Claude Code:

```
In Claude Code, say:
"Send an email to someone@example.com with subject 'Hello'
and body 'This is automated!'"
```

The MCP server handles authentication and sending via Gmail API.

---

## ⚙️ Automation (Cron Jobs)

Three cron jobs run automatically:

```bash
# Gmail watcher - every 2 minutes
*/2 * * * * /path/to/cron_gmail_watcher.sh

# LinkedIn poster - every hour
0 * * * * /path/to/cron_linkedin_poster.sh

# Log cleanup - daily at midnight
0 0 * * * find /path/to/cron_logs -name "*.log" -mtime +7 -delete
```

View active jobs:
```bash
crontab -l
```

---

## 🐛 Troubleshooting

### Gmail Watcher Not Running
```bash
ps aux | grep gmail_watcher
# If not running:
./run_gmail_watcher.sh
```

### No Tasks Detected
- Ensure emails are unread
- Check: `tail -f Memory/cron_logs/gmail_watcher.log`
- Verify credentials: `ls credentials/gmail_token.pickle`

### LinkedIn Post Failed
- Check token: `cat credentials/linkedin_token.json`
- Re-authenticate: `python authenticate_linkedin_openid.py`

### Task Not Executing
- Verify approval: `cat Approvals/task.md.approval.md | grep "\[x\]"`
- Check plan exists: `ls Plans/task.md`
- View logs: `cat Logs/task.md.execution.log`

---

## 📈 Future Enhancements

- [ ] Slack integration
- [ ] Calendar management
- [ ] GitHub automation
- [ ] Multi-language support
- [ ] Web dashboard
- [ ] Mobile notifications
- [ ] WhatsApp integration
- [ ] Banking automation

---

## 🎓 Key Features

### ✅ Autonomous Operation
- Detects and processes tasks automatically
- No manual intervention after approval
- Handles errors gracefully
- Runs 24/7 via cron

### ✅ Real-World Integration
- Gmail API for email monitoring
- LinkedIn API for social presence
- Claude MCP for conversational AI
- Production-ready automation

### ✅ Safety Features
- Human-in-the-loop approval workflow
- Detailed audit logging
- Error handling and recovery
- Complete transparency

### ✅ Scalability
- Stateless design
- API-based architecture
- Can process unlimited tasks
- Easy to add new integrations

---

## 📝 License

Built for the Personal AI Employee Hackathon 2026.

---

## 🙏 Acknowledgments

- Hackathon organizers for the challenge
- Google Gemini for LLM capabilities
- Gmail & LinkedIn APIs
- Anthropic Claude for MCP integration

---

## 👤 Author

**Suhail Khan**
- Email: sc3078745@gmail.com
- LinkedIn: [Your Profile]

---

## 📧 Contact

For questions or issues, refer to documentation files or create an issue.

---

**Built with ❤️ for the Personal AI Employee Hackathon 2026**

*This is what a true Digital FTE looks like - an AI that handles routine work so humans can focus on what matters.*
