#!/bin/bash
# Cron script to run Bronze Planner

cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
source venv/bin/activate

# Run Bronze Planner
python -m agent.bronze_planner >> Memory/cron_logs/bronze_planner.log 2>&1

# Log completion
echo "[$(date)] Bronze Planner completed" >> Memory/cron_logs/bronze_planner.log
