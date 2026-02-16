# Check Approvals Skill

**Purpose:** Check which tasks have been approved by human and are ready for execution

**Category:** Silver Tier - Approval Management
**Version:** 1.0
**Last Updated:** 2026-02-16

---

## Usage

```bash
/check-approvals
```

**No parameters required** - scans all approval files automatically.

---

## What This Skill Does

This skill scans the Approvals folder and identifies which tasks are ready for execution.

### Step-by-Step Process:
1. **Scan Approvals** - Lists all .approval.md files
2. **Read Each File** - Checks approval status
3. **Identify Approved** - Finds tasks marked [x] Approved
4. **Verify Task Exists** - Confirms task still in Needs_Action
5. **Return List** - Provides list of ready-to-execute tasks

---

## Inputs

### Context Files Read:
- `Approvals/*.approval.md` - All approval request files
- `Needs_Action/*.md` - Verifies tasks still exist

---

## Outputs

### Console Output:
```
Approved tasks ready for execution:
- EMAIL_Test_19c66ef2.md
- EMAIL_Invoice_Request_19c66f01.md

Pending approval:
- EMAIL_Client_Query_19c67001.md

Rejected:
- EMAIL_Spam_19c66ff0.md
```

### Return Value:
```python
{
    "approved": [
        "EMAIL_Test_19c66ef2.md",
        "EMAIL_Invoice_Request_19c66f01.md"
    ],
    "pending": [
        "EMAIL_Client_Query_19c67001.md"
    ],
    "rejected": [
        "EMAIL_Spam_19c66ff0.md"
    ]
}
```

---

## Approval Status Detection

### Approved:
```markdown
Decision:
[x] Approved
[ ] Rejected
```
OR
```markdown
Decision:
[X] Approved  # Capital X also valid
[ ] Rejected
```

### Rejected:
```markdown
Decision:
[ ] Approved
[x] Rejected
```

### Pending:
```markdown
Decision:
[ ] Approved
[ ] Rejected
```

---

## Use Cases

### 1. Before Execution Cycle
```bash
# Check what's ready to execute
/check-approvals

# Execute each approved task
for task in approved_tasks:
    /execute-task $task
```

### 2. Dashboard Updates
```bash
# Get approval counts for dashboard
/check-approvals
# Update Dashboard.md with counts
```

### 3. Human Review
```bash
# Show human what's pending
/check-approvals
# Display pending list in notification
```

---

## Error Handling

### Common Issues:
- **Approval file exists but task deleted** → Mark as orphaned
- **Task exists but no approval file** → Mark as needs planning
- **Malformed approval file** → Flag for human review
- **Permission denied** → Log error, alert human

---

## Example Output

### Scenario: 3 tasks in various states

**Approvals folder:**
- `EMAIL_Test_19c66ef2.md.approval.md` - [x] Approved
- `EMAIL_Invoice_19c66f01.md.approval.md` - [ ] Approved (pending)
- `EMAIL_Spam_19c66ff0.md.approval.md` - [x] Rejected

**Output:**
```
╔════════════════════════════════════════════════════════════╗
║                  APPROVAL STATUS REPORT                    ║
╚════════════════════════════════════════════════════════════╝

✅ APPROVED (Ready to Execute): 1
   → EMAIL_Test_19c66ef2.md

⏳ PENDING (Awaiting Human): 1
   → EMAIL_Invoice_19c66f01.md

❌ REJECTED (Will Not Execute): 1
   → EMAIL_Spam_19c66ff0.md

NEXT ACTION: Execute 1 approved task(s)
```

---

## Performance Metrics

- **Scan time:** < 1 second for 100 files
- **Accuracy:** 100% (simple file parsing)
- **Checks performed:** Track in logs

---

## Integration Points

### Used By:
- `execute_task` - Checks approval before execution
- `update_dashboard` - Gets counts for metrics
- Orchestrator - Determines what to execute next

### Uses:
- File system - Reads approval files
- Pattern matching - Detects [x] markers

---

## File Format Requirements

### Valid Approval File:
```markdown
# Approval Request

Task: EMAIL_Test_19c66ef2.md

Decision:
[ ] Approved
[ ] Rejected

Notes:
(optional human notes)
```

### Invalid Formats:
```markdown
# Missing checkbox format
Approved: Yes  # ❌ Won't detect

# Wrong checkbox syntax
[✓] Approved  # ❌ Must be [x] or [X]

# Missing Decision section
# ❌ Must have "Decision:" header
```

---

## Related Skills

- `plan_task` - Creates approval files that this skill checks
- `execute_task` - Uses this skill to verify approval
- `update_dashboard` - Uses counts from this skill

---

## Maintenance Notes

### When to Update This Skill:
- Approval file format changes
- New approval states are added (e.g., "Deferred")
- Performance optimization needed
- Error patterns emerge

### Version History:
- v1.0 (2026-02-16) - Initial creation for hackathon

---

**This skill is part of the Silver Tier human-in-the-loop approval system.**
