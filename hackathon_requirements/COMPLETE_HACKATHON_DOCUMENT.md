# Personal AI Employee Hackathon 0: Building Autonomous FTEs

**Tagline:** Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

**Date Saved:** 2026-02-16

---

## Core Concept

Build a "Digital FTE" (Full-Time Equivalent) - an AI agent powered by Claude Code and Obsidian that proactively manages personal and business affairs 24/7.

## Tech Stack Requirements

### Required Components
1. **Claude Code** - Primary reasoning engine (NOT Gemini API)
2. **Obsidian** - Knowledge base & dashboard (NOT plain markdown)
3. **Agent Skills** - Reusable intelligence modules (NOT Python scripts)
4. **MCP Servers** - External action handlers
5. **Python Watchers** - Monitoring scripts

### Architecture
- **Brain:** Claude Code (reasoning engine)
- **Memory/GUI:** Obsidian (local Markdown dashboard)
- **Senses:** Python Watcher scripts (Gmail, WhatsApp, filesystem)
- **Hands:** MCP servers (email sending, browser automation)

---

## Tier Requirements

### Bronze Tier (8-12 hours)
- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ One working Watcher script (Gmail OR filesystem)
- ✅ Claude Code reading/writing to vault
- ✅ Basic folder structure: /Inbox, /Needs_Action, /Done
- ⚠️ **All AI functionality as Agent Skills**

### Silver Tier (20-30 hours)
All Bronze requirements PLUS:
- ✅ Two or more Watcher scripts (Gmail + WhatsApp + LinkedIn)
- ✅ Automatically post on LinkedIn
- ✅ Claude reasoning loop creating Plan.md files
- ✅ One working MCP server (email sending)
- ✅ Human-in-the-loop approval workflow
- ✅ Basic scheduling via cron
- ⚠️ **All AI functionality as Agent Skills**

### Gold Tier (40+ hours)
All Silver requirements PLUS:
- Full cross-domain integration (Personal + Business)
- Odoo Community accounting system integration
- Facebook and Instagram integration
- Twitter (X) integration
- Multiple MCP servers
- Weekly Business Audit with CEO Briefing
- Error recovery and graceful degradation
- Comprehensive audit logging
- Ralph Wiggum loop for autonomous multi-step tasks
- ⚠️ **All AI functionality as Agent Skills**

### Platinum Tier (60+ hours)
All Gold requirements PLUS:
- Run AI Employee on Cloud 24/7
- Work-Zone Specialization (Cloud vs Local)
- Delegation via Synced Vault
- Odoo Community on Cloud VM
- Agent-to-Agent communication

---

## Critical Requirements

### Agent Skills (MANDATORY)
**From hackathon document:**
> "All AI functionality should be implemented as Agent Skills"

This appears in:
- Bronze Tier requirements
- Silver Tier requirements
- Gold Tier requirements

**What are Agent Skills?**
- Reusable, modular capabilities that Claude Code can invoke
- Defined in SKILL.md files
- Allow Claude to perform specific tasks autonomously
- NOT the same as Python scripts calling APIs directly

**Reference:**
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://www.youtube.com/watch?v=nbqqnl3JdR0

### Claude Code (MANDATORY)
Must use Claude Code as the primary reasoning engine, NOT Gemini API or other LLMs.

### Obsidian (MANDATORY)
Must use Obsidian as the knowledge base, NOT plain markdown files in a regular folder.

---

## Key Features

### Human-in-the-Loop (HITL)
For sensitive actions, AI creates approval request files:
- `/Pending_Approval/` - Awaiting human review
- `/Approved/` - Human approved, ready to execute
- `/Rejected/` - Human rejected, do not execute

### Ralph Wiggum Loop
Stop hook pattern that keeps Claude working until task is complete:
1. Orchestrator creates state file with prompt
2. Claude works on task
3. Claude tries to exit
4. Stop hook checks: Is task in /Done?
5. If NO → Block exit, re-inject prompt, loop continues
6. If YES → Allow exit (complete)

### Business Handover
Autonomous Business Audit feature:
- Runs every Sunday night (scheduled)
- Reads Business_Goals.md, Tasks/Done, Bank_Transactions.md
- Generates "Monday Morning CEO Briefing"
- Highlights: Revenue, Bottlenecks, Proactive Suggestions

---

## Security Requirements

### Credential Management
- Never store credentials in plain text
- Use environment variables for API keys
- Use secrets manager for banking credentials
- Create .env file (add to .gitignore)
- Rotate credentials monthly

### Sandboxing
- Development Mode flag prevents real actions
- Dry Run flag logs without executing
- Separate test/sandbox accounts
- Rate limiting (max actions per hour)

### Audit Logging
Every action must be logged:
```json
{
  "timestamp": "2026-01-07T10:30:00Z",
  "action_type": "email_send",
  "actor": "claude_code",
  "target": "client@example.com",
  "parameters": {"subject": "Invoice #123"},
  "approval_status": "approved",
  "approved_by": "human",
  "result": "success"
}
```

### Permission Boundaries
| Action Category | Auto-Approve | Always Require Approval |
|----------------|--------------|------------------------|
| Email replies | Known contacts | New contacts, bulk sends |
| Payments | < $50 recurring | All new payees, > $100 |
| Social media | Scheduled posts | Replies, DMs |
| File operations | Create, read | Delete, move outside vault |

---

## Judging Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Functionality | 30% | Does it work? Core features complete? |
| Innovation | 25% | Creative solutions, novel integrations |
| Practicality | 20% | Would you use this daily? |
| Security | 15% | Proper credential handling, HITL safeguards |
| Documentation | 10% | Clear README, setup, demo |

---

## Submission Requirements

1. GitHub repository (public or private with judge access)
2. README.md with setup instructions and architecture
3. Demo video (5-10 minutes) showing key features
4. Security disclosure: How credentials are handled
5. Tier declaration: Bronze, Silver, or Gold
6. **Submit Form:** https://forms.gle/JR9T1SJq5rmQyGkGA

---

## Learning Resources

### Prerequisites
- Claude Code Fundamentals: https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows
- Agent Skills: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- MCP Introduction: https://modelcontextprotocol.io/introduction
- Obsidian Fundamentals: https://help.obsidian.md/Getting+started

### Core Learning
- Claude + Obsidian Integration: https://www.youtube.com/watch?v=sCIS05Qt79Y
- Claude Agent Skills: https://www.youtube.com/watch?v=nbqqnl3JdR0
- Claude Agent Teams: https://www.youtube.com/watch?v=0J2_YGuNrDo
- Building MCP Servers: https://modelcontextprotocol.io/quickstart

---

## Weekly Research Meetings

**Every Wednesday at 10:00 PM PKT**
- Zoom: https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1
- Meeting ID: 871 8870 7642
- Passcode: 744832
- YouTube: https://www.youtube.com/@panaversity

---

**This document contains the complete hackathon requirements. All AI functionality MUST be implemented as Agent Skills to be compliant.**
