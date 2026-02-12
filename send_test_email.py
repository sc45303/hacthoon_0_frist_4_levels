#!/usr/bin/env python3
"""
Send a test email using Gmail API
"""
import pickle
import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """Authenticate and return Gmail service"""
    creds = None
    token_path = 'credentials/gmail_token.pickle'

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("No valid credentials found")

    return build('gmail', 'v1', credentials=creds)

def send_email(to, subject, body):
    """Send an email"""
    service = get_gmail_service()

    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        message = service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()
        print(f"✅ Email sent successfully!")
        print(f"   Message ID: {message['id']}")
        return message
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        raise

if __name__ == '__main__':
    print("📧 Sending test email...")
    print()

    to = "sc3078745@gmail.com"
    subject = "AI Employee Success!"
    body = "My Personal AI Employee is working! Built in 4 hours with Gmail monitoring, email automation, and LinkedIn integration ready."

    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    print()

    send_email(to, subject, body)
