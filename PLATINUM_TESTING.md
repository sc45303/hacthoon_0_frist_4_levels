# 🎯 Quick Testing Guide - Platinum Level

## Test Platinum Level in 5 Minutes

### Test 1: Simple Task (Single Agent)

```bash
# Step 1: Create a simple task
echo "Write a short poem about coding" > Needs_Action/platinum_simple.md

# Step 2: Generate plan
python -m agent.gold_planner

# Step 3: Approve
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/platinum_simple.md.approval.md

# Step 4: Execute with Platinum
python -m agent.platinum_executor

# Step 5: Check results
cat Logs/platinum_simple.md.execution.log
```

**Expected:** Single Writer agent executes the task.

---

### Test 2: Complex Task (Multiple Agents)

```bash
# Step 1: Create a complex task
echo "Research the benefits of exercise and write a short article about it" > Needs_Action/platinum_complex.md

# Step 2: Generate plan
python -m agent.gold_planner

# Step 3: Approve
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/platinum_complex.md.approval.md

# Step 4: Execute with Platinum (multi-agent collaboration!)
python -m agent.platinum_executor

# Step 5: Check collaboration log
cat Collaboration_Logs/platinum_complex.md.collaboration.json

# Step 6: Check execution log
cat Logs/platinum_complex.md.execution.log
```

**Expected:**
- Researcher agent gathers information about exercise
- Writer agent creates article using research
- Results combined in final output

---

### Test 3: Very Complex Task (All Agents)

```bash
# Create a task requiring all agent types
echo "Research Python web frameworks, analyze their pros and cons, write a comparison article, and provide sample code" > Needs_Action/platinum_full.md

python -m agent.gold_planner
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/platinum_full.md.approval.md
python -m agent.platinum_executor

# Check which agents were used
cat Collaboration_Logs/platinum_full.md.collaboration.json | grep agent_type
```

**Expected:**
- Researcher: Gathers framework information
- Analyst: Compares pros/cons
- Writer: Creates comparison article
- Coder: Generates sample code

---

## Verify Multi-Agent Collaboration

```bash
# Check collaboration log structure
cat Collaboration_Logs/platinum_complex.md.collaboration.json
```

You should see:
```json
{
  "original_task": "...",
  "collaboration": true,
  "agents_involved": 2,
  "subtasks_completed": 2,
  "agent_outputs": [
    {
      "subtask": "Research...",
      "agent": "Researcher",
      "status": "completed",
      "output": "..."
    },
    {
      "subtask": "Write...",
      "agent": "Writer",
      "status": "completed",
      "output": "..."
    }
  ]
}
```

---

## Run Autonomous Mode

```bash
# Start the full Platinum system
python main.py
```

This will:
- Watch for new tasks
- Auto-generate plans with learning
- Wait for approval
- Execute with multi-agent collaboration
- Request feedback
- Learn and improve

Press Ctrl+C to stop.

---

## Success Indicators

✅ **Platinum Working If:**
1. Multiple agents registered on startup
2. Complex tasks decomposed into subtasks
3. Different agent types execute different subtasks
4. Collaboration logs created in JSON format
5. Execution logs show multiple agent outputs
6. Results aggregated into final output

---

## Folder Structure Check

```bash
ls -la Collaboration_Logs/
ls -la Logs/
ls -la Done/
```

You should see:
- `.collaboration.json` files in Collaboration_Logs/
- `.execution.log` files in Logs/
- Completed tasks in Done/

---

## Quick Verification

```bash
# Count Python modules
find agent/ -name "*.py" | wc -l
# Should show: 21

# Check specialized agents
ls agent/specialized_agents/
# Should show: __init__.py, agents.py

# Verify all levels available
grep "CURRENT_LEVEL" main.py
# Should show: platinum
```

---

## What Makes Platinum Different?

**Silver Level:**
- Single execution path
- One AI does everything

**Gold Level:**
- Single execution with learning
- Improves over time

**Platinum Level:**
- Multiple specialized agents
- Task decomposition
- Parallel execution
- Agent collaboration
- Each agent has expertise

---

## Example Output

When you run a complex task, you'll see:

```
💎 PLATINUM LEVEL - Multi-Agent Collaboration
====================================
📋 Task: Research AI trends and write an article

🔨 Decomposing task...
✅ Task decomposed into 2 subtask(s)

🤝 Collaboration required - 2 agents needed

🎯 Executing subtask 1: Research AI trends
🔍 researcher_001: Starting research task...
✅ researcher_001: Research completed

🎯 Executing subtask 2: Write article using research
✍️  writer_001: Starting writing task...
✅ writer_001: Writing completed

📦 Aggregating results from all agents...
====================================
🤖 Researcher Agent - Research AI trends
[Research findings...]

🤖 Writer Agent - Write article
[Article content...]
```

---

**You're ready to test Platinum level!** 🚀
