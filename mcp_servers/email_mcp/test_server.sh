#!/bin/bash
# Test Email MCP Server

echo "================================================"
echo "🧪 Testing Email MCP Server"
echo "================================================"
echo ""

cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault/mcp_servers/email_mcp

echo "1. Checking Node.js version..."
node --version
echo ""

echo "2. Checking dependencies..."
if [ -d "node_modules" ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Dependencies missing - run: npm install"
    exit 1
fi
echo ""

echo "3. Checking Gmail credentials..."
if [ -f "../../credentials/gmail_credentials.json" ]; then
    echo "✅ Gmail credentials found"
else
    echo "❌ Gmail credentials missing"
    exit 1
fi
echo ""

echo "4. Checking Gmail token..."
if [ -f "../../credentials/gmail_token.json" ]; then
    echo "✅ Gmail token found"
else
    echo "❌ Gmail token missing - run Gmail watcher first"
    exit 1
fi
echo ""

echo "5. Testing MCP server startup..."
echo "   (This will start the server - press Ctrl+C to stop)"
echo ""
node index.js
