# Simple Testing Guide - Silver & Gold Levels

## Option 1: Automated Test (Easiest)

Run this single command to test everything:

```bash
bash test_complete.sh
```

This will automatically test both Silver and Gold levels and show you all the results.

---

## Option 2: Manual Testing (Step by Step)

### 🥈 TESTING SILVER LEVEL

#### Step 1: Create a Test Task
```bash
echo "Explain what machine learning is in simple terms" > Needs_Action/my_silver_test.md
```

#### Step 2: Generate Plan
```bash
source venv/bin/activate
python -m agent.bronze_planner
```

**Expected Output:**
```
🧠 Planning task: my_silver_test.md
✋ Approval requested for my_silver_test.md
```

#### Step 3: Check the Plan
```bash
cat Plans/my_silver_test.md
```

You should see a detailed plan for the task.

#### Step 4: Approve the Task

Open the file: `Approvals/my_silver_test.md.approval.md`

Change this line:
```
[ ] Approved  →  [x] Approved
```

Or use this command:
```bash
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/my_silver_test.md.approval.md
```

#### Step 5: Execute the Task
```bash
python -m agent.silver_executor
```

**Expected Output:**
```
🔍 Checking for approved tasks...
🚀 Executing task: my_silver_test.md
✅ Task executed successfully: my_silver_test.md
📦 Moved my_silver_test.md to Done folder
🎉 Executed 1 task(s)
```

#### Step 6: Check Results

**Check if task moved to Done:**
```bash
ls Done/ | grep my_silver_test
```

**Read the execution log:**
```bash
cat Logs/my_silver_test.md.execution.log
```

**✅ Silver Level Working if:**
- Task moved from Needs_Action/ to Done/
- Execution log created in Logs/
- Log contains the execution report

---

### 🥇 TESTING GOLD LEVEL

#### Step 1: Create a Test Task
```bash
echo "Write a creative tagline for a coffee shop" > Needs_Action/my_gold_test.md
```

#### Step 2: Generate Plan with Learning
```bash
python -m agent.gold_planner
```

**Expected Output:**
```
🧠 Planning task with learning: my_gold_test.md
✨ Generated improved plan using historical learning
✋ Approval requested for my_gold_test.md
```

#### Step 3: Check the Plan
```bash
cat Plans/my_gold_test.md
```

Notice: The plan should mention learning or reference past feedback if available.

#### Step 4: Approve the Task
```bash
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/my_gold_test.md.approval.md
```

#### Step 5: Execute with Gold Executor
```bash
python -m agent.gold_executor
```

**Expected Output:**
```
🔍 Checking for approved tasks...
🚀 Executing task: my_gold_test.md
✅ Task executed successfully: my_gold_test.md
📦 Moved my_gold_test.md to Done folder
📋 Feedback request created: my_gold_test.md
📋 Feedback requested for learning
🎉 Executed 1 task(s)
```

#### Step 6: Check Feedback Request
```bash
cat Feedback/my_gold_test.md.feedback.md
```

You should see a feedback form with rating options.

#### Step 7: Provide Feedback

Open `Feedback/my_gold_test.md.feedback.md` and fill it out:

Change:
```
[ ] 5 - Excellent  →  [x] 5 - Excellent
[ ] Yes (Plan Quality)  →  [x] Yes
[ ] Yes (Execution Quality)  →  [x] Yes
```

Add comments in the text sections.

Or use this quick command:
```bash
cat > Feedback/my_gold_test.md.feedback.md << 'EOF'
# Feedback Request

Task: my_gold_test.md
Date: 2026-02-11 13:30

## Quality Rating
Rate the execution quality (1-5):
[x] 5 - Excellent

## Plan Quality
Was the plan appropriate?
[x] Yes

## Execution Quality
Was the execution satisfactory?
[x] Yes

## What went well?
Great creative tagline! Very catchy.

## What could be improved?
Could provide 2-3 options to choose from.

## Additional Comments?
Excellent work!
EOF
```

#### Step 8: Process Feedback
```bash
python -m agent.feedback_processor
```

**Expected Output:**
```
📊 Processing feedback for learning...
✅ Feedback saved to learning database
✅ Processed feedback: my_gold_test.md (Rating: 5/5)
🎉 Processed 1 feedback(s)
📈 Updated Performance Metrics:
  Average Rating: 5.0/5
  Plan Quality: 100.0%
  Execution Quality: 100.0%
```

#### Step 9: Check Learning Metrics
```bash
python -m agent.learning_engine
```

**Expected Output:**
```
📊 Performance Metrics:
  Total Tasks: 2
  Average Rating: 5.0/5
  Plan Quality: 100.0%
  Execution Quality: 100.0%
```

#### Step 10: Verify Learning Database
```bash
cat Memory/feedback_history.json
```

You should see all feedback entries stored.

**✅ Gold Level Working if:**
- Feedback request created after execution
- Feedback processed and saved to database
- Performance metrics updated
- Learning database contains feedback entries

---

## Quick Verification Commands

### Check Silver Level Status:
```bash
echo "Silver Level Check:"
echo "Tasks in Done: $(ls Done/ | wc -l)"
echo "Execution logs: $(ls Logs/*.execution.log | wc -l)"
```

### Check Gold Level Status:
```bash
echo "Gold Level Check:"
echo "Feedback entries: $(ls Feedback/Processed/ 2>/dev/null | wc -l)"
python -m agent.learning_engine
```

### Check All Folders:
```bash
echo "=== Folder Status ==="
echo "Needs_Action: $(ls Needs_Action/*.md 2>/dev/null | wc -l) tasks"
echo "Plans: $(ls Plans/*.md 2>/dev/null | wc -l) plans"
echo "Approvals: $(ls Approvals/*.md 2>/dev/null | wc -l) approvals"
echo "Done: $(ls Done/*.md 2>/dev/null | wc -l) completed"
echo "Logs: $(ls Logs/*.log 2>/dev/null | wc -l) logs"
echo "Feedback: $(ls Feedback/*.md 2>/dev/null | wc -l) pending"
echo "Feedback Processed: $(ls Feedback/Processed/*.md 2>/dev/null | wc -l) processed"
```

---

## Troubleshooting

### Issue: "No module named agent"
**Solution:**
```bash
source venv/bin/activate
```

### Issue: Plans not being generated
**Solution:**
```bash
# Check if Gemini API key is set
cat .env | grep GEMINI_API_KEY
```

### Issue: Tasks not executing
**Solution:**
```bash
# Make sure task is approved
cat Approvals/your_task.md.approval.md | grep -i approved
```

### Issue: Feedback not processing
**Solution:**
```bash
# Make sure you marked a rating with [x]
cat Feedback/your_task.md.feedback.md | grep "\[x\]"
```

---

## What Success Looks Like

### Silver Level Success:
1. ✅ Task created in Needs_Action/
2. ✅ Plan generated in Plans/
3. ✅ Approval request in Approvals/
4. ✅ After approval, task executes
5. ✅ Task moves to Done/
6. ✅ Execution log in Logs/

### Gold Level Success:
1. ✅ All Silver level features work
2. ✅ Feedback request created after execution
3. ✅ Feedback can be filled out
4. ✅ Feedback processed and saved
5. ✅ Performance metrics updated
6. ✅ Learning database grows over time
7. ✅ Future plans reference past learning

---

## Next Steps After Testing

Once both levels work:
1. Try the autonomous mode: `python main.py`
2. Test with your own real tasks
3. Provide feedback on multiple tasks to see learning improve
4. Ready for Platinum level (multi-agent collaboration)
