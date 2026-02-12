#!/usr/bin/env python3
"""
LinkedIn OAuth2 Authentication - OpenID Connect version
Uses openid, profile, and w_member_social scopes
"""
import json
import sys
import requests

CREDENTIALS_PATH = 'credentials/linkedin_credentials.json'
TOKEN_PATH = 'credentials/linkedin_token.json'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
USERINFO_URL = 'https://api.linkedin.com/v2/userinfo'

def get_auth_url():
    """Generate authorization URL"""
    with open(CREDENTIALS_PATH, 'r') as f:
        creds = json.load(f)

    from urllib.parse import urlencode
    params = {
        'response_type': 'code',
        'client_id': creds['client_id'],
        'redirect_uri': creds['redirect_uri'],
        'scope': 'openid profile w_member_social'  # OpenID Connect scopes
    }
    return f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"

def exchange_code(auth_code):
    """Exchange authorization code for access token"""
    with open(CREDENTIALS_PATH, 'r') as f:
        creds = json.load(f)

    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'redirect_uri': creds['redirect_uri']
    }

    response = requests.post(TOKEN_URL, data=data)

    if response.status_code != 200:
        print(f"❌ Failed to get token: {response.status_code}")
        print(f"   {response.text}")
        return None

    return response.json()

def get_userinfo(access_token):
    """Get user info using OpenID Connect userinfo endpoint"""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(USERINFO_URL, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to get user info: {response.status_code}")
        print(f"   {response.text}")
        return None

    return response.json()

def save_token(token_data, userinfo):
    """Save token and user info"""
    # Extract person ID from sub claim
    person_id = userinfo.get('sub')

    # Build person URN
    person_urn = f"urn:li:person:{person_id}"

    token_info = {
        'access_token': token_data['access_token'],
        'expires_in': token_data['expires_in'],
        'person_urn': person_urn,
        'person_id': person_id,
        'name': userinfo.get('name', ''),
        'email': userinfo.get('email', '')
    }

    with open(TOKEN_PATH, 'w') as f:
        json.dump(token_info, f, indent=2)

    print(f"💾 Token saved to {TOKEN_PATH}")
    print(f"   Person URN: {person_urn}")
    print(f"   Name: {token_info['name']}")
    print(f"   Email: {token_info['email']}")

def main():
    print("=" * 60)
    print("🔐 LinkedIn OAuth2 Authentication (OpenID Connect)")
    print("=" * 60)
    print()

    if len(sys.argv) < 2:
        # Show authorization URL
        auth_url = get_auth_url()
        print("📋 Step 1: Open this URL in your browser:")
        print()
        print(auth_url)
        print()
        print("📋 Step 2: Click 'Allow' to authorize")
        print()
        print("📋 Step 3: Copy the 'code' from the redirect URL")
        print("   URL format: http://localhost:8080/callback?code=XXXXXXXX")
        print()
        print("📋 Step 4: Run this script with the code:")
        print(f"   venv/bin/python3 {sys.argv[0]} YOUR_CODE_HERE")
        print()
        return

    # Get code from command line
    auth_code = sys.argv[1]

    print("🔑 Exchanging code for access token...")
    token_data = exchange_code(auth_code)
    if not token_data:
        return

    print("✅ Access token received")
    print()

    print("👤 Getting user information...")
    userinfo = get_userinfo(token_data['access_token'])
    if not userinfo:
        return

    print(f"✅ User info retrieved")
    print()

    save_token(token_data, userinfo)

    print()
    print("=" * 60)
    print("✅ Authentication Complete!")
    print("=" * 60)
    print()
    print("You can now post to LinkedIn:")
    print("  venv/bin/python3 watchers/linkedin_poster.py")

if __name__ == '__main__':
    main()
