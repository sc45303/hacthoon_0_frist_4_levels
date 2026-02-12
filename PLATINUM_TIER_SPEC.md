# 💎 PLATINUM TIER - THE COLLABORATOR
## Complete Implementation Specification

---

## 📋 Hackathon Requirements (Official)

**From Hackathon Document:**

> **Platinum Tier: Always-On Cloud + Local Executive (Production-ish AI Employee)**
> **Estimated time:** 60+ hours
>
> **Requirements:**
> - All Gold requirements plus:
> - Run the AI Employee on Cloud 24/7 (always-on watchers + orchestrator + health monitoring)
> - Work-Zone Specialization (domain ownership):
>   - Cloud owns: Email triage + draft replies + social post drafts/scheduling
>   - Local owns: approvals, WhatsApp session, payments/banking, final "send/post" actions
> - Delegation via Synced Vault (Phase 1)
> - Agents communicate by writing files into: /Needs_Action/<domain>/, /Plans/<domain>/, /Pending_Approval/<domain>/
> - Prevent double-work using: /In_Progress/<agent>/ claim-by-move rule
> - For Vault sync use Git (recommended) or Syncthing
> - Security rule: Vault sync includes only markdown/state. Secrets never sync
> - Deploy Odoo Community on a Cloud VM (24/7) with HTTPS, backups, and health monitoring
> - Optional A2A Upgrade (Phase 2): Replace some file handoffs with direct A2A messages
> - Platinum demo: Email arrives while Local is offline → Cloud drafts reply + writes approval file → when Local returns, user approves → Local executes send via MCP → logs → moves task to /Done

---

## ✅ Current Status

### What You Already Have:
- ✅ Platinum executor (`agent/platinum_executor.py`)
- ✅ Platinum orchestrator (`agent/platinum_orchestrator.py`)
- ✅ Agent coordinator (`agent/agent_coordinator.py`)
- ✅ Task decomposer (`agent/task_decomposer.py`)
- ✅ Communication bus (`agent/communication_bus.py`)
- ✅ Agent registry (`agent/agent_registry.py`)
- ✅ 4 specialized agents (Researcher, Writer, Analyst, Coder)

### What's Missing for TRUE Platinum Tier:
- ❌ Cloud deployment (24/7 operation)
- ❌ Work-zone specialization (Cloud vs Local)
- ❌ Vault synchronization (Git/Syncthing)
- ❌ Claim-by-move rule implementation
- ❌ Health monitoring system
- ❌ Cloud Odoo deployment
- ❌ A2A communication (optional)

---

## 🎯 Platinum Tier Goals

The Platinum tier AI employee should:
1. **Run 24/7** on cloud infrastructure
2. **Specialize** work between Cloud and Local agents
3. **Synchronize** vault state via Git
4. **Prevent** double-work with claim-by-move
5. **Monitor** health and auto-recover
6. **Deploy** Odoo on cloud with HTTPS
7. **Communicate** agent-to-agent (optional)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    CLOUD AGENT (24/7)                    │
│  - Email triage                                          │
│  - Draft replies                                         │
│  - Social post drafts                                    │
│  - Scheduling                                            │
│  - Odoo integration                                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Git Sync (Vault)
                     │
┌────────────────────┴────────────────────────────────────┐
│                   LOCAL AGENT (On-demand)                │
│  - Approvals                                             │
│  - WhatsApp session                                      │
│  - Banking/payments                                      │
│  - Final send/post actions                              │
└─────────────────────────────────────────────────────────┘
```

---

## 🏗️ Required New Files

```
AI_Employee_Vault/
├── cloud/                      # ❌ MISSING
│   ├── cloud_orchestrator.py
│   ├── health_monitor.py
│   └── sync_manager.py
├── local/                      # ❌ MISSING
│   ├── local_orchestrator.py
│   └── approval_handler.py
├── In_Progress/                # ❌ MISSING
│   ├── cloud/
│   └── local/
├── Pending_Approval/           # ❌ MISSING
│   ├── email/
│   ├── social/
│   └── payment/
├── .git/                       # ❌ MISSING (for sync)
└── deployment/                 # ❌ MISSING
    ├── docker-compose.yml
    ├── nginx.conf
    └── deploy.sh
```

---

## 📝 Implementation Details

### 1. Cloud Deployment (❌ MISSING)

**Platform Options:**
- Oracle Cloud Free Tier (recommended)
- AWS EC2 t2.micro (free tier)
- Google Cloud Compute Engine

**Setup Steps:**
```bash
# 1. Create VM
# - OS: Ubuntu 22.04
# - RAM: 2GB minimum
# - Storage: 20GB

# 2. Install dependencies
sudo apt update
sudo apt install python3.11 python3-pip git docker.io

# 3. Clone vault
git clone <your-repo> AI_Employee_Vault
cd AI_Employee_Vault

# 4. Install Python packages
pip3 install -r requirements.txt

# 5. Set up systemd service
sudo cp deployment/ai-employee.service /etc/systemd/system/
sudo systemctl enable ai-employee
sudo systemctl start ai-employee
```

**Systemd Service:** `deployment/ai-employee.service`
```ini
[Unit]
Description=AI Employee Cloud Agent
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/AI_Employee_Vault
ExecStart=/usr/bin/python3 cloud/cloud_orchestrator.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

### 2. Work-Zone Specialization (❌ MISSING)

**Cloud Agent Responsibilities:**
- Monitor Gmail inbox
- Draft email replies (save to /Pending_Approval/email/)
- Draft social media posts (save to /Pending_Approval/social/)
- Schedule posts
- Triage tasks by priority

**Local Agent Responsibilities:**
- Review and approve drafts
- Execute WhatsApp actions (session on local machine)
- Execute banking/payment actions (credentials on local machine)
- Final send/post actions
- Sensitive data handling

**File:** `cloud/cloud_orchestrator.py`
```python
# Cloud agent - runs 24/7
def cloud_agent_loop():
    while True:
        # 1. Check Gmail
        check_gmail_inbox()

        # 2. Draft replies
        draft_email_replies()

        # 3. Draft social posts
        draft_social_posts()

        # 4. Sync vault
        sync_vault_to_git()

        time.sleep(300)  # Every 5 minutes
```

**File:** `local/local_orchestrator.py`
```python
# Local agent - runs on-demand
def local_agent_loop():
    while True:
        # 1. Pull latest from cloud
        pull_vault_from_git()

        # 2. Check for approvals needed
        check_pending_approvals()

        # 3. Execute approved actions
        execute_approved_actions()

        # 4. Push results
        push_vault_to_git()

        time.sleep(60)  # Every minute when running
```

---

### 3. Vault Synchronization (❌ MISSING)

**Setup Git Sync:**
```bash
# Initialize git repo
cd AI_Employee_Vault
git init
git remote add origin <your-repo-url>

# Create .gitignore
cat > .gitignore <<EOF
.env
credentials.json
*.session
venv/
__pycache__/
*.pyc
EOF

# Initial commit
git add .
git commit -m "Initial vault setup"
git push -u origin main
```

**Sync Manager:** `cloud/sync_manager.py`
```python
def sync_vault():
    # Pull latest
    subprocess.run(['git', 'pull', 'origin', 'main'])

    # Add changes
    subprocess.run(['git', 'add', '.'])

    # Commit
    subprocess.run(['git', 'commit', '-m', f'Auto-sync {datetime.now()}'])

    # Push
    subprocess.run(['git', 'push', 'origin', 'main'])
```

**Sync Frequency:**
- Cloud: Every 5 minutes
- Local: Every 1 minute when running

---

### 4. Claim-by-Move Rule (❌ MISSING)

**Purpose:** Prevent both Cloud and Local from working on same task

**Implementation:**
```python
def claim_task(task_file, agent_name):
    """Move task to In_Progress to claim it"""
    source = Path('Needs_Action') / task_file
    dest = Path('In_Progress') / agent_name / task_file

    try:
        # Atomic move
        source.rename(dest)
        return True  # Successfully claimed
    except FileNotFoundError:
        return False  # Another agent claimed it first
```

**Workflow:**
1. Cloud sees task in /Needs_Action/email/
2. Cloud moves to /In_Progress/cloud/
3. Local sees task is claimed, skips it
4. Cloud completes, moves to /Pending_Approval/email/
5. Local approves, moves to /Done/

---

### 5. Health Monitoring (❌ MISSING)

**File:** `cloud/health_monitor.py`

**Purpose:** Monitor cloud agent health, auto-restart if needed

**Key Features:**
- Check process is running
- Monitor memory usage
- Check disk space
- Verify API connectivity
- Send alerts if issues

**Implementation:**
```python
def health_check():
    checks = {
        'process_running': check_process(),
        'memory_ok': check_memory(),
        'disk_ok': check_disk(),
        'api_ok': check_api_connectivity()
    }

    if not all(checks.values()):
        send_alert(checks)
        restart_agent()
```

**Monitoring Schedule:** Every 5 minutes

---

### 6. Cloud Odoo Deployment (❌ MISSING)

**Docker Compose:** `deployment/docker-compose.yml`
```yaml
version: '3'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: ${ODOO_DB_PASSWORD}
      POSTGRES_DB: postgres
    volumes:
      - odoo-db:/var/lib/postgresql/data

  odoo:
    image: odoo:19
    depends_on:
      - postgres
    ports:
      - "8069:8069"
    environment:
      HOST: postgres
      USER: odoo
      PASSWORD: ${ODOO_DB_PASSWORD}
    volumes:
      - odoo-data:/var/lib/odoo

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl

volumes:
  odoo-db:
  odoo-data:
```

**Setup HTTPS:**
```bash
# Install certbot
sudo apt install certbot

# Get SSL certificate
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem deployment/ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem deployment/ssl/
```

---

### 7. A2A Communication (❌ OPTIONAL)

**File:** `agent/a2a_protocol.py`

**Purpose:** Direct agent-to-agent messaging (alternative to file-based)

**Message Format:**
```json
{
  "from": "cloud_agent",
  "to": "local_agent",
  "type": "approval_request",
  "payload": {
    "action": "send_email",
    "draft": "email_draft_123.md"
  },
  "timestamp": "2026-02-12T10:30:00Z"
}
```

**Implementation:** WebSocket or HTTP API between agents

---

## 🧪 Testing Procedures

### Test 1: Cloud Deployment
```bash
# SSH to cloud VM
ssh ubuntu@your-cloud-ip

# Check service status
sudo systemctl status ai-employee

# Check logs
sudo journalctl -u ai-employee -f
```

### Test 2: Vault Sync
```bash
# On cloud: Create task
echo "Test task" > Needs_Action/test.md
git add . && git commit -m "Test" && git push

# On local: Pull
git pull

# Expected: test.md appears locally
```

### Test 3: Claim-by-Move
```bash
# Start both agents
# Create task in Needs_Action/
# Expected: Only one agent claims it (moves to In_Progress/)
```

### Test 4: End-to-End Platinum Demo
```bash
# 1. Turn off local agent
# 2. Send email to your Gmail
# 3. Cloud detects, drafts reply, saves to Pending_Approval/
# 4. Turn on local agent
# 5. Local pulls, shows approval request
# 6. Approve
# 7. Local sends email via MCP
# 8. Task moves to Done/
```

---

## ✅ Completion Criteria

Platinum Tier is COMPLETE when:

- [ ] Cloud VM deployed and running 24/7
- [ ] Work-zone specialization implemented
- [ ] Vault syncing via Git
- [ ] Claim-by-move rule working
- [ ] Health monitoring active
- [ ] Odoo deployed on cloud with HTTPS
- [ ] End-to-end demo passing
- [ ] Security rules enforced (no secrets in sync)
- [ ] All tests passing

---

## 🎓 What Platinum Tier Achieves

At Platinum tier, your AI employee can:
- ✅ Run 24/7 without your computer on
- ✅ Handle tasks while you're offline
- ✅ Coordinate between cloud and local
- ✅ Prevent conflicts with claim-by-move
- ✅ Monitor its own health
- ✅ Manage accounting in cloud Odoo
- ✅ Maintain security (secrets stay local)

---

## 📚 Cost Estimate

**Cloud Infrastructure:**
- Oracle Cloud Free Tier: $0/month (2 VMs free forever)
- Domain name: $12/year
- SSL certificate: Free (Let's Encrypt)

**Total:** ~$1/month

---

**Platinum Tier Specification Complete**
**Version:** 1.0
**Date:** 2026-02-12
