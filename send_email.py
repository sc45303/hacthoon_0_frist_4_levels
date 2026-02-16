#!/usr/bin/env python3
"""
Simple email sender using Gmail API
Usage: python send_email.py "recipient@email.com" "Subject" "Body text"
"""

import sys
import json
import base64
from pathlib import Path
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def send_email(to, subject, body):
    """Send an email via Gmail API"""

    # Load credentials
    creds_path = Path(__file__).parent / 'credentials' / 'gmail_token.json'

    if not creds_path.exists():
        print("❌ Error: Gmail token not found. Please run gmail_watcher.py first to authenticate.")
        return False

    # Load token
    with open(creds_path, 'r') as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data.get('access_token'),
        refresh_token=token_data.get('refresh_token'),
        token_uri=token_data.get('token_uri', 'https://oauth2.googleapis.com/token'),
        client_id=token_data.get('client_id'),
        client_secret=token_data.get('client_secret'),
        scopes=token_data.get('scopes', ['https://www.googleapis.com/auth/gmail.send'])
    )

    # Build Gmail service
    service = build('gmail', 'v1', credentials=creds)

    # Create message
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject

    # Encode message
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    # Send email
    try:
        result = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        print(f"✅ Email sent successfully!")
        print(f"   To: {to}")
        print(f"   Subject: {subject}")
        print(f"   Message ID: {result['id']}")
        return True

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python send_email.py 'recipient@email.com' 'Subject' 'Body text'")
        sys.exit(1)

    to = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]

    success = send_email(to, subject, body)
    sys.exit(0 if success else 1)
