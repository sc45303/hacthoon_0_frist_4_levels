#!/bin/bash
# Run this before your demo to ensure everything is ready

echo "🔍 PRE-DEMO CHECKLIST"
echo "===================="
echo ""

# Check Gmail Watcher
if ps aux | grep -v grep | grep gmail_watcher.py > /dev/null; then
    echo "✅ Gmail Watcher is running"
else
    echo "❌ Gmail Watcher NOT running - Start with: ./run_gmail_watcher.sh"
fi

# Check credentials
if [ -f "credentials/gmail_token.pickle" ] && [ -f "credentials/linkedin_token.json" ]; then
    echo "✅ All credentials authenticated"
else
    echo "❌ Missing credentials"
fi

# Check cron
CRON_COUNT=$(crontab -l 2>/dev/null | grep -v "^#" | grep -v "^$" | wc -l)
if [ "$CRON_COUNT" -eq 3 ]; then
    echo "✅ All 3 cron jobs active"
else
    echo "⚠️  Expected 3 cron jobs, found $CRON_COUNT"
fi

# Check demo task
if [ -f "Done/demo_email_signature.md" ]; then
    echo "✅ Demo task ready in Done/"
else
    echo "⚠️  Demo task not found - create one for demo"
fi

# Check LinkedIn posts
POST_COUNT=$(ls Posts_Queue/posted/ 2>/dev/null | wc -l)
if [ "$POST_COUNT" -ge 1 ]; then
    echo "✅ LinkedIn posts published: $POST_COUNT"
else
    echo "⚠️  No LinkedIn posts yet"
fi

echo ""
echo "📊 QUICK STATS:"
echo "   Tasks completed: $(ls Done/ 2>/dev/null | wc -l)"
echo "   Emails processed: $(cat Memory/processed_emails.json 2>/dev/null | grep -o '19[a-z0-9]*' | wc -l)"
echo "   LinkedIn posts: $POST_COUNT"
echo ""
echo "🎬 READY TO DEMO!"
