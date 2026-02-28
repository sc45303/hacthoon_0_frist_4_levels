# ⚡ Quick Approval Guide

## How to Approve Tasks (The Only Manual Step)

### Method 1: Command Line (Fastest)

```bash
# Approve all pending tasks
for file in Approvals/*.approval.md; do
  sed -i 's/\[ \] Approved/[x] Approved/' "$file"
  echo "✓ Approved: $(basename $file)"
done
```

### Method 2: Edit Single File

```bash
# Find pending approvals
ls Approvals/*.approval.md

# Edit specific file
nano Approvals/EMAIL_xyz.md.approval.md

# Change this line:
[ ] Approved

# To this:
[x] Approved

# Save and exit (Ctrl+X, Y, Enter)
```

### Method 3: Approve One Task

```bash
# Approve specific task
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/EMAIL_Test_AI_Employee_Flow_*.approval.md
```

### Method 4: Reject a Task

```bash
# Edit file and change to:
[ ] Approved
[x] Rejected

# Task will not be executed
```

---

## 📋 Approval File Format

```markdown
# Approval Request

Task: EMAIL_Test_AI_Employee_Flow_xxx.md

Decision:
[ ] Approved ← Change this to [x]
[ ] Rejected

Notes:
(Optional: Add your notes here)
```

---

## ⏱️ When to Approve

**Check for new approvals every 5-10 minutes:**

```bash
# Quick check
ls Approvals/*.approval.md | wc -l

# If number > 0, you have pending approvals
```

**Or watch continuously:**

```bash
watch -n 30 'ls -lh Approvals/'
```

---

## 🎯 Approval Best Practices

1. **Review the plan first**

   ```bash
   # Read the plan before approving
   cat Plans/EMAIL_xyz.md
   ```

2. **Check task content**

   ```bash
   # Read original task
   cat Needs_Action/EMAIL_xyz.md
   ```

3. **Approve quickly for testing**
   - During testing, approve all tasks
   - In production, review carefully

4. **Reject suspicious tasks**
   - Unknown senders
   - Unusual requests
   - Sensitive actions

---

## 🔄 Approval Workflow

```
1. Bronze Planner creates approval request
   → Approvals/EMAIL_xyz.md.approval.md

2. You review and approve
   → Change [ ] to [x]

3. Silver Executor detects approval (within 5 min)
   → Executes task
   → Moves to Done/
```

---

**This is the ONLY manual step in your autonomous system!**
