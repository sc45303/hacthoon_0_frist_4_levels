#!/bin/bash
# Cron script to run Silver Executor

cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
source venv/bin/activate

# Run Silver Executor
python -m agent.silver_executor >> Memory/cron_logs/silver_executor.log 2>&1

# Log completion
echo "[$(date)] Silver Executor completed" >> Memory/cron_logs/silver_executor.log
