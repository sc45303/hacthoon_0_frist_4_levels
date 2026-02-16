# Personal AI Employee - Technical Architecture

**Part 2 of 5** | [← Back to Overview](understand_project.md) | [Next: How To Run →](understand_project_howto.md)

---

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL WORLD                            │
│  Gmail Inbox  │  LinkedIn  │  User Commands (via Claude)    │
└────────┬──────────────┬────────────────┬────────────────────┘
         │              │                │
         ▼              ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                    WATCHERS LAYER                            │
│  Gmail Watcher  │  LinkedIn Poster  │  File Watcher         │
└────────┬──────────────┬────────────────┬────────────────────┘
         │              │                │
         ▼              ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                  TASK QUEUE (Needs_Action/)                  │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI PLANNING LAYER                         │
│  Bronze Planner (Gemini AI) → Generates execution plans     │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                  APPROVAL LAYER (Human)                      │
│  Approvals/ folder - You review and approve                 │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                   EXECUTION LAYER                            │
│  Silver Executor → Executes approved tasks                  │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    ACTION LAYER                              │
│  MCP Servers  │  Direct Actions  │  API Calls               │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                  STORAGE & MEMORY                            │
│  Done/  │  Logs/  │  Memory/  │  Feedback/                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Component Interaction Flow

### 1. Gmail Monitoring Flow

```
Gmail Inbox (New Email)
    ↓
Gmail Watcher (Python script running via cron)
    ↓ Checks every 2 minutes
    ↓ Filters: is:unread is:important
    ↓
Detects new email
    ↓
Extracts: From, Subject, Body, Date
    ↓
Creates task file: EMAIL_[subject]_[id].md
    ↓
Saves to: Needs_Action/
    ↓
Logs to: Memory/processed_emails.json
```

### 2. Email Sending Flow (via MCP)

```
You (in Claude): "Send email to test@example.com"
    ↓
Claude Code receives command
    ↓
Calls Email MCP Server tool: send_email
    ↓
MCP Server (Node.js)
    ↓ Reads credentials/gmail_token.json
    ↓ Authenticates with Gmail API
    ↓ Creates RFC 2822 email message
    ↓ Encodes in base64
    ↓
Gmail API sends email
    ↓
Returns: Message ID + confirmation
    ↓
Claude shows you: "✅ Email sent! ID: 19c5..."
```

### 3. LinkedIn Posting Flow

```
Create post file: Posts_Queue/my_post.md
    ↓
LinkedIn Poster (Python script)
    ↓ Runs every hour via cron
    ↓ OR manually: python watchers/linkedin_poster.py
    ↓
Reads post file
    ↓ Parses frontmatter (type, visibility, url)
    ↓ Extracts content
    ↓
Authenticates with LinkedIn API
    ↓ Uses credentials/linkedin_token.json
    ↓
Creates API payload
    ↓ Text post OR Article post
    ↓
Posts to LinkedIn API
    ↓
Moves file to: Posts_Queue/posted/
    ↓
Logs to: Memory/linkedin_posts.log
```

### 4. Task Planning & Execution Flow

```
Task file appears in Needs_Action/
    ↓
Bronze Planner detects it
    ↓
Reads task content
    ↓
Sends to Gemini AI with prompt:
    "You are a Digital AI Employee. Create a plan for: [task]"
    ↓
Gemini generates step-by-step plan
    ↓
Saves plan to: Plans/[task].md
    ↓
Creates approval request: Approvals/[task].md.approval.md
    ↓
Updates memory: Memory/task_history.json
    ↓
WAITS for human approval
    ↓
You edit approval file: Change [ ] to [x] Approved
    ↓
Silver Executor detects approval
    ↓
Reads plan from Plans/
    ↓
Executes task steps
    ↓
Moves task to: Done/
    ↓
Creates log: Logs/[task].md.execution.log
    ↓
Updates memory with completion
```

---

## 🧩 Core Components Explained

### 1. Gmail Watcher (`watchers/gmail_watcher.py`)

**Purpose:** Monitor Gmail inbox and create tasks from important emails

**How it works:**
- Runs continuously (via cron every 2 minutes)
- Uses Gmail API with OAuth2 authentication
- Queries: `is:unread is:important`
- Tracks processed emails in `Memory/processed_emails.json`
- Creates task files with email metadata

**Key Functions:**
- `authenticate()` - OAuth2 flow with Gmail
- `check_inbox()` - Query for new emails
- `process_email(msg_id)` - Convert email to task file
- `run()` - Main loop

**Dependencies:**
- `google-auth` - OAuth2 authentication
- `google-api-python-client` - Gmail API client
- `pickle` - Token storage

### 2. Email MCP Server (`mcp_servers/email_mcp/index.js`)

**Purpose:** Provide email operations to Claude via MCP protocol

**How it works:**
- Node.js server using MCP SDK
- Communicates via stdio (standard input/output)
- Exposes 3 tools: send_email, draft_reply, search_emails
- Uses same Gmail credentials as watcher

**Key Tools:**
- `send_email` - Send email via Gmail
- `draft_reply` - Create draft reply to existing email
- `search_emails` - Search inbox with Gmail query syntax

**MCP Configuration:**
Located in `~/.config/claude-code/mcp_config.json`:
```json
{
  "mcpServers": {
    "email": {
      "command": "node",
      "args": ["/path/to/email_mcp/index.js"]
    }
  }
}
```

### 3. LinkedIn Auto-Poster (`watchers/linkedin_poster.py`)

**Purpose:** Automatically post content from queue to LinkedIn

**How it works:**
- Scans `Posts_Queue/` for .md files
- Parses frontmatter for post metadata
- Authenticates with LinkedIn API (OAuth2)
- Posts via LinkedIn UGC API
- Moves posted files to `Posts_Queue/posted/`

**Post Format:**
```markdown
---
type: text
visibility: PUBLIC
---

Your post content here #hashtags
```

**Key Functions:**
- `load_token()` - Load LinkedIn access token
- `parse_post_file()` - Parse markdown with frontmatter
- `create_text_post()` - Create text post payload
- `create_article_post()` - Create article/URL post payload
- `post_to_linkedin()` - Send to LinkedIn API

### 4. LinkedIn MCP Server (`mcp_servers/linkedin_mcp/index.js`)

**Purpose:** Post to LinkedIn via Claude commands

**How it works:**
- Similar to Email MCP
- Exposes 2 tools: post_to_linkedin, post_article_to_linkedin
- Uses credentials/linkedin_token.json

**Usage in Claude:**
```
"Post to LinkedIn: Check out my new AI project! #AI #automation"
```

### 5. Bronze Planner (`agent/bronze_planner.py`)

**Purpose:** Generate execution plans for tasks using AI

**How it works:**
- Reads task from Needs_Action/
- Sends to Gemini AI with planning prompt
- Receives step-by-step plan
- Saves to Plans/ folder
- Creates approval request

**AI Prompt:**
```
You are a Digital AI Employee.
Your job at Bronze level:
- Read the task
- Create a simple step-by-step plan
- Do NOT execute anything

Task: [task content]

Respond only with a clear plan.
```

### 6. Silver Executor (`agent/silver_executor.py`)

**Purpose:** Execute approved tasks autonomously

**How it works:**
- Monitors Approvals/ folder
- Detects approved tasks (marked with [x])
- Reads execution plan
- Executes task steps
- Logs results
- Moves task to Done/

**Execution Logic:**
- Simple tasks: Direct execution
- Complex tasks: Step-by-step execution
- Errors: Logged and reported

### 7. Gemini Brain (`agent/gemini_brain.py`)

**Purpose:** Interface to Google Gemini AI

**How it works:**
- Loads API key from .env file
- Creates Gemini client
- Provides `think()` function for AI reasoning
- Uses model: `gemini-2.5-flash`

**Usage:**
```python
from agent.gemini_brain import think
plan = think("Write a haiku about AI")
```

---

## 🔐 Authentication & Security

### Gmail Authentication

**Method:** OAuth2 with Google Cloud Platform

**Flow:**
1. Create project in Google Cloud Console
2. Enable Gmail API
3. Create OAuth2 credentials
4. Download `gmail_credentials.json`
5. Run authentication flow (opens browser)
6. Grant permissions
7. Token saved to `gmail_token.pickle` (Python) and `gmail_token.json` (Node.js)

**Scopes:**
- `gmail.readonly` - Read emails
- `gmail.send` - Send emails
- `gmail.compose` - Create drafts

### LinkedIn Authentication

**Method:** OAuth2 with LinkedIn Developer Portal

**Flow:**
1. Create LinkedIn App
2. Add products: "Share on LinkedIn" + "Sign In with LinkedIn using OpenID Connect"
3. Configure redirect URI: `http://localhost:8080/callback`
4. Run `authenticate_linkedin_openid.py`
5. Copy authorization URL to browser
6. Grant permissions
7. Copy code from URL
8. Exchange code for token
9. Token saved to `credentials/linkedin_token.json`

**Scopes:**
- `openid` - Basic authentication
- `profile` - User profile data
- `w_member_social` - Post to LinkedIn

---

## 📦 Data Storage

### File-Based Storage

All data stored in markdown files and JSON:

**Task Files (Markdown):**
- `Needs_Action/*.md` - New tasks
- `Plans/*.md` - Generated plans
- `Approvals/*.md` - Approval requests
- `Done/*.md` - Completed tasks
- `Logs/*.md` - Execution logs

**Memory Files (JSON):**
- `Memory/task_history.json` - Task tracking
- `Memory/processed_emails.json` - Email IDs
- `Memory/linkedin_posts.log` - Post history
- `Memory/cron_logs/*.log` - Automation logs

### Why File-Based?

1. **Obsidian Integration** - Visual GUI for free
2. **Human Readable** - Easy to inspect and edit
3. **Version Control** - Git-friendly
4. **No Database** - Simple setup
5. **Portable** - Easy backup and migration

---

## ⚙️ Automation with Cron

### Cron Jobs Installed

```bash
# Gmail Watcher - Every 2 minutes
*/2 * * * * /path/to/cron_gmail_watcher.sh

# LinkedIn Poster - Every hour
0 * * * * /path/to/cron_linkedin_poster.sh

# Log Cleanup - Daily at midnight
0 0 * * * find /path/to/Memory/cron_logs -name "*.log" -mtime +7 -delete
```

### How Cron Works

1. Cron daemon runs in background
2. Checks schedule every minute
3. Executes matching jobs
4. Logs output to files
5. Continues running 24/7

### Wrapper Scripts

**cron_gmail_watcher.sh:**
```bash
#!/bin/bash
cd /path/to/AI_Employee_Vault
source venv/bin/activate
python watchers/gmail_watcher.py >> Memory/cron_logs/gmail_watcher.log 2>&1
```

---

**Continue to: understand_project_howto.md**
