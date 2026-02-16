# Updated Crontab for Claude Code Architecture

# Replace old Gemini-based cron jobs with new Claude Code orchestrator

## Old Jobs (Remove):
```
*/5 * * * * /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault/cron_bronze_planner.sh
*/5 * * * * /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault/cron_silver_executor.sh
```

## New Jobs (Add):
```
*/5 * * * * /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault/cron_claude_planner.sh
*/5 * * * * /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault/cron_claude_executor.sh
```

## Complete Updated Crontab:
```
# Personal AI Employee - Claude Code Architecture
# Updated: 2026-02-16

# Gmail Watcher - Check every 2 minutes
*/2 * * * * /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault/cron_gmail_watcher.sh

# LinkedIn Poster - Run every hour
0 * * * * /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault/cron_linkedin_poster.sh

# Claude Code Planner - Run every 5 minutes (NEW)
*/5 * * * * /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault/cron_claude_planner.sh

# Claude Code Executor - Run every 5 minutes (NEW)
*/5 * * * * /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault/cron_claude_executor.sh

# Daily cleanup - Remove old logs (keep last 7 days)
0 0 * * * find /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault/Memory/cron_logs -name "*.log" -mtime +7 -delete
```

## To Apply:
```bash
# Backup current crontab
crontab -l > crontab_backup_$(date +%Y%m%d).txt

# Edit crontab
crontab -e

# Remove these lines:
# */5 * * * * .../cron_bronze_planner.sh
# */5 * * * * .../cron_silver_executor.sh

# Add these lines:
# */5 * * * * .../cron_claude_planner.sh
# */5 * * * * .../cron_claude_executor.sh

# Verify
crontab -l
```

## What Changed:
- **Old:** Direct Python calls to bronze_planner.py and silver_executor.py
- **New:** Claude Code orchestrator invokes Agent Skills
- **Result:** Hackathon compliant architecture

## Architecture Flow:
```
Old (Non-compliant):
Cron → Python script → Gemini API → Write file

New (Compliant):
Cron → Claude Code Orchestrator → Agent Skill → Gemini API → Write file
```

The orchestrator acts as the "reasoning engine" that decides which skills to invoke.
