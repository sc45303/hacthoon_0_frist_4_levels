"""
Gmail Watcher - Monitor Gmail inbox and create tasks
Part of Silver Tier implementation
"""

import os
import time
import json
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# Gmail API scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.compose'
]

class GmailWatcher:
    def __init__(self, vault_path: str, check_interval: int = 120):
        """
        Initialize Gmail Watcher

        Args:
            vault_path: Path to AI_Employee_Vault
            check_interval: Seconds between checks (default: 120 = 2 minutes)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.processed_ids_file = self.vault_path / 'Memory' / 'processed_emails.json'
        self.processed_ids = self._load_processed_ids()
        self.service = None

    def _load_processed_ids(self):
        """Load list of already processed email IDs"""
        if self.processed_ids_file.exists():
            with open(self.processed_ids_file, 'r') as f:
                return set(json.load(f))
        return set()

    def _save_processed_ids(self):
        """Save processed email IDs to file"""
        with open(self.processed_ids_file, 'w') as f:
            json.dump(list(self.processed_ids), f)

    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        token_file = self.vault_path / 'credentials' / 'gmail_token.pickle'
        credentials_file = self.vault_path / 'credentials' / 'gmail_credentials.json'

        # Create credentials directory if it doesn't exist
        token_file.parent.mkdir(exist_ok=True)

        # Load existing token
        if token_file.exists():
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not credentials_file.exists():
                    print("❌ Error: gmail_credentials.json not found!")
                    print(f"   Please place it in: {credentials_file}")
                    print("   Get it from: https://console.cloud.google.com/")
                    return False

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_file), SCOPES)

                # Get authorization URL
                flow.redirect_uri = flow._OOB_REDIRECT_URI if hasattr(flow, '_OOB_REDIRECT_URI') else 'urn:ietf:wg:oauth:2.0:oob'
                auth_url, _ = flow.authorization_url(prompt='consent')

                # Save URL to file for easy copying
                url_file = self.vault_path / 'gmail_auth_url.txt'
                url_file.write_text(auth_url, encoding='utf-8')

                # Print URL clearly for manual copying
                print("\n" + "=" * 80)
                print("🔐 GMAIL AUTHENTICATION REQUIRED")
                print("=" * 80)
                print("\nThe authentication URL has been saved to: gmail_auth_url.txt")
                print("\nOption 1: Copy from file")
                print(f"  cat {url_file}")
                print("\nOption 2: Copy from below (full URL):")
                print("-" * 80)
                # Print URL without any formatting that might truncate it
                import sys
                sys.stdout.write(auth_url + "\n")
                sys.stdout.flush()
                print("-" * 80)
                print("\n" + "=" * 80)
                print("After signing in, you'll get a code. Paste it below.")
                print("=" * 80 + "\n")

                # Get authorization code from user
                code = input("Enter the authorization code: ").strip()
                flow.fetch_token(code=code)
                creds = flow.credentials

            # Save token for future use
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)
        print("✅ Gmail API authenticated successfully")
        return True

    def check_inbox(self):
        """Check Gmail inbox for new unread emails"""
        try:
            # Query for unread emails (testing mode - detects all unread)
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=10
            ).execute()

            messages = results.get('messages', [])

            if not messages:
                return 0

            new_count = 0
            for msg in messages:
                if msg['id'] not in self.processed_ids:
                    self.process_email(msg['id'])
                    self.processed_ids.add(msg['id'])
                    new_count += 1

            if new_count > 0:
                self._save_processed_ids()

            return new_count

        except Exception as e:
            print(f"❌ Error checking inbox: {e}")
            return 0

    def _get_email_body(self, payload):
        """Extract full email body from payload"""
        body = ""

        if 'parts' in payload:
            # Multipart email
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        import base64
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
                elif part['mimeType'] == 'text/html' and not body:
                    if 'data' in part['body']:
                        import base64
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                elif 'parts' in part:
                    # Nested parts
                    body = self._get_email_body(part)
                    if body:
                        break
        else:
            # Simple email
            if 'data' in payload['body']:
                import base64
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

        return body

    def process_email(self, msg_id: str):
        """Convert email to task file"""
        try:
            # Get full email message
            msg = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()

            # Extract headers
            headers = {h['name']: h['value']
                      for h in msg['payload']['headers']}

            from_email = headers.get('From', 'Unknown')
            subject = headers.get('Subject', 'No Subject')
            date = headers.get('Date', 'Unknown')

            # Get FULL email body (not just snippet)
            full_body = self._get_email_body(msg['payload'])

            # Fallback to snippet if body extraction fails
            if not full_body or len(full_body.strip()) == 0:
                full_body = msg.get('snippet', '')

            # Clean up body (remove excessive whitespace, limit length for readability)
            full_body = full_body.strip()
            if len(full_body) > 5000:
                full_body = full_body[:5000] + "\n\n[Email truncated - full content available in Gmail]"

            # Determine priority based on keywords
            priority = 'high'
            urgent_keywords = ['urgent', 'asap', 'important', 'critical']
            if any(keyword in subject.lower() for keyword in urgent_keywords):
                priority = 'urgent'

            # Create task file with FULL email body
            task_content = f"""---
type: email
from: {from_email}
subject: {subject}
received: {date}
priority: {priority}
gmail_id: {msg_id}
detected: {datetime.now().isoformat()}
---

# Email Task: {subject}

**From:** {from_email}
**Date:** {date}
**Priority:** {priority}

## Email Content (Full)

{full_body}

## Suggested Actions
- [ ] Read full email
- [ ] Draft reply
- [ ] Forward if needed
- [ ] Archive after handling

## Notes
This task was automatically created by Gmail Watcher.
"""

            # Save task file
            safe_subject = "".join(c for c in subject if c.isalnum() or c in (' ', '-', '_'))[:50]
            task_file = self.needs_action / f'EMAIL_{safe_subject}_{msg_id[:8]}.md'
            task_file.write_text(task_content, encoding='utf-8')

            print(f"📧 Created task from email: {subject}")
            print(f"   From: {from_email}")
            print(f"   Priority: {priority}")

        except Exception as e:
            print(f"❌ Error processing email {msg_id}: {e}")

    def run(self):
        """Main loop - run continuously"""
        print("=" * 60)
        print("📧 Gmail Watcher Starting")
        print("=" * 60)
        print(f"Vault: {self.vault_path}")
        print(f"Check interval: {self.check_interval} seconds")
        print(f"Monitoring: All unread emails (testing mode)")
        print("=" * 60)

        # Authenticate
        if not self.authenticate():
            return

        print("\n👀 Watching Gmail inbox...")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                new_emails = self.check_inbox()

                if new_emails > 0:
                    print(f"✅ Processed {new_emails} new email(s)")

                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            print("\n\n⏹️  Gmail Watcher stopped by user")
        except Exception as e:
            print(f"\n❌ Fatal error: {e}")


if __name__ == "__main__":
    # Get vault path from environment or use default
    vault_path = os.getenv('AI_EMPLOYEE_VAULT', '/home/sk/projects/hacahthoon-0/personal-ai-employee/AI_Employee_Vault')

    # Create watcher
    watcher = GmailWatcher(vault_path, check_interval=120)

    # Run
    watcher.run()
