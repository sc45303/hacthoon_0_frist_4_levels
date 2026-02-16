# 📧 EMAIL SENDING - COMPLETE GUIDE FOR YOUR SETUP

Since you're using `claude-code-router`, the MCP servers don't load automatically. Here are **3 working methods** to send emails:

---

## ✅ METHOD 1: Direct Python Script (Easiest)

### Send Email from Command Line

```bash
cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
source venv/bin/activate

python send_email.py "recipient@email.com" "Subject Here" "Email body text here"
```

**Example:**
```bash
python send_email.py "mygamingchanal786@gmail.com" "Test from AI Employee" "Hello! This email was sent by my AI Employee system."
```

### Ask Claude to Send Email

When you want me (Claude) to send an email, just say:

```
Send an email to mygamingchanal786@gmail.com with subject "Test" and body "Hello from AI Employee"
```

I'll use the Python script via bash to send it!

---

## ✅ METHOD 2: Interactive Python Script

For more complex emails with formatting:

```bash
cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
source venv/bin/activate

python send_email_interactive.py '{"to":"recipient@email.com","subject":"Test","body":"Message here"}'
```

---

## ✅ METHOD 3: Create Email Tasks

Create a task file that your AI Employee will process:

```bash
cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
nano Needs_Action/SEND_EMAIL_test.md
```

Add this content:
```markdown
---
type: email_send
to: mygamingchanal786@gmail.com
subject: Test Email
priority: high
---

# Task: Send Email

**To:** mygamingchanal786@gmail.com
**Subject:** Test Email

## Email Body

Hello!

This is a test email from my Personal AI Employee system.

Best regards,
Your AI Employee

## Actions
- [ ] Send this email
```

Then ask Claude to process it:
```
Read the file Needs_Action/SEND_EMAIL_test.md and send the email using the send_email.py script
```

---

## 🔧 SOLUTION 2: Fix MCP for Router (Advanced)

If you want the MCP server to work with claude-code-router, you need to modify the router settings.

**Option A: Add MCP to Router Settings**

The router uses settings from `/tmp/claude-code-router/ccr-settings-*.json`. This file is regenerated each time, so we need to modify the router itself or use environment variables.

**Option B: Use Standard Claude Code**

Stop using the router temporarily:
```bash
# Kill router
pkill -f claude-code-router

# Start normal Claude Code
unset CLAUDECODE
claude
```

Then the MCP servers in `~/.config/claude-code/mcp_config.json` will load.

---

## 📊 COMPARISON

| Method | Pros | Cons |
|--------|------|------|
| **Python Script** | ✅ Works immediately<br>✅ No config needed<br>✅ Simple | ❌ Manual command |
| **Task Files** | ✅ Automated workflow<br>✅ Trackable | ❌ Extra file creation |
| **Fix MCP** | ✅ Native integration<br>✅ Best UX | ❌ Complex setup<br>❌ May break router |

**Recommendation:** Use Method 1 (Python Script) - it's simple and works perfectly with your setup.

---

## 🧪 TEST IT NOW

Run this command to send a test email:

```bash
cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault
source venv/bin/activate
python send_email.py "mygamingchanal786@gmail.com" "Test from AI Employee" "Success! Your AI Employee can send emails."
```

Check your inbox - you should receive the email within seconds!

---

## 💡 FOR CLAUDE TO SEND EMAILS

When you ask me to send an email, I'll automatically use the Python script like this:

```bash
cd /home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault && source venv/bin/activate && python send_email.py "recipient@email.com" "Subject" "Body text"
```

You don't need to do anything special - just ask naturally!
