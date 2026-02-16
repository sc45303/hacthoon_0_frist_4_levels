#!/bin/bash
# Quick LinkedIn Post Script
# Usage: ./quick_post.sh "Your post content here"

cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault

# Generate filename with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="Posts_Queue/quick_post_${TIMESTAMP}.md"

# Create post file
cat > "$FILENAME" << EOF
---
type: text
visibility: PUBLIC
---

$1
EOF

echo "✅ Post created: $FILENAME"
echo "📤 Posting to LinkedIn..."

# Activate venv and post immediately
source venv/bin/activate
python watchers/linkedin_poster.py

echo "🎉 Done! Check your LinkedIn profile."
