# How to Test Silver Level AI Employee

## Quick Test (5 minutes)

### Step 1: Create a Task
Create a file in `Needs_Action/` folder:
```bash
echo "Summarize the benefits of cloud computing in 3 bullet points" > Needs_Action/my_test.md
```

### Step 2: Generate Plan
```bash
source venv/bin/activate
python -m agent.bronze_planner
```

You'll see:
- ✅ Plan created in `Plans/my_test.md`
- ✅ Approval request in `Approvals/my_test.md.approval.md`

### Step 3: Approve the Task
Edit `Approvals/my_test.md.approval.md` and change:
```
[ ] Approved  →  [x] Approved
```

### Step 4: Execute
```bash
python -m agent.silver_executor
```

You'll see:
- ✅ Task executed
- ✅ Moved to `Done/my_test.md`
- ✅ Log created in `Logs/my_test.md.execution.log`

### Step 5: Check Results
```bash
cat Logs/my_test.md.execution.log
```

---

## Full Autonomous Mode

Run the orchestrator to watch folders automatically:
```bash
python main.py
```

This will:
- Watch for new tasks in Needs_Action/
- Auto-generate plans
- Auto-execute when you approve
- Run continuously until you press Ctrl+C

---

## What Silver Level Does

✅ **Autonomous Planning** - AI reads tasks and creates execution plans
✅ **Human Approval** - Safety check before execution
✅ **Autonomous Execution** - AI executes approved plans
✅ **Detailed Logging** - Every execution is documented
✅ **Task Management** - Automatic file organization
✅ **Memory System** - Tracks all task history

---

## Folder Structure

```
Needs_Action/  → Put new tasks here
Plans/         → AI generates plans here
Approvals/     → Approve tasks here
Done/          → Completed tasks
Logs/          → Execution logs
Memory/        → Task history JSON
```

---

## Silver Level = COMPLETE ✅

Your AI Employee can now:
- Detect tasks
- Plan execution
- Request approval
- Execute autonomously
- Track everything
