# LinkedIn API Implementation Notes

## API Requirements

### Authentication
- **Flow**: 3-legged OAuth 2.0 (Member Authorization)
- **Required Scope**: `w_member_social` (create posts on behalf of member)
- **Person URN**: Need to retrieve user's Person URN (format: `urn:li:person:XXXXXXXX`)

### API Endpoint
```
POST https://api.linkedin.com/v2/ugcPosts
```

**Required Header:**
```
X-Restli-Protocol-Version: 2.0.0
```

### Rate Limits
- **Per Member**: 150 requests/day
- **Per Application**: 100,000 requests/day

## Post Types

### 1. Text-Only Post
```json
{
    "author": "urn:li:person:8675309",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": "Your post text here"
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}
```

### 2. Article/URL Post
```json
{
    "author": "urn:li:person:8675309",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": "Check out this article!"
            },
            "shareMediaCategory": "ARTICLE",
            "media": [
                {
                    "status": "READY",
                    "description": {
                        "text": "Article description"
                    },
                    "originalUrl": "https://example.com/article",
                    "title": {
                        "text": "Article Title"
                    }
                }
            ]
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}
```

## OAuth2 Flow Steps

1. **Create LinkedIn App** at https://www.linkedin.com/developers/
2. **Configure OAuth Settings**:
   - Redirect URI: `http://localhost:8080/callback`
   - Request scope: `w_member_social`
3. **Authorization URL**:
   ```
   https://www.linkedin.com/oauth/v2/authorization?
     response_type=code&
     client_id={CLIENT_ID}&
     redirect_uri={REDIRECT_URI}&
     scope=w_member_social
   ```
4. **Exchange Code for Token**:
   ```
   POST https://www.linkedin.com/oauth/v2/accessToken
   Content-Type: application/x-www-form-urlencoded

   grant_type=authorization_code&
   code={AUTH_CODE}&
   client_id={CLIENT_ID}&
   client_secret={CLIENT_SECRET}&
   redirect_uri={REDIRECT_URI}
   ```
5. **Get Person URN**:
   ```
   GET https://api.linkedin.com/v2/userinfo
   Authorization: Bearer {ACCESS_TOKEN}
   ```

## Implementation Plan

### Files to Create
1. `watchers/linkedin_poster.py` - Main poster script
2. `Posts_Queue/` - Directory for queued posts
3. `credentials/linkedin_credentials.json` - OAuth credentials
4. `credentials/linkedin_token.json` - Access token storage

### Post Queue Format
Each post is a markdown file with frontmatter:
```markdown
---
type: text
visibility: PUBLIC
scheduled: false
---

Your post content here!

#hashtags #business #sales
```

## References
- [Share on LinkedIn API](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin)
- [OAuth 2.0 Authentication](https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication)
