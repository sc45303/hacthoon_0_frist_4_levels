# LinkedIn MCP Server

## Overview

The LinkedIn MCP Server exposes LinkedIn posting functionality as MCP tools that Claude can use directly during conversations.

## Features

- ✅ Post text updates to LinkedIn
- ✅ Post articles/URLs with preview cards
- ✅ Control post visibility (PUBLIC or CONNECTIONS)
- ✅ Uses same authentication as LinkedIn Auto-Poster

## Available Tools

### 1. post_to_linkedin

Post a text update to LinkedIn.

**Parameters:**
- `text` (required): The post content
- `visibility` (optional): "PUBLIC" or "CONNECTIONS" (default: PUBLIC)

**Example:**
```
Post to LinkedIn: "Just launched my Personal AI Employee! 🚀 #AI #Automation"
```

### 2. post_article_to_linkedin

Post an article or URL with a preview card.

**Parameters:**
- `text` (required): Commentary text
- `url` (required): Article URL
- `title` (optional): Custom title for preview
- `description` (optional): Custom description for preview
- `visibility` (optional): "PUBLIC" or "CONNECTIONS" (default: PUBLIC)

**Example:**
```
Post this article to LinkedIn: "Check out this amazing AI tool!"
URL: https://www.anthropic.com/claude
```

## Setup

### Prerequisites

1. **LinkedIn Authentication**
   - Run: `python authenticate_linkedin.py`
   - This creates `credentials/linkedin_token.json`

2. **MCP Configuration** (Already done ✅)
   - Added to `~/.config/claude-code/mcp_config.json`

### Installation

```bash
cd mcp_servers/linkedin_mcp
npm install
```

### Testing

```bash
node test.js
```

Expected output:
```
✅ Token file found
✅ Access token present
✅ Person URN present
✅ Authenticated as: Your Name
```

## Usage

After restarting Claude Code, you can use LinkedIn posting in conversations:

**Example 1: Simple text post**
```
Post to LinkedIn: "Excited to share my latest project! #innovation"
```

**Example 2: Article post**
```
Post this article to LinkedIn with the text "Great read on AI automation!"
URL: https://example.com/article
```

**Example 3: Connections-only post**
```
Post to LinkedIn (connections only): "Personal update for my network..."
```

## Rate Limits

- **Per Member**: 150 posts/day
- **Per Application**: 100,000 posts/day

## Troubleshooting

### "Token file not found"
- Run `python authenticate_linkedin.py` first
- Make sure authentication completed successfully

### "Failed to post: 401 Unauthorized"
- Token expired, re-authenticate
- Run `python authenticate_linkedin.py` again

### "Failed to post: 403 Forbidden"
- Check that "Share on LinkedIn" product is added to your app
- Verify `w_member_social` permission is granted

## Files

- `index.js` - MCP server implementation
- `package.json` - Dependencies
- `test.js` - Test script

## Integration with Auto-Poster

The MCP Server and Auto-Poster share the same authentication:
- **Auto-Poster**: Queue-based, scheduled posting
- **MCP Server**: Real-time posting via Claude

Both use `credentials/linkedin_token.json` for authentication.

## Next Steps

1. **Authenticate**: Run `python authenticate_linkedin.py`
2. **Restart Claude Code**: To load the MCP server
3. **Test**: Ask Claude to post something to LinkedIn
4. **Verify**: Check your LinkedIn profile

---

**LinkedIn MCP Server Ready!** 🎉
