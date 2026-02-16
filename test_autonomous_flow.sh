#!/bin/bash
# Test script to demonstrate the autonomous flow

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           🧪 TESTING AUTONOMOUS WORKFLOW                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "📊 Current Status:"
echo "  Needs_Action: $(ls Needs_Action/*.md 2>/dev/null | wc -l) tasks waiting"
echo "  Plans: $(ls Plans/*.md 2>/dev/null | wc -l) plans created"
echo "  Approvals: $(ls Approvals/*.md 2>/dev/null | wc -l) awaiting approval"
echo "  Done: $(ls Done/*.md 2>/dev/null | wc -l) tasks completed"
echo ""

echo "⏰ Cron Jobs Status:"
crontab -l | grep -E "(gmail_watcher|bronze_planner|silver_executor|linkedin_poster)" | while read line; do
  echo "  ✓ $line"
done
echo ""

echo "📝 Recent Activity (last 5 log entries):"
if [ -f Memory/cron_logs/gmail_watcher.log ]; then
  echo "  Gmail Watcher:"
  tail -5 Memory/cron_logs/gmail_watcher.log | sed 's/^/    /'
fi
echo ""

echo "🎯 What Happens Next:"
echo "  1. Gmail Watcher runs every 2 min (detecting emails)"
echo "  2. Bronze Planner runs every 5 min (creating plans)"
echo "  3. You approve tasks manually (edit Approvals/ files)"
echo "  4. Silver Executor runs every 5 min (executing tasks)"
echo ""

echo "⚠️  Current Limitation:"
echo "  Gemini API quota exhausted (resets in ~24 hours)"
echo "  Bronze Planner and Silver Executor will work tomorrow"
echo ""

echo "✅ Your AI Employee is configured and ready!"
