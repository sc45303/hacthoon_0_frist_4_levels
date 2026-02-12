# 📧 Email MCP Server

## Overview

The Email MCP Server provides Gmail operations to Claude Code via the Model Context Protocol.

**Capabilities:**
- ✅ Send emails via Gmail
- ✅ Create draft replies to emails
- ✅ Search Gmail inbox

---

## 🎯 What This Enables

**Complete Email Workflow:**
1. Gmail Watcher detects incoming email → Creates task
2. AI generates reply plan → You approve
3. **Email MCP sends the reply** ← This server

---

## ✅ Setup Complete

Your Email MCP Server is configured and ready to use!

**Files created:**
- `index.js` - MCP server implementation
- `package.json` - Dependencies
- `~/.config/claude-code/mcp_config.json` - Claude Code configuration

**Credentials:**
- Using same Gmail credentials as Gmail Watcher
- Token converted to JSON format

---

## 🚀 How to Use

### In Claude Code

The Email MCP Server runs automatically when you use Claude Code. You now have access to these tools:

#### 1. Send Email
```
Send an email to user@example.com with subject "Hello" and body "This is a test"
```

#### 2. Draft Reply
```
Create a draft reply to email ID 19c52a47b16eed4d with body "Thank you for your message"
```

#### 3. Search Emails
```
Search my Gmail for emails from john@example.com that are unread
```

---

## 🧪 Testing the Server

### Test 1: Verify Server Starts

Restart Claude Code to load the MCP server:
```bash
# Exit Claude Code (Ctrl+D)
# Start Claude Code again
claude-code
```

You should see the Email MCP server load automatically.

### Test 2: Search Emails

In Claude Code, ask:
```
Search my Gmail for recent emails
```

Expected: Claude will use the `search_emails` tool and show results.

### Test 3: Send Test Email

In Claude Code, ask:
```
Send a test email to myself (sc3078745@gmail.com) with subject "MCP Test" and body "Testing Email MCP Server"
```

Expected: Email sent successfully, you'll receive it in your inbox.

### Test 4: Draft Reply

First, get an email ID from the Gmail watcher task files:
```bash
cat Needs_Action/EMAIL_*.md | grep gmail_id
```

Then in Claude Code:
```
Create a draft reply to email ID [paste-id-here] saying "Thank you for reaching out"
```

Expected: Draft created in Gmail.

---

## 🔧 Available Tools

### send_email
**Purpose:** Send an email via Gmail

**Parameters:**
- `to` (required): Recipient email address
- `subject` (required): Email subject
- `body` (required): Email body (plain text)
- `cc` (optional): CC email addresses (comma-separated)

**Example:**
```json
{
  "to": "user@example.com",
  "subject": "Meeting Follow-up",
  "body": "Thank you for the meeting today. Here are the action items...",
  "cc": "manager@example.com"
}
```

### draft_reply
**Purpose:** Create a draft reply to an email

**Parameters:**
- `message_id` (required): Gmail message ID to reply to
- `body` (required): Reply body (plain text)

**Example:**
```json
{
  "message_id": "19c52a47b16eed4d",
  "body": "Thank you for your email. I will review this and get back to you."
}
```

### search_emails
**Purpose:** Search Gmail inbox

**Parameters:**
- `query` (required): Gmail search query
- `max_results` (optional): Maximum results (default: 10)

**Example queries:**
- `"from:user@example.com"` - Emails from specific sender
- `"is:unread is:important"` - Unread important emails
- `"subject:invoice"` - Emails with "invoice" in subject
- `"after:2026/02/01"` - Emails after specific date

---

## 🎯 End-to-End Workflow Example

### Scenario: Reply to an Important Email

**Step 1: Gmail Watcher Detects Email**
```
📧 Created task from email: "URGENT: Project Update"
   From: boss@company.com
   Priority: urgent
```

**Step 2: Review Task File**
```bash
cat Needs_Action/EMAIL_URGENT_Project_Update_19c52a47.md
```

**Step 3: Ask Claude to Draft Reply**
```
Read the email task file EMAIL_URGENT_Project_Update_19c52a47.md and draft a professional reply
```

**Step 4: Claude Generates Reply**
Claude reads the task, understands context, and drafts a reply.

**Step 5: Approve and Send**
```
Send that reply to the email with ID 19c52a47b16eed4d
```

**Step 6: Email Sent!**
```
✅ Email sent successfully!
To: boss@company.com
Subject: Re: URGENT: Project Update
```

---

## 🔍 Troubleshooting

### Server Not Loading

**Check MCP config:**
```bash
cat ~/.config/claude-code/mcp_config.json
```

Should show the email server configuration.

**Restart Claude Code:**
```bash
# Exit and restart
claude-code
```

### Authentication Errors

**Verify token exists:**
```bash
ls -lh credentials/gmail_token.json
```

**Regenerate token if needed:**
```bash
# Run Gmail watcher to re-authenticate
./run_gmail_watcher.sh
# Then convert token again
source venv/bin/activate
python mcp_servers/convert_token.py
```

### Permission Errors

The Gmail API needs the `gmail.send` scope to send emails. If you get permission errors:

1. Delete the token:
```bash
rm credentials/gmail_token.pickle credentials/gmail_token.json
```

2. Update Gmail watcher to request send permission:
```python
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.compose'
]
```

3. Re-authenticate:
```bash
./run_gmail_watcher.sh
```

---

## 📊 Success Metrics

Email MCP Server is working when:
- ✅ Server loads in Claude Code without errors
- ✅ Search emails returns results
- ✅ Send email delivers messages
- ✅ Draft reply creates drafts in Gmail
- ✅ End-to-end workflow completes: Email arrives → Reply sent

---

## 🎓 What You've Achieved

With Gmail Watcher + Email MCP Server, you now have:
- ✅ **Read emails** - Gmail Watcher monitors inbox
- ✅ **Send emails** - Email MCP sends replies
- ✅ **Complete automation** - End-to-end email workflow

**This is a MAJOR milestone!** Your AI employee can now handle real email communication.

---

## 📝 Next Steps

Now that email workflow is complete, you can:
1. Test the end-to-end workflow
2. Build WhatsApp Watcher (monitor WhatsApp messages)
3. Build LinkedIn Auto-Poster (generate sales leads)
4. Complete Silver Tier requirements

---

**Email MCP Server Ready!**
**Date:** 2026-02-12
**Status:** ✅ Configured and ready to use
