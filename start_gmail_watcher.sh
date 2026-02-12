#!/bin/bash
# Quick Start Script for Gmail Watcher

echo "================================================"
echo "📧 Gmail Watcher - Quick Start"
echo "================================================"
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not activated"
    echo "   Activating now..."
    source venv/bin/activate
fi

# Check if credentials exist
if [ ! -f "credentials/gmail_credentials.json" ]; then
    echo "❌ Error: gmail_credentials.json not found!"
    echo ""
    echo "📋 Setup Instructions:"
    echo "1. Go to: https://console.cloud.google.com/"
    echo "2. Create a new project"
    echo "3. Enable Gmail API"
    echo "4. Create OAuth2 credentials (Desktop app)"
    echo "5. Download credentials as gmail_credentials.json"
    echo "6. Place it in: credentials/gmail_credentials.json"
    echo ""
    echo "📖 Full guide: GMAIL_WATCHER_SETUP.md"
    exit 1
fi

echo "✅ Credentials found"
echo ""

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
python -c "import google.auth" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Gmail API dependencies not installed"
    echo "   Installing now..."
    pip install -q google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies OK"
fi

echo ""
echo "🚀 Starting Gmail Watcher..."
echo "   Check interval: 2 minutes"
echo "   Monitoring: Unread + Important emails"
echo ""
echo "Press Ctrl+C to stop"
echo "================================================"
echo ""

# Run the watcher
python watchers/gmail_watcher.py
