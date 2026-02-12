#!/bin/bash
# LinkedIn Poster Launcher Script

echo "🔗 Starting LinkedIn Auto-Poster..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found"
    echo "   Run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if credentials exist
if [ ! -f "credentials/linkedin_credentials.json" ]; then
    echo "❌ LinkedIn credentials not found"
    echo "   Please create credentials/linkedin_credentials.json"
    echo "   See LINKEDIN_POSTER_GUIDE.md for instructions"
    exit 1
fi

# Check if token exists
if [ ! -f "credentials/linkedin_token.json" ]; then
    echo "⚠️  No authentication token found"
    echo "   Running authentication flow..."
    echo ""
    python authenticate_linkedin.py
    echo ""
fi

# Run the poster
python watchers/linkedin_poster.py
