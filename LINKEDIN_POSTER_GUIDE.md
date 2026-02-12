# 🔗 LinkedIn Auto-Poster - Complete Setup Guide

## 📋 Overview

The LinkedIn Auto-Poster automatically posts content from a queue directory to your LinkedIn profile. It's part of the Silver Tier implementation for the Personal AI Employee.

## ✅ What's Already Built

- ✅ OAuth2 authentication script
- ✅ LinkedIn posting script
- ✅ Post queue system
- ✅ Logging and error handling
- ✅ Support for text and article posts

## 🚀 Setup Instructions

### Step 1: Create LinkedIn App (5 minutes)

1. **Go to LinkedIn Developer Portal**
   - Visit: https://www.linkedin.com/developers/apps
   - Sign in with your LinkedIn account

2. **Create New App**
   - Click "Create app"
   - Fill in:
     - **App name**: "Personal AI Employee"
     - **LinkedIn Page**: Select or create a company page
     - **App logo**: Optional
   - Agree to terms and create

3. **Get Your Credentials**
   - Copy your **Client ID**
   - Click "Show" and copy your **Client Secret**

4. **Configure OAuth**
   - Go to "Auth" tab
   - Add redirect URL: `http://localhost:8080/callback`
   - Click "Update"

5. **Request API Access**
   - Go to "Products" tab
   - Find "Share on LinkedIn"
   - Click "Request access" or "Add to app"
   - Wait for approval (usually instant)

### Step 2: Save Credentials

Create the credentials file:

```bash
cp credentials/linkedin_credentials.json.template credentials/linkedin_credentials.json
```

Edit `credentials/linkedin_credentials.json` and add your credentials:

```json
{
  "client_id": "YOUR_CLIENT_ID_HERE",
  "client_secret": "YOUR_CLIENT_SECRET_HERE",
  "redirect_uri": "http://localhost:8080/callback"
}
```

### Step 3: Authenticate

Run the authentication script:

```bash
source venv/bin/activate
python authenticate_linkedin.py
```

This will:
1. Open your browser for LinkedIn authorization
2. Exchange the code for an access token
3. Get your Person URN
4. Save everything to `credentials/linkedin_token.json`

### Step 4: Create Your First Post

Create a markdown file in `Posts_Queue/`:

**Example: `Posts_Queue/my_first_post.md`**

```markdown
---
type: text
visibility: PUBLIC
---

🚀 Just automated my LinkedIn posting with my Personal AI Employee!

This post was created and published automatically. The future of business automation is here!

#AI #Automation #Innovation
```

### Step 5: Run the Poster

```bash
source venv/bin/activate
python watchers/linkedin_poster.py
```

Or use the launcher script:

```bash
./run_linkedin_poster.sh
```

## 📝 Post Format

### Text Post

```markdown
---
type: text
visibility: PUBLIC
---

Your post content here!

#hashtags #work #great
```

### Article/URL Post

```markdown
---
type: article
visibility: PUBLIC
url: https://example.com/article
url_title: Article Title
url_description: Short description
---

Check out this amazing article!

It covers everything you need to know about...

#learning #growth
```

### Visibility Options

- `PUBLIC` - Anyone on LinkedIn can see (default)
- `CONNECTIONS` - Only your 1st-degree connections

## 📁 Directory Structure

```
Posts_Queue/
├── my_post.md              # Pending posts (will be processed)
├── posted/                 # Successfully posted
│   └── my_post.md
└── failed/                 # Failed posts
    └── error_post.md
```

## 🔄 Workflow

1. **Create** a `.md` file in `Posts_Queue/`
2. **Run** the poster script
3. **Post is published** to LinkedIn
4. **File moves** to `posted/` or `failed/`
5. **Check logs** in `Memory/linkedin_posts.log`

## 🧪 Testing

### Test 1: Authentication

```bash
python authenticate_linkedin.py
```

Expected output:
```
✅ Authentication Complete!
   Person URN: urn:li:person:XXXXXXXX
```

### Test 2: Post to LinkedIn

```bash
# Use the example post
python watchers/linkedin_poster.py
```

Expected output:
```
✅ Posted successfully! ID: urn:li:share:XXXXXXXX
```

### Test 3: Check LinkedIn

- Go to your LinkedIn profile
- Verify the post appears in your feed

## 📊 Rate Limits

- **Per Member**: 150 posts/day
- **Per Application**: 100,000 posts/day

The poster includes automatic rate limiting (5 seconds between posts).

## 🐛 Troubleshooting

### "Token file not found"
- Run `python authenticate_linkedin.py` first

### "Credentials file not found"
- Create `credentials/linkedin_credentials.json` from template
- Add your Client ID and Secret

### "Failed to post: 401"
- Token expired, re-authenticate
- Run `python authenticate_linkedin.py` again

### "Failed to post: 403"
- Check that "Share on LinkedIn" product is added to your app
- Verify `w_member_social` permission is granted

### "Redirect URI mismatch"
- Ensure redirect URI in app settings is exactly: `http://localhost:8080/callback`

## 🎯 Next Steps

After successful setup:

1. **Automate with Cron**
   - Schedule the poster to run hourly
   - Add posts to queue throughout the day

2. **Integrate with AI**
   - Have your AI Employee generate posts
   - Save them to Posts_Queue/
   - Auto-post on schedule

3. **Build LinkedIn MCP Server**
   - Allow Claude to post directly via MCP
   - Real-time posting capability

## 📚 API Documentation

- [Share on LinkedIn API](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin)
- [OAuth 2.0 Authentication](https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication)

## ✅ Success Criteria

LinkedIn Auto-Poster is working when:
- ✅ Authentication completes successfully
- ✅ Posts appear on your LinkedIn profile
- ✅ Files move from queue to posted/
- ✅ Logs show successful posts

---

**Setup Complete!** 🎉

Your Personal AI Employee can now post to LinkedIn automatically.
