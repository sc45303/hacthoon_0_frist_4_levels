#!/bin/bash
# Cron script for Claude Code Executor
# Runs every 5 minutes to execute approved tasks

cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault

# Check if already running
if pgrep -f "orchestrator_claude.py execute" > /dev/null; then
    echo "[$(date)] Executor already running, skipping" >> Memory/cron_logs/claude_executor.log
    exit 0
fi

# Activate virtual environment and run
source venv/bin/activate
python orchestrator_claude.py execute >> Memory/cron_logs/claude_executor.log 2>&1

echo "[$(date)] Claude Executor completed" >> Memory/cron_logs/claude_executor.log
