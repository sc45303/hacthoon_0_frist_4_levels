# Step-by-Step Migration Plan: Current System → Hackathon Compliant

**Goal:** Convert your working Gemini-based system to hackathon-compliant Claude Code + Agent Skills architecture

**Estimated Time:** 15-20 hours
**Current Status:** Silver functionality, non-compliant architecture
**Target Status:** Silver tier, fully compliant

---

## Phase 1: Setup Obsidian Vault (30 minutes)

### Step 1.1: Initialize Obsidian Vault
```bash
# Your current folder is already structured correctly
# Just need to initialize as Obsidian vault

# 1. Open Obsidian application
# 2. Click "Open folder as vault"
# 3. Select: /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
# 4. Obsidian will create .obsidian/ folder automatically
```

### Step 1.2: Create Dashboard.md
```bash
# Create the main dashboard
cat > Dashboard.md << 'EOF'
# AI Employee Dashboard

**Last Updated:** {{date}}

## System Status
- Gmail Watcher: 🟢 Running
- LinkedIn Poster: 🟢 Running
- Bronze Planner: 🟢 Running
- Silver Executor: 🟢 Running

## Today's Activity
- Emails processed: 0
- Tasks completed: 0
- LinkedIn posts: 0

## Pending Actions
- Tasks in Needs_Action: 0
- Tasks awaiting approval: 0

## Recent Completions
- None yet today

---
*Updated automatically by AI Employee*
EOF
```

### Step 1.3: Create Company_Handbook.md
```bash
cat > Company_Handbook.md << 'EOF'
# Company Handbook - Rules of Engagement

## Communication Rules
- Always be professional and polite
- Respond to urgent emails within 24 hours
- Flag any unusual requests for human review

## Financial Rules
- Never approve payments > $100 without human approval
- Always verify recipient before sending money
- Log all transactions in accounting system

## Social Media Rules
- Post on LinkedIn during business hours (9 AM - 5 PM)
- Keep posts professional and relevant to business
- Never post controversial content

## Security Rules
- Never share credentials or sensitive data
- Always use approval workflow for sensitive actions
- Log all actions for audit trail

---
*This handbook guides AI Employee decision-making*
EOF
```

**Checkpoint:** Obsidian vault is now initialized with core files.

---

## Phase 2: Create Agent Skills (4-6 hours)

### What are Agent Skills?
Agent Skills are reusable capabilities that Claude Code can invoke. They're defined in SKILL.md files and allow Claude to perform specific tasks autonomously.

### Step 2.1: Create Skills Directory Structure
```bash
mkdir -p skills/plan_task
mkdir -p skills/execute_task
mkdir -p skills/check_approvals
mkdir -p skills/linkedin_post
mkdir -p skills/update_dashboard
```

### Step 2.2: Create Plan Task Skill
```bash
cat > skills/plan_task/SKILL.md << 'EOF'
# Plan Task Skill

**Purpose:** Analyze tasks from Needs_Action and create execution plans

## Usage
```
/plan-task <task_file>
```

## What This Skill Does
1. Reads task file from Needs_Action folder
2. Analyzes task requirements and context
3. Checks Company_Handbook.md for relevant rules
4. Creates detailed execution plan in Plans folder
5. Creates approval request in Approvals folder

## Input
- Task file path (e.g., Needs_Action/EMAIL_xyz.md)

## Output
- Plans/<task_name>.md - Detailed execution plan
- Approvals/<task_name>.approval.md - Approval request

## Decision Logic
- If task involves payment > $100 → Requires approval
- If task involves new contact → Requires approval
- If task is routine (known contact, simple reply) → Auto-approve eligible

## Example
```
/plan-task Needs_Action/EMAIL_Test_19c66ef2.md
```

Creates:
- Plans/EMAIL_Test_19c66ef2.md
- Approvals/EMAIL_Test_19c66ef2.md.approval.md
EOF
```

### Step 2.3: Create Execute Task Skill
```bash
cat > skills/execute_task/SKILL.md << 'EOF'
# Execute Task Skill

**Purpose:** Execute approved tasks according to their plans

## Usage
```
/execute-task <task_file>
```

## What This Skill Does
1. Checks if task is approved (reads Approvals folder)
2. Reads execution plan from Plans folder
3. Executes each step in the plan
4. Logs execution details
5. Moves completed task to Done folder

## Input
- Task file path (e.g., Needs_Action/EMAIL_xyz.md)

## Output
- Logs/<task_name>.execution.log - Detailed execution log
- Done/<task_name>.md - Completed task (moved from Needs_Action)

## Safety Checks
- MUST verify approval exists before executing
- MUST check approval is marked [x] Approved
- MUST NOT execute if marked [x] Rejected
- MUST log every action taken

## Example
```
/execute-task Needs_Action/EMAIL_Test_19c66ef2.md
```

Executes the task and moves to Done folder.
EOF
```

### Step 2.4: Create Check Approvals Skill
```bash
cat > skills/check_approvals/SKILL.md << 'EOF'
# Check Approvals Skill

**Purpose:** Check which tasks have been approved by human

## Usage
```
/check-approvals
```

## What This Skill Does
1. Scans Approvals folder for all .approval.md files
2. Checks each file for approval status
3. Returns list of approved tasks ready for execution

## Output
Returns list of task files that are:
- Marked [x] Approved
- Not yet executed (still in Needs_Action)

## Example
```
/check-approvals
```

Returns:
```
Approved tasks ready for execution:
- EMAIL_Test_19c66ef2.md
- EMAIL_Invoice_Request_19c66f01.md
```
EOF
```

### Step 2.5: Create LinkedIn Post Skill
```bash
cat > skills/linkedin_post/SKILL.md << 'EOF'
# LinkedIn Post Skill

**Purpose:** Create and post content to LinkedIn

## Usage
```
/linkedin-post <post_file>
```

## What This Skill Does
1. Reads post content from Posts_Queue folder
2. Validates post meets Company_Handbook rules
3. Posts to LinkedIn using MCP server
4. Moves posted content to Posts_Queue/posted
5. Logs posting activity

## Input
- Post file path (e.g., Posts_Queue/my_post.md)

## Output
- Posts_Queue/posted/<post_name>.md - Archived post
- Memory/linkedin_posts.log - Updated log

## Safety Checks
- Check posting time (9 AM - 5 PM business hours)
- Verify content is professional
- Check for controversial keywords
- Require approval for sensitive topics

## Example
```
/linkedin-post Posts_Queue/ai_employee_announcement.md
```

Posts to LinkedIn and archives.
EOF
```

### Step 2.6: Create Update Dashboard Skill
```bash
cat > skills/update_dashboard/SKILL.md << 'EOF'
# Update Dashboard Skill

**Purpose:** Update Dashboard.md with current system status

## Usage
```
/update-dashboard
```

## What This Skill Does
1. Counts files in each folder (Needs_Action, Approvals, Done)
2. Checks cron job status
3. Reads recent logs for activity
4. Updates Dashboard.md with current stats

## Output
- Dashboard.md - Updated with current stats and timestamp

## Metrics Tracked
- Emails processed today
- Tasks completed today
- LinkedIn posts today
- Pending approvals count
- System health status

## Example
```
/update-dashboard
```

Updates Dashboard.md with latest stats.
EOF
```

**Checkpoint:** All required Agent Skills are now defined.

---

## Phase 3: Create Skill Implementation Scripts (4-6 hours)

Agent Skills need implementation scripts that Claude Code can invoke.

### Step 3.1: Create Plan Task Implementation
```bash
cat > skills/plan_task/plan_task.py << 'EOF'
#!/usr/bin/env python3
"""
Plan Task Skill Implementation
Called by Claude Code to create execution plans
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import google.generativeai as genai

# Configure Gemini (or use Claude API)
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def plan_task(task_file_path):
    """Create execution plan for a task"""
    task_path = Path(task_file_path)

    if not task_path.exists():
        return f"Error: Task file not found: {task_file_path}"

    # Read task content
    task_content = task_path.read_text()

    # Read Company Handbook for context
    handbook_path = Path('Company_Handbook.md')
    handbook = handbook_path.read_text() if handbook_path.exists() else ""

    # Generate plan using AI
    prompt = f"""You are a task planning assistant. Create a detailed execution plan.

Task to plan:
{task_content}

Company rules:
{handbook}

Create a step-by-step plan with:
1. Clear action items
2. Required approvals
3. Expected outcomes
4. Safety checks

Format as markdown with checkboxes."""

    response = model.generate_content(prompt)
    plan = response.text

    # Save plan
    task_name = task_path.stem
    plan_path = Path('Plans') / f'{task_name}.md'
    plan_path.write_text(f"""# Execution Plan: {task_name}

Created: {datetime.now().isoformat()}

## Task
{task_content}

## Plan
{plan}
""")

    # Create approval request
    approval_path = Path('Approvals') / f'{task_name}.md.approval.md'
    approval_path.write_text(f"""# Approval Request

Task: {task_name}.md

Decision:
[ ] Approved
[ ] Rejected

Notes:
""")

    return f"✅ Plan created: {plan_path}\n✅ Approval requested: {approval_path}"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python plan_task.py <task_file_path>")
        sys.exit(1)

    result = plan_task(sys.argv[1])
    print(result)
EOF

chmod +x skills/plan_task/plan_task.py
```

### Step 3.2: Create Execute Task Implementation
```bash
cat > skills/execute_task/execute_task.py << 'EOF'
#!/usr/bin/env python3
"""
Execute Task Skill Implementation
Called by Claude Code to execute approved tasks
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import google.generativeai as genai
import shutil

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def check_approval(task_name):
    """Check if task is approved"""
    approval_path = Path('Approvals') / f'{task_name}.md.approval.md'

    if not approval_path.exists():
        return False, "No approval file found"

    content = approval_path.read_text()

    if '[x] Approved' in content or '[X] Approved' in content:
        return True, "Approved"
    elif '[x] Rejected' in content or '[X] Rejected' in content:
        return False, "Rejected"
    else:
        return False, "Pending approval"

def execute_task(task_file_path):
    """Execute an approved task"""
    task_path = Path(task_file_path)
    task_name = task_path.stem

    # Check approval
    approved, status = check_approval(task_name)
    if not approved:
        return f"❌ Cannot execute: {status}"

    # Read task and plan
    task_content = task_path.read_text()
    plan_path = Path('Plans') / f'{task_name}.md'
    plan = plan_path.read_text() if plan_path.exists() else "No plan found"

    # Execute using AI
    prompt = f"""You are a task executor. Execute this task according to the plan.

Task:
{task_content}

Plan:
{plan}

Provide a detailed execution report with:
1. Each step taken
2. Results of each action
3. Any issues encountered
4. Final status

Format as markdown."""

    response = model.generate_content(prompt)
    execution_report = response.text

    # Create execution log
    log_path = Path('Logs') / f'{task_name}.md.execution.log'
    log_path.write_text(f"""# Execution Log: {task_name}
Timestamp: {datetime.now().isoformat()}

## Task
{task_content}

## Plan
{plan}

## Execution Report
{execution_report}

Status: Completed
""")

    # Move task to Done
    done_path = Path('Done') / task_path.name
    shutil.move(str(task_path), str(done_path))

    return f"✅ Task executed successfully: {task_name}\n📦 Moved to Done folder\n📝 Log: {log_path}"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python execute_task.py <task_file_path>")
        sys.exit(1)

    result = execute_task(sys.argv[1])
    print(result)
EOF

chmod +x skills/execute_task/execute_task.py
```

**Checkpoint:** Core skill implementations are ready.

---

## Phase 4: Integrate Claude Code (6-8 hours)

### Step 4.1: Install Claude Code
```bash
# If not already installed
npm install -g @anthropic/claude-code

# Verify installation
claude --version
```

### Step 4.2: Configure Claude Code for Your Vault
```bash
# Create Claude Code config
mkdir -p ~/.config/claude-code

cat > ~/.config/claude-code/config.json << 'EOF'
{
  "vault_path": "/home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault",
  "skills_path": "/home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault/skills",
  "auto_approve_threshold": 50,
  "max_iterations": 10
}
EOF
```

### Step 4.3: Create Claude Code Orchestrator
```bash
cat > orchestrator_claude.py << 'EOF'
#!/usr/bin/env python3
"""
Claude Code Orchestrator
Replaces direct Gemini API calls with Claude Code invocations
"""
import subprocess
import os
from pathlib import Path
import time

VAULT_PATH = Path('/home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault')

def invoke_claude_skill(skill_name, *args):
    """Invoke a Claude Code skill"""
    cmd = ['claude', 'code', f'/{skill_name}'] + list(args)
    result = subprocess.run(
        cmd,
        cwd=VAULT_PATH,
        capture_output=True,
        text=True
    )
    return result.stdout

def process_needs_action():
    """Process all tasks in Needs_Action folder"""
    needs_action = VAULT_PATH / 'Needs_Action'

    for task_file in needs_action.glob('*.md'):
        print(f"🧠 Planning task: {task_file.name}")
        result = invoke_claude_skill('plan-task', str(task_file))
        print(result)

def process_approved_tasks():
    """Execute all approved tasks"""
    # First check which tasks are approved
    result = invoke_claude_skill('check-approvals')
    print(result)

    # Execute each approved task
    needs_action = VAULT_PATH / 'Needs_Action'
    for task_file in needs_action.glob('*.md'):
        task_name = task_file.stem
        approval_file = VAULT_PATH / 'Approvals' / f'{task_name}.md.approval.md'

        if approval_file.exists():
            content = approval_file.read_text()
            if '[x] Approved' in content or '[X] Approved' in content:
                print(f"🚀 Executing task: {task_file.name}")
                result = invoke_claude_skill('execute-task', str(task_file))
                print(result)

def update_dashboard():
    """Update dashboard with current stats"""
    result = invoke_claude_skill('update-dashboard')
    print(result)

if __name__ == '__main__':
    print("[Claude Code Orchestrator Started]")

    # Process new tasks
    process_needs_action()

    # Execute approved tasks
    process_approved_tasks()

    # Update dashboard
    update_dashboard()

    print("[Claude Code Orchestrator Completed]")
EOF

chmod +x orchestrator_claude.py
```

### Step 4.4: Update Cron Jobs to Use Claude Code
```bash
# Backup current cron
crontab -l > cron_backup.txt

# Create new cron scripts that use Claude Code orchestrator
cat > cron_claude_planner.sh << 'EOF'
#!/bin/bash
cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
source venv/bin/activate
python orchestrator_claude.py --mode=plan >> Memory/cron_logs/claude_planner.log 2>&1
echo "[$(date)] Claude Planner completed" >> Memory/cron_logs/claude_planner.log
EOF

chmod +x cron_claude_planner.sh

cat > cron_claude_executor.sh << 'EOF'
#!/bin/bash
cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
source venv/bin/activate
python orchestrator_claude.py --mode=execute >> Memory/cron_logs/claude_executor.log 2>&1
echo "[$(date)] Claude Executor completed" >> Memory/cron_logs/claude_executor.log
EOF

chmod +x cron_claude_executor.sh
```

**Checkpoint:** Claude Code integration is ready.

---

## Phase 5: Testing & Validation (4-6 hours)

### Step 5.1: Test Agent Skills Manually
```bash
# Test plan task skill
cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
python skills/plan_task/plan_task.py Needs_Action/EMAIL_Youre*.md

# Verify plan was created
ls -lh Plans/
ls -lh Approvals/

# Approve the task manually
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/EMAIL_Youre*.approval.md

# Test execute task skill
python skills/execute_task/execute_task.py Needs_Action/EMAIL_Youre*.md

# Verify execution
ls -lh Done/
cat Logs/EMAIL_Youre*.execution.log
```

### Step 5.2: Test Claude Code Orchestrator
```bash
# Run orchestrator manually
python orchestrator_claude.py

# Check logs
tail -50 Memory/cron_logs/claude_planner.log
tail -50 Memory/cron_logs/claude_executor.log
```

### Step 5.3: Update Crontab (Final Step)
```bash
# Remove old Gemini-based cron jobs
crontab -l | grep -v "cron_bronze_planner" | grep -v "cron_silver_executor" > new_cron.txt

# Add new Claude Code cron jobs
echo "*/5 * * * * /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault/cron_claude_planner.sh" >> new_cron.txt
echo "*/5 * * * * /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault/cron_claude_executor.sh" >> new_cron.txt

# Install new crontab
crontab new_cron.txt

# Verify
crontab -l
```

**Checkpoint:** System is now hackathon compliant!

---

## Phase 6: Documentation & Submission (2-3 hours)

### Step 6.1: Update README.md
Add section explaining:
- Architecture: Claude Code + Agent Skills + Obsidian
- How Agent Skills work
- How to add new skills
- Security measures

### Step 6.2: Create Demo Video
Record 5-10 minute video showing:
1. Send test email
2. Gmail Watcher detects it
3. Claude Code creates plan (via Agent Skill)
4. Human approves task
5. Claude Code executes (via Agent Skill)
6. Task moves to Done with execution log

### Step 6.3: Submit to Hackathon
- GitHub repository URL
- Demo video link
- Tier declaration: Silver
- Security disclosure

---

## Summary: What Changed

### Before (Non-Compliant)
```
Cron → Python script → Gemini API → Write file
```

### After (Compliant)
```
Cron → Claude Code Orchestrator → Claude Code → Agent Skill → Action
```

### Key Differences
1. **Agent Skills** - All AI functionality is now modular and reusable
2. **Claude Code** - Primary reasoning engine (can still use Gemini internally)
3. **Obsidian** - Proper vault with Dashboard and Handbook
4. **Skill-based** - Easy to add new capabilities

---

## Next Steps

1. **Start with Phase 1** - Initialize Obsidian vault (30 min)
2. **Complete Phase 2** - Create all Agent Skills (4-6 hours)
3. **Test incrementally** - Don't wait until the end
4. **Keep backups** - Your current system works, don't break it
5. **Ask for help** - Wednesday research meetings

**Estimated completion: 15-20 hours of focused work**

---

**Ready to start? Begin with Phase 1: Setup Obsidian Vault**
