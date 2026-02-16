#!/bin/bash
# Cron script for Claude Code Planner
# Runs every 5 minutes to process Needs_Action tasks

cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault

# Check if already running
if pgrep -f "orchestrator_claude.py plan" > /dev/null; then
    echo "[$(date)] Planner already running, skipping" >> Memory/cron_logs/claude_planner.log
    exit 0
fi

# Activate virtual environment and run
source venv/bin/activate
python orchestrator_claude.py plan >> Memory/cron_logs/claude_planner.log 2>&1

echo "[$(date)] Claude Planner completed" >> Memory/cron_logs/claude_planner.log
