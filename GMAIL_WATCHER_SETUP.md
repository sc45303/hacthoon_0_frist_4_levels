# 📧 Gmail Watcher Setup Guide
## Step-by-Step Instructions

---

## 🎯 What This Does

The Gmail Watcher will:
- Monitor your Gmail inbox every 2 minutes
- Detect unread + important emails
- Create task files in Needs_Action/
- Track processed emails to avoid duplicates
- Work continuously in the background

---

## 📋 Prerequisites

- Google account with Gmail
- Python 3.8+
- Internet connection

---

## 🚀 Setup Steps

### Step 1: Enable Gmail API (15 minutes)

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/

2. **Create a New Project**
   - Click "Select a project" → "New Project"
   - Name: "AI-Employee"
   - Click "Create"

3. **Enable Gmail API**
   - Go to: https://console.cloud.google.com/apis/library
   - Search for "Gmail API"
   - Click "Gmail API"
   - Click "Enable"

4. **Create OAuth2 Credentials**
   - Go to: https://console.cloud.google.com/apis/credentials
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure OAuth consent screen:
     - User Type: External
     - App name: "AI Employee"
     - User support email: your email
     - Developer contact: your email
     - Click "Save and Continue"
     - Scopes: Skip (click "Save and Continue")
     - Test users: Add your email
     - Click "Save and Continue"
   - Back to Create OAuth client ID:
     - Application type: "Desktop app"
     - Name: "AI Employee Gmail Watcher"
     - Click "Create"

5. **Download Credentials**
   - Click "Download JSON"
   - Save as: `gmail_credentials.json`

---

### Step 2: Install Dependencies (2 minutes)

```bash
cd AI_Employee_Vault

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Gmail API libraries
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

### Step 3: Place Credentials (1 minute)

```bash
# Create credentials directory
mkdir -p credentials

# Move downloaded file
mv ~/Downloads/gmail_credentials.json credentials/

# Verify
ls -la credentials/
# Should show: gmail_credentials.json
```

---

### Step 4: First Run - Authentication (5 minutes)

```bash
# Run the watcher for the first time
python watchers/gmail_watcher.py
```

**What will happen:**
1. Browser window opens automatically
2. Google asks you to sign in
3. Google shows: "AI Employee wants to access your Gmail"
4. Click "Allow"
5. Browser shows: "The authentication flow has completed"
6. Close browser
7. Watcher starts monitoring

**Important:** This authentication only happens once. The token is saved for future use.

---

### Step 5: Test It (5 minutes)

**Test 1: Send yourself an email**
```bash
# While watcher is running, send yourself an email:
# - To: your-email@gmail.com
# - Subject: URGENT: Test email
# - Mark as important (star it)

# Expected output in terminal:
# 📧 Created task from email: URGENT: Test email
#    From: your-email@gmail.com
#    Priority: urgent
```

**Test 2: Check task file created**
```bash
# In another terminal
ls -la Needs_Action/

# Should see: EMAIL_URGENT_Test_email_*.md
cat Needs_Action/EMAIL_URGENT_Test_email_*.md
```

---

## 🔧 Configuration

### Change Check Interval

Edit `watchers/gmail_watcher.py`:
```python
# Default: Check every 2 minutes (120 seconds)
watcher = GmailWatcher(vault_path, check_interval=120)

# Check every 5 minutes:
watcher = GmailWatcher(vault_path, check_interval=300)

# Check every 30 seconds (for testing):
watcher = GmailWatcher(vault_path, check_interval=30)
```

### Change Email Filter

Edit the query in `check_inbox()`:
```python
# Current: Unread + Important
q='is:unread is:important'

# All unread:
q='is:unread'

# Unread from specific sender:
q='is:unread from:client@example.com'

# Unread with keyword in subject:
q='is:unread subject:invoice'
```

---

## 🧪 Testing Checklist

- [ ] Gmail API enabled in Google Cloud Console
- [ ] OAuth2 credentials downloaded
- [ ] Credentials placed in `credentials/gmail_credentials.json`
- [ ] Dependencies installed
- [ ] First authentication completed
- [ ] Token saved in `credentials/gmail_token.pickle`
- [ ] Watcher running without errors
- [ ] Test email sent to yourself
- [ ] Task file created in Needs_Action/
- [ ] Email marked as processed (not detected again)

---

## 🐛 Troubleshooting

### Error: "gmail_credentials.json not found"
**Solution:** Place the downloaded credentials file in `credentials/gmail_credentials.json`

### Error: "Access blocked: This app's request is invalid"
**Solution:**
1. Go to OAuth consent screen
2. Add your email to "Test users"
3. Try authentication again

### Error: "The user has not granted the app..."
**Solution:** Click "Allow" when Google asks for permission

### Watcher not detecting emails
**Check:**
1. Email is unread
2. Email is marked as important (starred)
3. Check interval hasn't passed yet
4. Check terminal for errors

### Authentication window doesn't open
**Solution:**
1. Check firewall settings
2. Try running: `python watchers/gmail_watcher.py` directly
3. Check if port 8080 is available

---

## 🔒 Security Notes

### What's Stored:
- `credentials/gmail_credentials.json` - OAuth2 client credentials (keep private)
- `credentials/gmail_token.pickle` - Access token (keep private)
- `Memory/processed_emails.json` - List of processed email IDs (safe to share)

### What to Add to .gitignore:
```
credentials/
*.pickle
```

### Permissions Granted:
- Read-only access to Gmail
- Cannot send emails
- Cannot delete emails
- Cannot modify emails

---

## 🚀 Running in Background

### Option 1: Screen (Linux/Mac)
```bash
# Start screen session
screen -S gmail-watcher

# Run watcher
python watchers/gmail_watcher.py

# Detach: Press Ctrl+A, then D

# Reattach later
screen -r gmail-watcher
```

### Option 2: tmux (Linux/Mac)
```bash
# Start tmux session
tmux new -s gmail-watcher

# Run watcher
python watchers/gmail_watcher.py

# Detach: Press Ctrl+B, then D

# Reattach later
tmux attach -t gmail-watcher
```

### Option 3: nohup (Linux/Mac)
```bash
nohup python watchers/gmail_watcher.py > gmail_watcher.log 2>&1 &

# Check if running
ps aux | grep gmail_watcher

# Stop
pkill -f gmail_watcher.py
```

### Option 4: Windows Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: At startup
4. Action: Start a program
5. Program: `python`
6. Arguments: `watchers/gmail_watcher.py`
7. Start in: `C:\path\to\AI_Employee_Vault`

---

## 📊 Monitoring

### Check Status
```bash
# View log (if using nohup)
tail -f gmail_watcher.log

# Check processed emails
cat Memory/processed_emails.json | jq length
# Shows: Number of emails processed

# Check task files created
ls -la Needs_Action/EMAIL_*
```

### Performance
- Memory usage: ~50-100 MB
- CPU usage: <1% (idle), ~5% (checking)
- Network: Minimal (only API calls)

---

## ✅ Success Criteria

Gmail Watcher is working when:
- ✅ Runs without errors
- ✅ Detects new emails within check interval
- ✅ Creates task files in Needs_Action/
- ✅ Doesn't process same email twice
- ✅ Logs activity to terminal
- ✅ Can run in background

---

## 🎓 Next Steps

After Gmail Watcher is working:
1. Build WhatsApp Watcher (next integration)
2. Build Email MCP Server (to send replies)
3. Integrate with your planner/executor
4. Test end-to-end workflow

---

**Setup Guide Complete**
**Estimated Setup Time:** 30 minutes
**Difficulty:** Beginner-friendly
