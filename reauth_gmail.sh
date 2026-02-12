#!/bin/bash
# Re-authenticate Gmail with send permissions

echo "================================================"
echo "🔐 Gmail Re-authentication (with Send Permissions)"
echo "================================================"
echo ""
echo "This will:"
echo "1. Authenticate Gmail with READ + SEND permissions"
echo "2. Convert token for MCP server"
echo "3. Verify setup"
echo ""
echo "================================================"
echo ""

cd ~/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault

# Activate virtual environment
source venv/bin/activate

# Set BROWSER variable
export BROWSER=~/open-browser.sh

# Run Gmail watcher (will trigger authentication)
echo "Starting Gmail watcher for authentication..."
echo "After you authenticate, press Ctrl+C to stop the watcher."
echo ""

python watchers/gmail_watcher.py &
WATCHER_PID=$!

# Wait for authentication to complete
echo ""
echo "Waiting for authentication..."
sleep 5

# Check if token was created
while [ ! -f credentials/gmail_token.pickle ]; do
    sleep 2
done

echo ""
echo "✅ Authentication complete!"
echo ""

# Stop the watcher
kill $WATCHER_PID 2>/dev/null

# Convert token to JSON
echo "Converting token for MCP server..."
python mcp_servers/convert_token.py

echo ""
echo "================================================"
echo "✅ Setup Complete!"
echo "================================================"
echo ""
echo "Your Gmail is now authenticated with:"
echo "  ✅ Read emails"
echo "  ✅ Send emails"
echo "  ✅ Compose drafts"
echo ""
echo "Next: Restart Claude Code to load the Email MCP server"
echo "================================================"
