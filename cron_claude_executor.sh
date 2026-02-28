#!/bin/bash
# Cron script for Automatic Task Executor
# Runs every 5 minutes to execute approved tasks

cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault

# Check if already running
if pgrep -f "auto_executor.py" > /dev/null; then
    echo "[$(date)] Executor already running, skipping" >> Memory/cron_logs/claude_executor.log
    exit 0
fi

# Activate virtual environment and run
source venv/bin/activate
# Add node to PATH for claude command
export PATH="/home/sk/.nvm/versions/node/v20.20.0/bin:$PATH"
python auto_executor.py >> Memory/cron_logs/claude_executor.log 2>&1

echo "[$(date)] Executor check completed" >> Memory/cron_logs/claude_executor.log
