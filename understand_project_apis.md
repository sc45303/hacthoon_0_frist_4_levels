# Personal AI Employee - APIs & Integrations

**Part 4 of 5** | [← Back to How To Run](understand_project_howto.md) | [Next: Capabilities →](understand_project_capabilities.md)

---

## 🔌 APIs Used in This Project

### 1. Google Gemini AI API

**Purpose:** AI brain for planning and reasoning

**Model:** `gemini-2.5-flash`

**What it does:**
- Generates execution plans for tasks
- Analyzes task complexity
- Creates step-by-step instructions
- Provides AI reasoning

**How to get API key:**
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key
5. Add to `.env` file: `GEMINI_API_KEY=your_key_here`

**Usage in code:**
```python
from agent.gemini_brain import think

plan = think("Write a haiku about AI")
# Returns: AI-generated plan
```

**Cost:** Free tier includes 60 requests per minute

**Limitations:**
- Rate limits on free tier
- Context window: ~32k tokens
- May refuse certain requests

---

### 2. Gmail API

**Purpose:** Email monitoring and sending

**Version:** v1

**What it does:**
- Read emails from inbox
- Send emails
- Create draft replies
- Search emails
- Mark emails as read/unread

**Authentication:** OAuth2

**Scopes used:**
- `https://www.googleapis.com/auth/gmail.readonly` - Read emails
- `https://www.googleapis.com/auth/gmail.send` - Send emails
- `https://www.googleapis.com/auth/gmail.compose` - Create drafts

**How to set up:**

1. **Create Google Cloud Project:**
   - Visit: https://console.cloud.google.com/
   - Create new project: "AI Employee"
   - Note the project ID

2. **Enable Gmail API:**
   - Go to "APIs & Services" > "Library"
   - Search "Gmail API"
   - Click "Enable"

3. **Create OAuth2 Credentials:**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "AI Employee Gmail"
   - Download JSON file
   - Save as `credentials/gmail_credentials.json`

4. **Add Test User (for development):**
   - Go to "OAuth consent screen"
   - Add your email as test user
   - This allows you to use the app while in testing mode

5. **Authenticate:**
   ```bash
   python watchers/gmail_watcher.py
   # Follow authentication prompts
   ```

**API Endpoints used:**

```javascript
// List messages
GET https://gmail.googleapis.com/gmail/v1/users/me/messages
?q=is:unread is:important
&maxResults=10

// Get message details
GET https://gmail.googleapis.com/gmail/v1/users/me/messages/{messageId}

// Send email
POST https://gmail.googleapis.com/gmail/v1/users/me/messages/send
Body: { raw: base64EncodedEmail }

// Create draft
POST https://gmail.googleapis.com/gmail/v1/users/me/drafts
Body: { message: { raw: base64EncodedEmail } }
```

**Rate Limits:**
- 250 quota units per user per second
- 1 billion quota units per day
- Most operations cost 5-10 units

**Cost:** Free (within quota limits)

---

### 3. LinkedIn API

**Purpose:** Social media posting

**Version:** v2 (UGC Posts API)

**What it does:**
- Post text updates
- Post articles with URLs
- Share content
- Control post visibility

**Authentication:** OAuth2

**Scopes used:**
- `openid` - Basic authentication
- `profile` - User profile data
- `w_member_social` - Post to LinkedIn

**How to set up:**

1. **Create LinkedIn App:**
   - Visit: https://www.linkedin.com/developers/apps
   - Click "Create app"
   - Fill in details:
     - App name: "Personal AI Employee"
     - LinkedIn Page: (select your page or create one)
     - App logo: (optional)
   - Click "Create app"

2. **Add Products:**
   - In app dashboard, go to "Products" tab
   - Add "Share on LinkedIn" (Default Tier)
   - Add "Sign In with LinkedIn using OpenID Connect" (Standard Tier)
   - Wait 5-10 minutes for products to activate

3. **Configure OAuth:**
   - Go to "Auth" tab
   - Add redirect URL: `http://localhost:8080/callback`
   - Note Client ID and Client Secret
   - Save to `credentials/linkedin_credentials.json`:
     ```json
     {
       "client_id": "your_client_id",
       "client_secret": "your_client_secret",
       "redirect_uri": "http://localhost:8080/callback"
     }
     ```

4. **Authenticate:**
   ```bash
   python authenticate_linkedin_openid.py
   # Follow prompts to get access token
   ```

**API Endpoints used:**

```javascript
// Post to LinkedIn
POST https://api.linkedin.com/v2/ugcPosts
Headers:
  Authorization: Bearer {access_token}
  X-Restli-Protocol-Version: 2.0.0
  Content-Type: application/json

Body (text post):
{
  "author": "urn:li:person:PERSON_ID",
  "lifecycleState": "PUBLISHED",
  "specificContent": {
    "com.linkedin.ugc.ShareContent": {
      "shareCommentary": {
        "text": "Your post content"
      },
      "shareMediaCategory": "NONE"
    }
  },
  "visibility": {
    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
  }
}
```

**Rate Limits:**
- 100 posts per day per person
- 25 posts per hour per person
- Throttling on rapid requests

**Cost:** Free (within limits)

**Token Expiration:**
- Access tokens expire after 60 days
- Need to re-authenticate when expired

---

### 4. Model Context Protocol (MCP)

**Purpose:** Connect AI models to external tools

**Version:** 1.0.0

**What it does:**
- Provides standardized protocol for AI tool use
- Allows Claude to call external functions
- Enables email sending, LinkedIn posting, etc.

**How it works:**

1. **MCP Server (Node.js):**
   - Runs as separate process
   - Communicates via stdio
   - Exposes tools to Claude
   - Handles authentication and API calls

2. **MCP Configuration:**
   - Located: `~/.config/claude-code/mcp_config.json`
   - Defines available servers
   - Specifies command to run each server

3. **Tool Definition:**
   ```javascript
   {
     name: 'send_email',
     description: 'Send an email via Gmail',
     inputSchema: {
       type: 'object',
       properties: {
         to: { type: 'string' },
         subject: { type: 'string' },
         body: { type: 'string' }
       },
       required: ['to', 'subject', 'body']
     }
   }
   ```

4. **Tool Execution:**
   - Claude calls tool with parameters
   - MCP server receives request
   - Server executes action (e.g., send email)
   - Returns result to Claude
   - Claude shows result to user

**MCP Servers in this project:**

1. **Email MCP** (`mcp_servers/email_mcp/`)
   - Tools: send_email, draft_reply, search_emails
   - Uses Gmail API

2. **LinkedIn MCP** (`mcp_servers/linkedin_mcp/`)
   - Tools: post_to_linkedin, post_article_to_linkedin
   - Uses LinkedIn API

**Documentation:** https://modelcontextprotocol.io/

---

## 🔐 Credential Management

### Files and Their Purpose

```
credentials/
├── gmail_credentials.json      # OAuth2 app credentials (from Google Cloud)
├── gmail_token.pickle          # Python Gmail auth token
├── gmail_token.json            # Node.js Gmail auth token (for MCP)
├── linkedin_credentials.json   # OAuth2 app credentials (from LinkedIn)
└── linkedin_token.json         # LinkedIn access token
```

### Security Best Practices

**DO:**
- ✅ Keep credentials in `credentials/` folder
- ✅ Add `credentials/` to `.gitignore`
- ✅ Use environment variables for API keys (`.env` file)
- ✅ Restrict file permissions: `chmod 600 credentials/*`
- ✅ Regularly rotate tokens

**DON'T:**
- ❌ Commit credentials to Git
- ❌ Share credentials publicly
- ❌ Hardcode API keys in code
- ❌ Use production credentials for testing

### Token Expiration

**Gmail tokens:**
- Refresh tokens: Don't expire (unless revoked)
- Access tokens: Expire after 1 hour (auto-refreshed)

**LinkedIn tokens:**
- Access tokens: Expire after 60 days
- Need to re-authenticate when expired

**Gemini API keys:**
- Don't expire (unless revoked)
- Can be rotated manually

---

## 🔄 Running Without Claude (Alternative AI)

You asked: "How can I run my AI employee without using Claude?"

**Answer:** Your AI employee already runs without Claude!

### Current Setup

**AI Brain:** Google Gemini (not Claude)
- File: `agent/gemini_brain.py`
- Model: `gemini-2.5-flash`
- Used for: Task planning and reasoning

**Claude's Role:**
- Claude Code (me) is just the development assistant
- Claude helps you write code and debug
- Claude is NOT the AI brain of your employee

### Your AI Employee Uses:

1. **Google Gemini** - For planning and reasoning
2. **Gmail API** - For email operations
3. **LinkedIn API** - For social media
4. **Python/Node.js** - For execution

### To Run Completely Standalone:

```bash
# Your AI employee runs independently:

# 1. Gmail watcher (runs via cron)
# Uses: Gmail API + Python
# No Claude needed

# 2. LinkedIn poster (runs via cron)
# Uses: LinkedIn API + Python
# No Claude needed

# 3. Task planner (runs when task detected)
# Uses: Gemini AI + Python
# No Claude needed

# 4. Task executor (runs when approved)
# Uses: Python only
# No Claude needed
```

### MCP Servers (Optional)

MCP servers are only used when you want to control your AI employee through Claude Code's chat interface.

**Without MCP:**
- Everything still works
- Use Python scripts directly
- Use cron for automation
- No chat interface

**With MCP:**
- Can control via chat: "Send email to..."
- More convenient for manual operations
- Still uses same APIs underneath

### Alternative AI Models

You can replace Gemini with other AI models:

**Option 1: OpenAI GPT**
```python
# Replace agent/gemini_brain.py with:
import openai

def think(task_text: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": task_text}]
    )
    return response.choices[0].message.content
```

**Option 2: Anthropic Claude API**
```python
# Replace agent/gemini_brain.py with:
import anthropic

def think(task_text: str) -> str:
    client = anthropic.Anthropic(api_key="your_key")
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": task_text}]
    )
    return response.content[0].text
```

**Option 3: Local LLM (Ollama)**
```python
# Replace agent/gemini_brain.py with:
import requests

def think(task_text: str) -> str:
    response = requests.post('http://localhost:11434/api/generate',
        json={"model": "llama2", "prompt": task_text})
    return response.json()['response']
```

---

## 🤖 When Will It Be Fully Automatic 24/7?

**Answer:** It's ALREADY running 24/7!

### What's Automatic Now:

✅ **Gmail Watcher** - Runs every 2 minutes via cron
✅ **LinkedIn Poster** - Runs every hour via cron
✅ **Log Cleanup** - Runs daily at midnight

### What Requires Manual Action:

⚠️ **Task Approval** - You must approve plans before execution
⚠️ **LinkedIn Authentication** - Need to authenticate once

### To Make It Fully Autonomous:

**Option 1: Auto-approve simple tasks**
```python
# Modify agent/bronze_planner.py
# Add auto-approval for low-risk tasks
if task_complexity == "low" and task_type in ["read", "search"]:
    auto_approve(task)
```

**Option 2: Remove approval requirement**
```python
# Modify agent/silver_orchestrator.py
# Skip approval check (RISKY!)
# Execute tasks immediately after planning
```

**Option 3: Use confidence thresholds**
```python
# Only require approval for uncertain tasks
if confidence_score < 0.8:
    request_approval()
else:
    execute_immediately()
```

### Current Workflow:

```
Automatic → Manual → Automatic
   ↓          ↓         ↓
Detect    Approve   Execute
```

### Fully Automatic Workflow (Risky):

```
Automatic → Automatic → Automatic
   ↓          ↓           ↓
Detect    Auto-approve  Execute
```

**Recommendation:** Keep human approval for safety!

---

**Continue to: understand_project_capabilities.md**
