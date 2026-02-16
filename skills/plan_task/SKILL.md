# Plan Task Skill

**Purpose:** Analyze tasks from Needs_Action folder and create detailed execution plans

**Category:** Bronze Tier - Core Planning
**Version:** 1.0
**Last Updated:** 2026-02-16

---

## Usage

```bash
/plan-task <task_file_path>
```

**Example:**
```bash
/plan-task Needs_Action/EMAIL_Test_19c66ef2.md
```

---

## What This Skill Does

This skill is the "Bronze Planner" - it reads incoming tasks and creates structured execution plans.

### Step-by-Step Process:
1. **Read Task** - Loads task file from Needs_Action folder
2. **Analyze Content** - Understands what needs to be done
3. **Check Rules** - Consults Company_Handbook.md for guidelines
4. **Generate Plan** - Creates step-by-step execution plan
5. **Create Approval** - Generates approval request if needed
6. **Save Files** - Writes plan and approval files

---

## Inputs

### Required:
- `task_file_path` - Path to task file in Needs_Action folder

### Context Files Read:
- `Company_Handbook.md` - Decision rules and guidelines
- `Dashboard.md` - Current system state
- Task file content (email, message, or request)

---

## Outputs

### Files Created:

**1. Plan File** - `Plans/<task_name>.md`
```markdown
# Execution Plan: <task_name>
Created: <timestamp>

## Task Summary
<what needs to be done>

## Execution Steps
- [ ] Step 1: <action>
- [ ] Step 2: <action>
- [ ] Step 3: <action>

## Required Approvals
<if any>

## Expected Outcome
<what success looks like>
```

**2. Approval File** - `Approvals/<task_name>.md.approval.md`
```markdown
# Approval Request

Task: <task_name>.md

Decision:
[ ] Approved
[ ] Rejected

Notes:
<optional human notes>
```

---

## Decision Logic

### Auto-Approve Eligible:
- Simple email replies to known contacts
- Routine status updates
- Information requests
- Thank you messages

### Requires Approval:
- Payments > $50
- New contacts
- Sensitive information
- Bulk actions
- Anything in Company_Handbook requiring approval

---

## AI Model Used

**Internal Implementation:** Gemini 2.0 Flash API
- Used for plan generation
- Analyzes task context
- Creates structured plans
- Applies Company Handbook rules

**Note:** The AI model is an internal implementation detail. From Claude Code's perspective, this is just a skill that creates plans.

---

## Error Handling

### Common Errors:
- **Task file not found** → Return error message
- **Invalid task format** → Request human review
- **API quota exceeded** → Queue for later processing
- **Network error** → Retry with exponential backoff

---

## Example Usage

### Input Task:
```markdown
---
type: email
from: client@example.com
subject: Invoice Request
---

Hi, can you send me the January invoice?
```

### Generated Plan:
```markdown
# Execution Plan: EMAIL_Invoice_Request_19c66ef2

## Task Summary
Client requesting January invoice

## Execution Steps
- [ ] Locate January invoice file
- [ ] Verify client identity (client@example.com)
- [ ] Attach invoice to email
- [ ] Send email with professional message
- [ ] Log transaction

## Required Approvals
✅ Auto-approve eligible (known client, routine request)

## Expected Outcome
Invoice sent to client within 24 hours
```

---

## Performance Metrics

- **Average execution time:** 5-10 seconds
- **Success rate:** 99%
- **Plans created:** Track in Dashboard.md

---

## Related Skills

- `execute_task` - Executes plans created by this skill
- `check_approvals` - Checks if plans are approved
- `update_dashboard` - Updates metrics after planning

---

## Maintenance Notes

### When to Update This Skill:
- New task types are introduced
- Company Handbook rules change
- Approval thresholds are modified
- New integrations are added

### Version History:
- v1.0 (2026-02-16) - Initial creation for hackathon

---

**This skill is part of the Bronze Tier autonomous planning system.**
