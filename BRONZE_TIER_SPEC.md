# 🥉 BRONZE TIER - THE PLANNER
## Complete Implementation Specification

---

## 📋 Hackathon Requirements (Official)

**From Hackathon Document:**

> **Bronze Tier: Foundation (Minimum Viable Deliverable)**
> **Estimated time:** 8-12 hours
>
> **Requirements:**
> - Obsidian vault with Dashboard.md and Company_Handbook.md
> - One working Watcher script (Gmail OR file system monitoring)
> - Claude Code successfully reading from and writing to the vault
> - Basic folder structure: /Inbox, /Needs_Action, /Done
> - All AI functionality should be implemented as Agent Skills

---

## ✅ Current Status

### What You Already Have:
- ✅ Obsidian vault configured
- ✅ Dashboard.md created
- ✅ Company_Handbook.md created
- ✅ File watcher (`watchers/file_watcher.py`)
- ✅ Basic folder structure
- ✅ AI planning system (`agent/bronze_planner.py`)
- ✅ Memory management (`agent/memory_manager.py`)
- ✅ Approval workflow (`agent/approval_manager.py`)

### What's Missing for TRUE Bronze Tier:
- ❌ Gmail Watcher OR enhanced file watcher
- ❌ Claude Code integration (you're using Gemini instead)
- ❌ Agent Skills implementation

---

## 🎯 Bronze Tier Goals

The Bronze tier AI employee should:
1. **Detect** new tasks automatically
2. **Generate** execution plans using AI
3. **Request** human approval before acting
4. **Store** task history in memory
5. **Monitor** either Gmail OR local files continuously

---

## 🏗️ Required File Structure

```
AI_Employee_Vault/
├── .obsidian/              # Obsidian configuration (✅ EXISTS)
├── Dashboard.md            # Status dashboard (✅ EXISTS)
├── Company_Handbook.md     # Rules and guidelines (✅ EXISTS)
├── Needs_Action/           # Input: New tasks (✅ EXISTS)
├── Plans/                  # Generated plans (✅ EXISTS)
├── Approvals/              # Approval requests (✅ EXISTS)
├── Done/                   # Completed tasks (✅ EXISTS)
├── Memory/                 # Task history (✅ EXISTS)
├── Logs/                   # System logs (✅ EXISTS)
├── watchers/               # Watcher scripts (✅ EXISTS)
│   ├── file_watcher.py     # (✅ EXISTS)
│   └── gmail_watcher.py    # (❌ MISSING - OPTIONAL)
├── agent/                  # AI modules (✅ EXISTS)
│   ├── bronze_planner.py   # (✅ EXISTS)
│   ├── memory_manager.py   # (✅ EXISTS)
│   └── approval_manager.py # (✅ EXISTS)
└── requirements.txt        # Dependencies (✅ EXISTS)
```

---

## 📝 Required Files - Detailed Specifications

### 1. Dashboard.md (✅ COMPLETE)

**Purpose:** Real-time status overview

**Required Content:**
```markdown
# AI Employee Dashboard

## Current Level: Bronze - The Planner

## Status
System: Active, Monitoring

## Capabilities
- Task detection and monitoring
- Plan generation using AI
- Memory system for task history
- Approval workflow

## Workflow
1. 📥 New task added to Needs_Action/
2. 🧠 AI generates plan → Plans/
3. ✋ Approval request → Approvals/
4. ✅ Human approves task
5. 📝 Task logged to Memory/

## Performance Metrics
- Total Tasks Detected: X
- Plans Generated: X
- Awaiting Approval: X

## Last Update
[Timestamp]
```

**Status:** ✅ You have this

---

### 2. Company_Handbook.md (✅ COMPLETE)

**Purpose:** Rules of engagement for AI

**Required Content:**
```markdown
# Company Handbook – AI Employee Rules

## Your Role
You are a Digital Full-Time Employee (FTE).
You help manage tasks using files.

## Rules
1. Always read tasks from Needs_Action.
2. Always create a plan before doing work.
3. Never perform risky actions.
4. Always ask for approval if unsure.
5. Move completed tasks to Done.
6. Update Dashboard after each task.

## Safety
- No financial actions without approval.
- No sending messages without approval.
- No deleting important files.

## Goal
Help the human by organizing and planning work.
```

**Status:** ✅ You have this

---

### 3. watchers/file_watcher.py (✅ COMPLETE)

**Purpose:** Monitor Needs_Action folder for new tasks

**Required Functionality:**
- Watch Needs_Action/ folder continuously
- Detect new .md files
- Detect modifications to existing files
- Trigger planning process
- Log all detections

**Your Implementation:** ✅ WORKING

**Code Structure:**
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        # Detect new task file
        # Log detection
        # Trigger planner

    def on_modified(self, event):
        # Detect task updates
        # Log modification

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(Handler(), WATCH_FOLDER)
    observer.start()
    # Keep running
```

**Status:** ✅ You have this

---

### 4. watchers/gmail_watcher.py (❌ OPTIONAL FOR BRONZE)

**Purpose:** Monitor Gmail inbox for important emails

**Required Functionality:**
- Connect to Gmail API using OAuth2
- Check inbox every 2 minutes
- Filter for important/unread emails
- Create task files in Needs_Action/
- Mark emails as processed

**Implementation Specification:**

```python
# watchers/gmail_watcher.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from pathlib import Path
import time
import json

class GmailWatcher:
    def __init__(self, vault_path: str, credentials_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.creds = Credentials.from_authorized_user_file(credentials_path)
        self.service = build('gmail', 'v1', credentials=self.creds)
        self.processed_ids = set()

    def check_inbox(self):
        """Check for new important emails"""
        results = self.service.users().messages().list(
            userId='me',
            q='is:unread is:important'
        ).execute()

        messages = results.get('messages', [])

        for msg in messages:
            if msg['id'] not in self.processed_ids:
                self.process_email(msg['id'])
                self.processed_ids.add(msg['id'])

    def process_email(self, msg_id: str):
        """Convert email to task file"""
        msg = self.service.users().messages().get(
            userId='me',
            id=msg_id
        ).execute()

        # Extract headers
        headers = {h['name']: h['value']
                  for h in msg['payload']['headers']}

        # Create task file
        task_content = f"""---
type: email
from: {headers.get('From', 'Unknown')}
subject: {headers.get('Subject', 'No Subject')}
received: {headers.get('Date', 'Unknown')}
priority: high
---

## Email Content
{msg.get('snippet', '')}

## Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
"""

        task_file = self.needs_action / f'EMAIL_{msg_id}.md'
        task_file.write_text(task_content)
        print(f"📧 Created task from email: {headers.get('Subject')}")

    def run(self):
        """Main loop"""
        print("👀 Watching Gmail inbox...")
        while True:
            try:
                self.check_inbox()
                time.sleep(120)  # Check every 2 minutes
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(60)

if __name__ == "__main__":
    watcher = GmailWatcher(
        vault_path='/path/to/AI_Employee_Vault',
        credentials_path='credentials.json'
    )
    watcher.run()
```

**Setup Requirements:**
1. Enable Gmail API in Google Cloud Console
2. Download OAuth2 credentials
3. Run authentication flow once
4. Store credentials.json securely

**Status:** ❌ NOT IMPLEMENTED (Optional for Bronze)

---

### 5. agent/bronze_planner.py (✅ COMPLETE)

**Purpose:** Generate execution plans for tasks

**Required Functionality:**
- Read tasks from Needs_Action/
- Analyze task requirements
- Generate step-by-step plan
- Create plan file in Plans/
- Create approval request in Approvals/
- Update memory

**Your Implementation:** ✅ WORKING

**Expected Output Format:**
```markdown
# Execution Plan: [Task Name]

## Task Summary
[Brief description]

## Steps
1. [ ] Step 1 description
2. [ ] Step 2 description
3. [ ] Step 3 description

## Resources Needed
- Resource 1
- Resource 2

## Estimated Complexity
Low / Medium / High

## Approval Required
Yes / No

## Generated By
AI Planner (Bronze Level)

## Timestamp
[ISO timestamp]
```

**Status:** ✅ You have this

---

### 6. agent/memory_manager.py (✅ COMPLETE)

**Purpose:** Store and retrieve task history

**Required Functionality:**
- Save task metadata to JSON
- Track task lifecycle (created → planned → approved → done)
- Provide search/retrieval functions
- Calculate statistics

**Data Structure:**
```json
{
  "tasks": [
    {
      "id": "task_001",
      "name": "example_task.md",
      "created": "2026-02-12T10:00:00Z",
      "status": "planned",
      "plan_generated": "2026-02-12T10:05:00Z",
      "approved": null,
      "completed": null,
      "complexity": "medium"
    }
  ],
  "statistics": {
    "total_tasks": 1,
    "plans_generated": 1,
    "awaiting_approval": 1,
    "completed": 0
  }
}
```

**Status:** ✅ You have this

---

### 7. agent/approval_manager.py (✅ COMPLETE)

**Purpose:** Manage human approval workflow

**Required Functionality:**
- Create approval request files
- Check approval status
- Handle approvals/rejections
- Log approval decisions

**Approval File Format:**
```markdown
# Approval Request: [Task Name]

## Task Description
[Task content]

## Generated Plan
[Link to plan file or inline summary]

## Approval Decision

[ ] Approved - Proceed with execution
[ ] Rejected - Do not execute
[ ] Needs Modification - See comments below

## Comments
[Space for human feedback]

## Instructions
To approve: Change [ ] to [x] next to "Approved"
To reject: Change [ ] to [x] next to "Rejected"

## Timestamp
[ISO timestamp]
```

**Status:** ✅ You have this

---

## 🧪 Testing Procedures

### Test 1: File Watcher Detection
```bash
# Terminal 1: Start watcher
cd AI_Employee_Vault
source venv/bin/activate
python watchers/file_watcher.py

# Terminal 2: Create test task
echo "Write a haiku about technology" > Needs_Action/test_task.md

# Expected: Watcher detects file and logs it
```

### Test 2: Plan Generation
```bash
# Create task
echo "Explain quantum computing in simple terms" > Needs_Action/quantum.md

# Run planner
python -m agent.bronze_planner

# Expected outputs:
# - Plans/quantum.md (execution plan)
# - Approvals/quantum.md.approval.md (approval request)
# - Memory/task_history.json (updated)
```

### Test 3: Memory System
```bash
# Check memory
cat Memory/task_history.json

# Expected: JSON with task records
```

### Test 4: Approval Workflow
```bash
# Check approval file
cat Approvals/quantum.md.approval.md

# Approve manually
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/quantum.md.approval.md

# Verify approval
python -m agent.approval_manager
```

---

## ✅ Completion Criteria

Bronze Tier is COMPLETE when:

- [x] Obsidian vault configured
- [x] Dashboard.md exists and is updated
- [x] Company_Handbook.md exists with rules
- [x] Folder structure created (/Needs_Action, /Plans, /Approvals, /Done, /Memory)
- [x] File watcher running and detecting tasks
- [ ] Gmail watcher running (OPTIONAL - OR file watcher)
- [x] Bronze planner generating plans
- [x] Approval workflow functional
- [x] Memory system tracking tasks
- [x] All tests passing

**Your Status:** ✅ BRONZE TIER COMPLETE (with file watcher)

---

## 🎓 What Bronze Tier Achieves

At Bronze tier, your AI employee can:
- ✅ Detect new tasks automatically
- ✅ Generate intelligent execution plans
- ✅ Request human approval
- ✅ Track task history
- ✅ Maintain organized workspace

At Bronze tier, your AI employee CANNOT:
- ❌ Execute tasks autonomously (that's Silver)
- ❌ Learn from feedback (that's Gold)
- ❌ Coordinate multiple agents (that's Platinum)

---

## 📚 Dependencies

```txt
# requirements.txt for Bronze Tier
watchdog>=3.0.0          # File system monitoring
google-generativeai>=0.3.0  # AI (Gemini)
python-dotenv>=1.0.0     # Environment variables

# Optional for Gmail watcher:
google-auth>=2.16.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
google-api-python-client>=2.80.0
```

---

## 🚀 Next Steps

After completing Bronze:
1. Move to Silver Tier (autonomous execution)
2. Add Gmail watcher if not done
3. Implement task execution logic
4. Add detailed logging

---

**Bronze Tier Specification Complete**
**Version:** 1.0
**Date:** 2026-02-12
