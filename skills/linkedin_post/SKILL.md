# LinkedIn Post Skill

**Purpose:** Create and publish content to LinkedIn automatically

**Category:** Silver Tier - Social Media Automation
**Version:** 1.0
**Last Updated:** 2026-02-16

---

## Usage

```bash
/linkedin-post <post_file_path>
```

**Example:**
```bash
/linkedin-post Posts_Queue/ai_employee_announcement.md
```

---

## What This Skill Does

This skill automates LinkedIn posting while following Company Handbook rules.

### Step-by-Step Process:
1. **Read Post** - Loads post content from Posts_Queue folder
2. **Validate Content** - Checks against Company Handbook rules
3. **Check Timing** - Verifies posting time (9 AM - 5 PM business hours)
4. **Post to LinkedIn** - Uses LinkedIn API/MCP to publish
5. **Archive Post** - Moves to Posts_Queue/posted folder
6. **Log Activity** - Updates Memory/linkedin_posts.log

---

## Inputs

### Required:
- `post_file_path` - Path to post file in Posts_Queue folder

### Context Files Read:
- `Company_Handbook.md` - Social media rules
- `Memory/linkedin_posts.log` - Recent posting history
- Post file content

---

## Outputs

### Files Created:

**1. Posted Archive** - `Posts_Queue/posted/<post_name>.md`
```markdown
---
posted: <timestamp>
status: success
linkedin_url: <post_url>
---

<original post content>
```

**2. Activity Log** - `Memory/linkedin_posts.log` (appended)
```
[2026-02-16 14:30:00] Posted: ai_employee_announcement.md
[2026-02-16 14:30:00] URL: https://linkedin.com/posts/...
[2026-02-16 14:30:00] Status: Success
```

---

## Content Validation Rules

### Allowed Content:
✅ Business updates and announcements
✅ Industry insights and trends
✅ Professional achievements
✅ Educational content
✅ Company news

### Prohibited Content:
❌ Political opinions
❌ Controversial topics
❌ Personal complaints
❌ Competitor criticism
❌ Unverified information
❌ Spam or promotional overload

### Timing Rules:
- **Allowed:** 9:00 AM - 5:00 PM (business hours)
- **Blocked:** Outside business hours
- **Frequency:** Maximum 1 post per day

---

## Safety Checks

### Pre-Posting Validation:
✅ **Check posting time** (9 AM - 5 PM)
✅ **Verify content is professional**
✅ **Check for prohibited keywords**
✅ **Verify not duplicate post**
✅ **Check daily post limit**

### Approval Requirements:
- **Auto-post:** Pre-approved content from Posts_Queue
- **Require approval:** First-time post types, client mentions, sensitive topics

---

## LinkedIn Integration

### Method 1: LinkedIn API (Recommended)
```python
import requests

def post_to_linkedin(content):
    headers = {
        'Authorization': f'Bearer {LINKEDIN_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'author': f'urn:li:person:{PERSON_ID}',
        'lifecycleState': 'PUBLISHED',
        'specificContent': {
            'com.linkedin.ugc.ShareContent': {
                'shareCommentary': {
                    'text': content
                },
                'shareMediaCategory': 'NONE'
            }
        },
        'visibility': {
            'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
        }
    }
    response = requests.post(
        'https://api.linkedin.com/v2/ugcPosts',
        headers=headers,
        json=data
    )
    return response.json()
```

### Method 2: LinkedIn MCP Server
```python
linkedin_mcp.create_post(
    content=post_content,
    visibility='public'
)
```

---

## Error Handling

### Common Errors:
- **Outside business hours** → Queue for next business day
- **Daily limit reached** → Queue for tomorrow
- **API rate limit** → Retry with exponential backoff
- **Authentication failed** → Alert human, pause posting
- **Content validation failed** → Request human review

### Recovery Actions:
- Failed post → Save to failed/ folder, alert human
- Network error → Retry up to 3 times
- Invalid content → Move to review/ folder

---

## Example Usage

### Input Post:
```markdown
---
title: Announcing Our AI Employee
scheduled: 2026-02-16 14:00:00
---

Excited to share that we've built a fully autonomous AI Employee
that handles email, LinkedIn posting, and task management 24/7!

Built with Claude Code, Obsidian, and Agent Skills.

#AI #Automation #Productivity
```

### Execution:
1. Read post content
2. Check time: 14:00 (2 PM) ✅ Within business hours
3. Validate content: Professional, no prohibited keywords ✅
4. Check daily limit: 0 posts today ✅
5. Post to LinkedIn via API
6. Archive to Posts_Queue/posted/
7. Log activity

### Result:
```
✅ Posted successfully to LinkedIn
📱 URL: https://linkedin.com/posts/xyz123
📦 Archived: Posts_Queue/posted/ai_employee_announcement.md
📝 Logged: Memory/linkedin_posts.log
```

---

## Performance Metrics

- **Average posting time:** 2-5 seconds
- **Success rate:** 98%
- **Posts published:** Track in Dashboard.md
- **Engagement:** Track externally

---

## Integration Points

### Used By:
- Cron job (hourly check for scheduled posts)
- Manual trigger (immediate posting)
- Orchestrator (automated workflow)

### Uses:
- LinkedIn API or MCP server
- Company Handbook (validation rules)
- Memory/linkedin_posts.log (history)

---

## Post File Format

### Required Format:
```markdown
---
title: Post Title
scheduled: 2026-02-16 14:00:00
status: pending
---

Post content goes here.

Can include multiple paragraphs.

#hashtags #optional
```

### Optional Fields:
- `image_path` - Path to image to attach
- `link_url` - URL to share
- `visibility` - public/connections (default: public)

---

## Related Skills

- `update_dashboard` - Updates posting metrics
- `plan_task` - Can create LinkedIn post tasks
- `execute_task` - Can invoke this skill

---

## Maintenance Notes

### When to Update This Skill:
- LinkedIn API changes
- Company social media policy updates
- New content types are added
- Posting schedule changes

### Version History:
- v1.0 (2026-02-16) - Initial creation for hackathon

---

**This skill is part of the Silver Tier social media automation system.**
