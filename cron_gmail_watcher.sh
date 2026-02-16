#!/bin/bash
# Cron script to run Gmail Watcher (with duplicate prevention)

cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault

# Check if already running
if pgrep -f "gmail_watcher.py" > /dev/null; then
    echo "[$(date)] Gmail Watcher already running, skipping" >> Memory/cron_logs/gmail_watcher.log
    exit 0
fi

# Activate virtual environment and run
source venv/bin/activate
python watchers/gmail_watcher.py >> Memory/cron_logs/gmail_watcher.log 2>&1 &

echo "[$(date)] Gmail Watcher started" >> Memory/cron_logs/gmail_watcher.log
