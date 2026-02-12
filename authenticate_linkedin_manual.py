#!/usr/bin/env python3
"""
LinkedIn OAuth2 Authentication - Manual Code Entry
For WSL environments where localhost redirect doesn't work
"""
import json
import os
import requests

# Paths
CREDENTIALS_PATH = 'credentials/linkedin_credentials.json'
TOKEN_PATH = 'credentials/linkedin_token.json'

# OAuth2 URLs
AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
USERINFO_URL = 'https://api.linkedin.com/v2/userinfo'

def load_credentials():
    """Load LinkedIn app credentials"""
    with open(CREDENTIALS_PATH, 'r') as f:
        return json.load(f)

def exchange_code_for_token(creds, auth_code):
    """Exchange authorization code for access token"""
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'redirect_uri': creds['redirect_uri']
    }

    response = requests.post(TOKEN_URL, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   {response.text}")
        return None

def get_user_info(access_token):
    """Get user's Person URN"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(USERINFO_URL, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def save_token(token_data, user_info):
    """Save token and user info"""
    person_id = user_info.get('sub')
    person_urn = f"urn:li:person:{person_id}"

    token_info = {
        'access_token': token_data['access_token'],
        'expires_in': token_data['expires_in'],
        'person_urn': person_urn,
        'person_id': person_id,
        'name': user_info.get('name'),
        'email': user_info.get('email')
    }

    with open(TOKEN_PATH, 'w') as f:
        json.dump(token_info, f, indent=2)

    print(f"✅ Token saved to {TOKEN_PATH}")
    print(f"   Person URN: {person_urn}")

def main():
    print("=" * 60)
    print("🔐 LinkedIn OAuth2 Authentication (Manual)")
    print("=" * 60)
    print()

    # Load credentials
    creds = load_credentials()

    # Build authorization URL
    from urllib.parse import urlencode
    params = {
        'response_type': 'code',
        'client_id': creds['client_id'],
        'redirect_uri': creds['redirect_uri'],
        'scope': 'w_member_social profile openid email'
    }
    auth_url = f"{AUTH_URL}?{urlencode(params)}"

    print("📋 Step 1: Open this URL in your browser:")
    print()
    print(auth_url)
    print()
    print("📋 Step 2: Click 'Allow' to authorize")
    print()
    print("📋 Step 3: After redirect, copy the 'code' parameter from the URL")
    print("   The URL will look like:")
    print("   http://localhost:8080/callback?code=XXXXXXXX&state=...")
    print()
    print("   Copy everything after 'code=' and before '&' (or end of URL)")
    print()

    # Get authorization code from user
    auth_code = input("📝 Paste the authorization code here: ").strip()

    if not auth_code:
        print("❌ No code provided")
        return

    print()
    print("🔑 Exchanging code for access token...")

    # Exchange code for token
    token_data = exchange_code_for_token(creds, auth_code)
    if not token_data:
        return

    print("✅ Access token received")
    print()
    print("👤 Getting user information...")

    # Get user info
    user_info = get_user_info(token_data['access_token'])
    if not user_info:
        print("❌ Failed to get user info")
        return

    print(f"✅ Authenticated as: {user_info.get('name')}")
    print()

    # Save token
    save_token(token_data, user_info)

    print()
    print("=" * 60)
    print("✅ Authentication Complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
