#!/bin/bash
# Cron Scheduler Setup for Personal AI Employee
# This script sets up automated scheduling for all watchers and posters

PROJECT_DIR="/home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault"
VENV_DIR="$PROJECT_DIR/venv"
LOG_DIR="$PROJECT_DIR/Memory/cron_logs"

# Create log directory
mkdir -p "$LOG_DIR"

echo "="
echo "🕐 Personal AI Employee - Cron Scheduler Setup"
echo "="
echo ""

# Check if we're on WSL or Linux
if grep -qi microsoft /proc/version; then
    echo "📍 Detected: WSL (Windows Subsystem for Linux)"
    PLATFORM="wsl"
else
    echo "📍 Detected: Native Linux"
    PLATFORM="linux"
fi

echo ""
echo "📁 Project Directory: $PROJECT_DIR"
echo "📁 Log Directory: $LOG_DIR"
echo ""

# Create wrapper scripts for each task
echo "📝 Creating wrapper scripts..."

# Gmail Watcher wrapper
cat > "$PROJECT_DIR/cron_gmail_watcher.sh" << 'EOF'
#!/bin/bash
cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
source venv/bin/activate
python watchers/gmail_watcher.py >> Memory/cron_logs/gmail_watcher.log 2>&1
EOF
chmod +x "$PROJECT_DIR/cron_gmail_watcher.sh"
echo "✅ Created: cron_gmail_watcher.sh"

# LinkedIn Poster wrapper
cat > "$PROJECT_DIR/cron_linkedin_poster.sh" << 'EOF'
#!/bin/bash
cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
source venv/bin/activate
python watchers/linkedin_poster.py >> Memory/cron_logs/linkedin_poster.log 2>&1
EOF
chmod +x "$PROJECT_DIR/cron_linkedin_poster.sh"
echo "✅ Created: cron_linkedin_poster.sh"

# Create crontab entries file
CRON_FILE="$PROJECT_DIR/crontab_entries.txt"

cat > "$CRON_FILE" << EOF
# Personal AI Employee - Automated Tasks
# Generated on $(date)

# Gmail Watcher - Check every 2 minutes
*/2 * * * * $PROJECT_DIR/cron_gmail_watcher.sh

# LinkedIn Poster - Run every hour
0 * * * * $PROJECT_DIR/cron_linkedin_poster.sh

# Daily cleanup - Remove old logs (keep last 7 days)
0 0 * * * find $LOG_DIR -name "*.log" -mtime +7 -delete

EOF

echo "✅ Created: crontab_entries.txt"
echo ""

# Display the cron entries
echo "📋 Cron Schedule:"
echo "─────────────────────────────────────────────────────────"
cat "$CRON_FILE"
echo "─────────────────────────────────────────────────────────"
echo ""

# Instructions for installation
echo "🔧 Installation Instructions:"
echo ""
echo "To install these cron jobs, run:"
echo ""
echo "  crontab -e"
echo ""
echo "Then add the contents of: $CRON_FILE"
echo ""
echo "Or automatically install with:"
echo ""
echo "  crontab -l > /tmp/current_cron 2>/dev/null || true"
echo "  cat $CRON_FILE >> /tmp/current_cron"
echo "  crontab /tmp/current_cron"
echo "  rm /tmp/current_cron"
echo ""

# Check if cron is running
if command -v crontab &> /dev/null; then
    echo "✅ crontab command available"

    if systemctl is-active --quiet cron 2>/dev/null || service cron status &>/dev/null; then
        echo "✅ Cron service is running"
    else
        echo "⚠️  Cron service may not be running"
        echo "   Start with: sudo service cron start"
    fi
else
    echo "❌ crontab not found - install cron first"
fi

echo ""
echo "="
echo "✅ Cron Scheduler Setup Complete!"
echo "="
echo ""
echo "📊 Monitoring:"
echo "  - Gmail logs: tail -f $LOG_DIR/gmail_watcher.log"
echo "  - LinkedIn logs: tail -f $LOG_DIR/linkedin_poster.log"
echo "  - View cron jobs: crontab -l"
echo ""
