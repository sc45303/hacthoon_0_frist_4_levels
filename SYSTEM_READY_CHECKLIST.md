# ✅ System Ready Checklist - When to Test

## 🚦 Current Blockers (Temporary)

### 1. Network Connectivity
**Status:** ⚠️ DNS resolution failing
**Check:** `ping oauth2.googleapis.com`
**Fix:** 
- Check internet connection
- Restart WSL: `wsl --shutdown` then reopen
- Check firewall settings

### 2. Gemini API Quota
**Status:** ❌ Exhausted (20/20 requests used)
**Resets:** ~24 hours from now
**Check:** Try running: `python -m agent.bronze_planner`

---

## ✅ When Both Are Fixed, Follow This:

### Step 1: Verify System Health (2 minutes)
```bash
# Check cron jobs
crontab -l

# Check no duplicate processes
ps aux | grep -E "(gmail_watcher|bronze_planner|silver_executor)" | grep -v grep

# Should see only 1 gmail_watcher process
```

### Step 2: Send Test Email (1 minute)
```bash
# Send yourself an email with subject: "Test AI Employee Flow"
# Mark it as important in Gmail
```

### Step 3: Watch the Magic Happen (10 minutes)
```bash
# Terminal 1: Watch Gmail Watcher
tail -f Memory/cron_logs/gmail_watcher.log

# Terminal 2: Watch Bronze Planner
tail -f Memory/cron_logs/bronze_planner.log

# Terminal 3: Watch folders
watch -n 5 'ls -lh Needs_Action/ Plans/ Approvals/ Done/'
```

### Step 4: Timeline (What You'll See)
```
Minute 0: Send test email
Minute 2: Gmail Watcher detects it
          → Creates Needs_Action/EMAIL_Test_AI_Employee_Flow_xxx.md
          
Minute 5: Bronze Planner runs
          → Creates Plans/EMAIL_Test_AI_Employee_Flow_xxx.md
          → Creates Approvals/EMAIL_Test_AI_Employee_Flow_xxx.md.approval.md
          
Minute 6: YOU APPROVE (manual step)
          → Edit Approvals/EMAIL_Test_AI_Employee_Flow_xxx.md.approval.md
          → Change [ ] Approved to [x] Approved
          → Save file
          
Minute 10: Silver Executor runs
           → Reads approved task
           → Executes according to plan
           → Creates Logs/EMAIL_Test_AI_Employee_Flow_xxx.md.execution.log
           → Moves task to Done/EMAIL_Test_AI_Employee_Flow_xxx.md
           
Minute 10: ✅ COMPLETE!
```

### Step 5: Verify Success
```bash
# Check Done folder
ls -lh Done/

# Read execution log
cat Logs/EMAIL_Test_AI_Employee_Flow_*.md.execution.log

# Verify task moved
ls Needs_Action/EMAIL_Test* # Should be empty
ls Done/EMAIL_Test* # Should exist
```

---

## 🎯 Success Criteria

Your autonomous system is working if:
- [x] Email detected within 2 minutes
- [x] Plan created within 5 minutes
- [x] Approval request created
- [x] After approval, task executes within 5 minutes
- [x] Task moved to Done/
- [x] Execution log created
- [x] No errors in logs

---

## 🐛 Troubleshooting

### If Gmail Watcher doesn't detect email:
```bash
# Check if running
ps aux | grep gmail_watcher

# Check logs
tail -50 Memory/cron_logs/gmail_watcher.log

# Restart manually
./cron_gmail_watcher.sh
```

### If Bronze Planner doesn't create plan:
```bash
# Check Gemini API quota
python -m agent.bronze_planner

# If quota error, wait 24 hours
# If other error, check logs
```

### If Silver Executor doesn't execute:
```bash
# Verify approval file has [x] Approved
cat Approvals/EMAIL_Test*.approval.md

# Check logs
tail -50 Memory/cron_logs/silver_executor.log

# Run manually to see error
source venv/bin/activate
python -m agent.silver_executor
```

---

## 📊 Expected Logs

### Gmail Watcher Log (Success):
```
[2026-02-17 10:00:00] Gmail Watcher started
[2026-02-17 10:00:05] Found 1 new email(s)
[2026-02-17 10:00:05] Created task: EMAIL_Test_AI_Employee_Flow_xxx.md
```

### Bronze Planner Log (Success):
```
[2026-02-17 10:05:00] Bronze Planner started
🧠 Planning task: EMAIL_Test_AI_Employee_Flow_xxx.md
✋ Approval requested for EMAIL_Test_AI_Employee_Flow_xxx.md
[2026-02-17 10:05:10] Bronze Planner completed
```

### Silver Executor Log (Success):
```
[2026-02-17 10:10:00] Silver Executor started
🚀 Executing task: EMAIL_Test_AI_Employee_Flow_xxx.md
✅ Task executed successfully
📦 Moved to Done folder
[2026-02-17 10:10:15] Silver Executor completed
```

---

## 🎉 When It Works

You'll have proven:
1. ✅ Fully autonomous email detection
2. ✅ AI-powered planning
3. ✅ Human-in-the-loop approval
4. ✅ Autonomous execution
5. ✅ Complete audit trail

**This is Silver tier functionality working in production!**

---

## 📝 Next Steps After Success

1. **Document for hackathon** - Create submission materials
2. **Test edge cases** - Try different email types
3. **Add more features** - Gold tier integrations
4. **Optimize** - Reduce API calls, improve error handling

---

**Save this file and follow it when blockers are resolved!**
