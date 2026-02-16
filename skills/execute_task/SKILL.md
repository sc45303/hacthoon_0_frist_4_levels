# Execute Task Skill

**Purpose:** Execute approved tasks according to their execution plans

**Category:** Silver Tier - Core Execution
**Version:** 1.0
**Last Updated:** 2026-02-16

---

## Usage

```bash
/execute-task <task_file_path>
```

**Example:**
```bash
/execute-task Needs_Action/EMAIL_Test_19c66ef2.md
```

---

## What This Skill Does

This skill is the "Silver Executor" - it executes approved tasks following their plans.

### Step-by-Step Process:
1. **Check Approval** - Verifies task is approved by human
2. **Read Plan** - Loads execution plan from Plans folder
3. **Read Task** - Loads original task details
4. **Execute Steps** - Performs each action in the plan
5. **Log Results** - Creates detailed execution log
6. **Move to Done** - Archives completed task

---

## Inputs

### Required:
- `task_file_path` - Path to task file in Needs_Action folder

### Context Files Read:
- `Approvals/<task_name>.md.approval.md` - Approval status
- `Plans/<task_name>.md` - Execution plan
- `Company_Handbook.md` - Safety rules
- Task file content

---

## Outputs

### Files Created:

**1. Execution Log** - `Logs/<task_name>.md.execution.log`
```markdown
# Execution Log: <task_name>
Timestamp: <timestamp>

## Task
<original task content>

## Plan
<execution plan>

## Execution Report
### Step 1: <action>
- Action Taken: <details>
- Result: <outcome>
- Status: Completed

### Step 2: <action>
- Action Taken: <details>
- Result: <outcome>
- Status: Completed

## Final Status
Status: Completed
Execution Time: <duration>
```

### Files Moved:
- `Needs_Action/<task_name>.md` → `Done/<task_name>.md`

---

## Safety Checks

### Pre-Execution Validation:
✅ **MUST verify approval exists**
✅ **MUST check [x] Approved is marked**
✅ **MUST NOT execute if [x] Rejected**
✅ **MUST verify plan exists**
✅ **MUST check Company Handbook rules**

### During Execution:
- Log every action taken
- Stop on errors
- Never override safety rules
- Request human help if uncertain

---

## Approval Status Checks

### Approved:
```markdown
Decision:
[x] Approved
[ ] Rejected
```
→ **Execute task**

### Rejected:
```markdown
Decision:
[ ] Approved
[x] Rejected
```
→ **Do NOT execute, move to Done with rejection note**

### Pending:
```markdown
Decision:
[ ] Approved
[ ] Rejected
```
→ **Wait, do NOT execute**

---

## AI Model Used

**Internal Implementation:** Gemini 2.0 Flash API
- Used for task execution
- Follows plan steps
- Generates execution reports
- Handles complex reasoning

**Note:** The AI model is an internal implementation detail. From Claude Code's perspective, this is just a skill that executes tasks.

---

## Error Handling

### Common Errors:
- **No approval found** → Skip execution, log warning
- **Approval pending** → Wait for human decision
- **Task rejected** → Archive with rejection note
- **Execution fails** → Log error, alert human
- **API quota exceeded** → Queue for later

### Recovery Actions:
- Partial completion → Save progress, request human review
- Network error → Retry with exponential backoff
- Invalid data → Flag for human intervention

---

## Example Execution

### Input Task:
```markdown
---
type: email
from: client@example.com
subject: Invoice Request
---

Hi, can you send me the January invoice?
```

### Execution Plan:
```markdown
- [ ] Locate January invoice
- [ ] Verify client identity
- [ ] Send email with invoice
- [ ] Log transaction
```

### Execution Log:
```markdown
# Execution Log: EMAIL_Invoice_Request_19c66ef2

## Step 1: Locate January invoice
- Action: Searched /Invoices folder
- Result: Found invoice_jan_2026.pdf
- Status: Completed

## Step 2: Verify client identity
- Action: Checked client@example.com in contacts
- Result: Known client, verified
- Status: Completed

## Step 3: Send email with invoice
- Action: Used Email MCP to send
- Result: Email sent successfully
- Status: Completed

## Step 4: Log transaction
- Action: Updated accounting log
- Result: Transaction logged
- Status: Completed

## Final Status: Completed ✅
```

---

## Integration with MCP Servers

This skill can invoke MCP servers for external actions:

### Email MCP:
```python
email_mcp.send_email(
    to="client@example.com",
    subject="January Invoice",
    body="Please find attached...",
    attachment="invoice_jan_2026.pdf"
)
```

### Browser MCP:
```python
browser_mcp.navigate("https://payment-portal.com")
browser_mcp.fill_form({"amount": "500", "recipient": "Client A"})
# Stop here, require approval for submit
```

---

## Performance Metrics

- **Average execution time:** 10-30 seconds
- **Success rate:** 95%
- **Tasks executed:** Track in Dashboard.md
- **Error rate:** Track for improvement

---

## Related Skills

- `plan_task` - Creates plans that this skill executes
- `check_approvals` - Verifies approval before execution
- `update_dashboard` - Updates metrics after execution

---

## Prohibited Actions

**NEVER do these without explicit approval:**
- Delete files
- Send money to new recipients
- Share confidential information
- Modify system configurations
- Override security rules

---

## Maintenance Notes

### When to Update This Skill:
- New action types are added
- MCP servers are updated
- Safety rules change
- Error patterns emerge

### Version History:
- v1.0 (2026-02-16) - Initial creation for hackathon

---

**This skill is part of the Silver Tier autonomous execution system.**
