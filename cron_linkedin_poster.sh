#!/bin/bash
cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
source venv/bin/activate
python watchers/linkedin_poster_enhanced.py >> Memory/cron_logs/linkedin_poster.log 2>&1
