#!/bin/bash
# Gmail Watcher - Quick Launch Script
# Sets BROWSER variable and runs Gmail watcher

export BROWSER=~/open-browser.sh
cd ~/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
source venv/bin/activate
python watchers/gmail_watcher.py
