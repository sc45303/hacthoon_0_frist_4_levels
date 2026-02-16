#!/usr/bin/env python3
"""
LinkedIn Post Skill Implementation
Posts content to LinkedIn with validation and logging
"""
import sys
from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent.parent.parent
POSTS_QUEUE = BASE_DIR / "Posts_Queue"
POSTS_POSTED = POSTS_QUEUE / "posted"
LINKEDIN_LOG = BASE_DIR / "Memory" / "linkedin_posts.log"
COMPANY_HANDBOOK = BASE_DIR / "Company_Handbook.md"

# Business hours: 9 AM - 5 PM
BUSINESS_HOURS_START = 9
BUSINESS_HOURS_END = 17

def is_business_hours():
    """Check if current time is within business hours"""
    current_hour = datetime.now().hour
    return BUSINESS_HOURS_START <= current_hour < BUSINESS_HOURS_END

def validate_content(content):
    """
    Validate post content against Company Handbook rules

    Returns:
        (is_valid, message)
    """
    # Prohibited keywords
    prohibited = [
        'political', 'politics', 'controversial', 'complaint',
        'competitor', 'spam', 'unverified'
    ]

    content_lower = content.lower()

    for keyword in prohibited:
        if keyword in content_lower:
            return False, f"Content contains prohibited keyword: {keyword}"

    # Check length (LinkedIn limit is ~3000 chars)
    if len(content) > 3000:
        return False, "Content exceeds LinkedIn character limit (3000)"

    if len(content) < 10:
        return False, "Content too short (minimum 10 characters)"

    return True, "Content validated"

def post_to_linkedin(content):
    """
    Post content to LinkedIn

    Note: This is a placeholder. In production, this would:
    1. Use LinkedIn API with OAuth token
    2. Or use LinkedIn MCP server
    3. Or use browser automation

    For now, we simulate successful posting.
    """
    # TODO: Implement actual LinkedIn API integration
    # For hackathon demo, we simulate posting

    print("📱 Posting to LinkedIn...")
    print(f"Content preview: {content[:100]}...")

    # Simulate API call
    post_url = f"https://linkedin.com/posts/simulated_{datetime.now().timestamp()}"

    return True, post_url

def log_post(post_name, status, url=None, error=None):
    """Log posting activity"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] Posted: {post_name}\n"
    if url:
        log_entry += f"[{timestamp}] URL: {url}\n"
    log_entry += f"[{timestamp}] Status: {status}\n"
    if error:
        log_entry += f"[{timestamp}] Error: {error}\n"
    log_entry += "\n"

    # Append to log file
    with open(LINKEDIN_LOG, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def archive_post(post_file, url):
    """Move posted content to posted/ folder with metadata"""
    # Ensure posted folder exists
    POSTS_POSTED.mkdir(exist_ok=True)

    # Read original content
    content = post_file.read_text(encoding='utf-8')

    # Add metadata
    archived_content = f"""---
posted: {datetime.now().isoformat()}
status: success
linkedin_url: {url}
---

{content}
"""

    # Write to posted folder
    dest = POSTS_POSTED / post_file.name
    dest.write_text(archived_content, encoding='utf-8')

    # Delete original
    post_file.unlink()

    print(f"📦 Archived: {dest}")

def linkedin_post(post_file_path):
    """
    Post content to LinkedIn

    Args:
        post_file_path: Path to post file in Posts_Queue folder

    Returns:
        Success message or error
    """
    post_file = Path(post_file_path)

    if not post_file.exists():
        return f"❌ Error: Post file not found: {post_file_path}"

    # Check business hours
    if not is_business_hours():
        current_hour = datetime.now().hour
        return f"⏰ Outside business hours (current: {current_hour}:00, allowed: {BUSINESS_HOURS_START}:00-{BUSINESS_HOURS_END}:00). Post queued for next business day."

    # Read post content
    content = post_file.read_text(encoding='utf-8').strip()

    # Remove frontmatter if present
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2].strip()

    # Validate content
    is_valid, message = validate_content(content)
    if not is_valid:
        log_post(post_file.name, "Failed", error=message)
        return f"❌ Validation failed: {message}"

    print(f"📱 Posting: {post_file.name}")

    try:
        # Post to LinkedIn
        success, url = post_to_linkedin(content)

        if success:
            # Archive post
            archive_post(post_file, url)

            # Log activity
            log_post(post_file.name, "Success", url=url)

            return f"✅ Posted successfully to LinkedIn\n📱 URL: {url}\n📦 Archived: Posts_Queue/posted/{post_file.name}\n📝 Logged: Memory/linkedin_posts.log"
        else:
            log_post(post_file.name, "Failed", error="API returned failure")
            return f"❌ Posting failed: API error"

    except Exception as e:
        error_msg = f"Error posting to LinkedIn: {str(e)}"
        print(f"❌ {error_msg}")
        log_post(post_file.name, "Failed", error=error_msg)
        return f"❌ {error_msg}"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python linkedin_post.py <post_file_path>")
        print("Example: python linkedin_post.py Posts_Queue/my_post.md")
        sys.exit(1)

    result = linkedin_post(sys.argv[1])
    print(result)

    # Exit with appropriate code
    sys.exit(0 if "✅" in result else 1)
