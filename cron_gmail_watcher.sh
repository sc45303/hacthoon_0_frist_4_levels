#!/bin/bash
cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
source venv/bin/activate
python watchers/gmail_watcher.py >> Memory/cron_logs/gmail_watcher.log 2>&1
