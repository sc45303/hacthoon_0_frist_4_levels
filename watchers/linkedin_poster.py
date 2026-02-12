#!/usr/bin/env python3
"""
LinkedIn Auto-Poster
Automatically posts content from the Posts_Queue directory to LinkedIn
"""
import json
import os
import time
import requests
from datetime import datetime
from pathlib import Path
import re

# Paths
TOKEN_PATH = 'credentials/linkedin_token.json'
QUEUE_DIR = 'Posts_Queue'
POSTED_DIR = 'Posts_Queue/posted'
FAILED_DIR = 'Posts_Queue/failed'
LOG_FILE = 'Memory/linkedin_posts.log'

# LinkedIn API
API_URL = 'https://api.linkedin.com/v2/ugcPosts'
HEADERS_REQUIRED = {
    'X-Restli-Protocol-Version': '2.0.0',
    'Content-Type': 'application/json'
}

class LinkedInPoster:
    """LinkedIn posting automation"""

    def __init__(self):
        self.token_data = None
        self.access_token = None
        self.person_urn = None

    def load_token(self):
        """Load access token from file"""
        if not os.path.exists(TOKEN_PATH):
            print(f"❌ Token file not found: {TOKEN_PATH}")
            print(f"   Run: python authenticate_linkedin.py")
            return False

        with open(TOKEN_PATH, 'r') as f:
            self.token_data = json.load(f)

        self.access_token = self.token_data['access_token']
        self.person_urn = self.token_data['person_urn']

        print(f"✅ Token loaded for: {self.token_data.get('name', 'Unknown')}")
        return True

    def parse_post_file(self, filepath):
        """Parse a post file with frontmatter"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse frontmatter (YAML-style)
        metadata = {
            'type': 'text',
            'visibility': 'PUBLIC',
            'url': None,
            'url_title': None,
            'url_description': None
        }

        # Check for frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                content = parts[2].strip()

                # Parse frontmatter
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        metadata[key] = value

        return metadata, content

    def create_text_post(self, text, visibility='PUBLIC'):
        """Create a text-only post payload"""
        return {
            "author": self.person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }

    def create_article_post(self, text, url, title=None, description=None, visibility='PUBLIC'):
        """Create an article/URL post payload"""
        media = {
            "status": "READY",
            "originalUrl": url
        }

        if title:
            media["title"] = {"text": title}
        if description:
            media["description"] = {"text": description}

        return {
            "author": self.person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "ARTICLE",
                    "media": [media]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }

    def post_to_linkedin(self, payload):
        """Post content to LinkedIn"""
        headers = {
            **HEADERS_REQUIRED,
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 201:
            post_id = response.headers.get('X-RestLi-Id', 'unknown')
            return True, post_id
        else:
            error_msg = f"Status {response.status_code}: {response.text}"
            return False, error_msg

    def process_post(self, filepath):
        """Process a single post file"""
        filename = os.path.basename(filepath)
        print(f"\n📝 Processing: {filename}")

        try:
            # Parse post
            metadata, content = self.parse_post_file(filepath)

            if not content.strip():
                print(f"   ⚠️  Empty post, skipping")
                return False

            # Create payload based on type
            post_type = metadata.get('type', 'text').lower()
            visibility = metadata.get('visibility', 'PUBLIC').upper()

            if post_type == 'article' and metadata.get('url'):
                payload = self.create_article_post(
                    text=content,
                    url=metadata['url'],
                    title=metadata.get('url_title'),
                    description=metadata.get('url_description'),
                    visibility=visibility
                )
            else:
                payload = self.create_text_post(content, visibility)

            # Post to LinkedIn
            print(f"   📤 Posting to LinkedIn...")
            success, result = self.post_to_linkedin(payload)

            if success:
                print(f"   ✅ Posted successfully! ID: {result}")
                self.log_post(filename, 'success', result, content[:100])

                # Move to posted directory
                dest = os.path.join(POSTED_DIR, filename)
                os.rename(filepath, dest)
                print(f"   📁 Moved to: {POSTED_DIR}/")

                return True
            else:
                print(f"   ❌ Failed to post: {result}")
                self.log_post(filename, 'failed', result, content[:100])

                # Move to failed directory
                dest = os.path.join(FAILED_DIR, filename)
                os.rename(filepath, dest)
                print(f"   📁 Moved to: {FAILED_DIR}/")

                return False

        except Exception as e:
            print(f"   ❌ Error processing post: {e}")
            self.log_post(filename, 'error', str(e), '')
            return False

    def log_post(self, filename, status, result, preview):
        """Log post attempt"""
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {status.upper()}: {filename} | {result} | Preview: {preview}\n"

        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)

    def scan_queue(self):
        """Scan queue directory for posts"""
        posts = []

        for filename in os.listdir(QUEUE_DIR):
            filepath = os.path.join(QUEUE_DIR, filename)

            # Only process .md files in the root queue directory
            if os.path.isfile(filepath) and filename.endswith('.md'):
                posts.append(filepath)

        return sorted(posts)

    def run(self):
        """Main execution loop"""
        print("=" * 60)
        print("🚀 LinkedIn Auto-Poster")
        print("=" * 60)

        # Load token
        if not self.load_token():
            return

        # Scan for posts
        posts = self.scan_queue()

        if not posts:
            print(f"\n📭 No posts found in {QUEUE_DIR}/")
            print(f"   Create a .md file in {QUEUE_DIR}/ to post")
            return

        print(f"\n📬 Found {len(posts)} post(s) in queue")

        # Process each post
        success_count = 0
        for post_path in posts:
            if self.process_post(post_path):
                success_count += 1

            # Rate limiting: wait between posts
            if len(posts) > 1:
                print(f"   ⏳ Waiting 5 seconds before next post...")
                time.sleep(5)

        # Summary
        print("\n" + "=" * 60)
        print(f"✅ Posted {success_count}/{len(posts)} successfully")
        print("=" * 60)

def main():
    poster = LinkedInPoster()
    poster.run()

if __name__ == '__main__':
    main()
