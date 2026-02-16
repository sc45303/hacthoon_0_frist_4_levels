#!/bin/bash
# AI Employee System Status Dashboard

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        🤖 Personal AI Employee - System Status            ║"
echo "╔════════════════════════════════════════════════════════════╗"
echo ""

# Check Gmail Watcher
echo "📧 GMAIL WATCHER"
if ps aux | grep -v grep | grep gmail_watcher.py > /dev/null; then
    echo "   Status: ✅ Running"
    echo "   PID: $(ps aux | grep -v grep | grep gmail_watcher.py | awk '{print $2}')"
else
    echo "   Status: ⚠️  Not running"
    echo "   Start: ./run_gmail_watcher.sh"
fi
echo "   Last check: $(tail -1 Memory/cron_logs/gmail_watcher.log 2>/dev/null | cut -c1-19 || echo 'No logs yet')"
echo ""

# Check Task Folders
echo "📁 TASK FOLDERS"
echo "   Needs_Action: $(ls Needs_Action/ 2>/dev/null | wc -l) tasks waiting"
echo "   Plans: $(ls Plans/ 2>/dev/null | wc -l) plans created"
echo "   Approvals: $(ls Approvals/ 2>/dev/null | wc -l) awaiting approval"
echo "   Done: $(ls Done/ 2>/dev/null | wc -l) tasks completed"
echo "   Logs: $(ls Logs/ 2>/dev/null | wc -l) execution logs"
echo ""

# Check LinkedIn
echo "🔗 LINKEDIN POSTING"
echo "   Posts queued: $(ls Posts_Queue/*.md 2>/dev/null | wc -l)"
echo "   Posts published: $(ls Posts_Queue/posted/ 2>/dev/null | wc -l)"
echo "   Last post: $(tail -1 Memory/cron_logs/linkedin_poster.log 2>/dev/null | cut -c1-19 || echo 'No posts yet')"
echo ""

# Check Credentials
echo "🔐 CREDENTIALS"
if [ -f "credentials/gmail_token.pickle" ]; then
    echo "   Gmail: ✅ Authenticated"
else
    echo "   Gmail: ❌ Not authenticated"
fi
if [ -f "credentials/linkedin_token.json" ]; then
    echo "   LinkedIn: ✅ Authenticated"
else
    echo "   LinkedIn: ❌ Not authenticated"
fi
echo ""

# Check Cron Jobs
echo "⏰ AUTOMATION (CRON)"
CRON_COUNT=$(crontab -l 2>/dev/null | grep -v "^#" | grep -v "^$" | wc -l)
echo "   Active jobs: $CRON_COUNT"
echo "   - Gmail watcher: Every 2 minutes"
echo "   - LinkedIn poster: Every hour"
echo "   - Log cleanup: Daily at midnight"
echo ""

# Recent Activity
echo "📊 RECENT ACTIVITY"
echo "   Emails processed: $(cat Memory/processed_emails.json 2>/dev/null | grep -o '19[a-z0-9]*' | wc -l)"
if [ -f "Memory/task_history.json" ]; then
    echo "   Task history: ✅ Tracking"
else
    echo "   Task history: ⚠️  No history yet"
fi
echo ""

# Quick Actions
echo "🚀 QUICK ACTIONS"
echo "   Check new emails: ls -lh Needs_Action/"
echo "   Create plans: python -m agent.bronze_planner"
echo "   Execute tasks: python -m agent.silver_executor"
echo "   Post to LinkedIn: python watchers/linkedin_poster.py"
echo "   View logs: tail -f Memory/cron_logs/gmail_watcher.log"
echo ""

echo "╚════════════════════════════════════════════════════════════╝"
