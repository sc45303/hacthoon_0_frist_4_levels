#!/usr/bin/env python3
"""
LinkedIn OAuth2 Authentication - Simplified for Share on LinkedIn product only
Works with just w_member_social and r_liteprofile scopes
"""
import json
import sys
import requests

CREDENTIALS_PATH = 'credentials/linkedin_credentials.json'
TOKEN_PATH = 'credentials/linkedin_token.json'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
PROFILE_URL = 'https://api.linkedin.com/v2/me'

def get_auth_url():
    """Generate authorization URL"""
    with open(CREDENTIALS_PATH, 'r') as f:
        creds = json.load(f)

    from urllib.parse import urlencode
    params = {
        'response_type': 'code',
        'client_id': creds['client_id'],
        'redirect_uri': creds['redirect_uri'],
        'scope': 'r_liteprofile w_member_social'  # Only these scopes
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

def get_profile(access_token):
    """Get user profile using v2 API"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    response = requests.get(PROFILE_URL, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to get profile: {response.status_code}")
        print(f"   {response.text}")
        return None

    return response.json()

def save_token(token_data, profile_data):
    """Save token and profile info"""
    # Extract person ID from profile
    person_id = profile_data.get('id')

    # Build person URN
    person_urn = f"urn:li:person:{person_id}"

    token_info = {
        'access_token': token_data['access_token'],
        'expires_in': token_data['expires_in'],
        'person_urn': person_urn,
        'person_id': person_id,
        'name': f"{profile_data.get('localizedFirstName', '')} {profile_data.get('localizedLastName', '')}".strip()
    }

    with open(TOKEN_PATH, 'w') as f:
        json.dump(token_info, f, indent=2)

    print(f"💾 Token saved to {TOKEN_PATH}")
    print(f"   Person URN: {person_urn}")
    print(f"   Name: {token_info['name']}")

def main():
    print("=" * 60)
    print("🔐 LinkedIn OAuth2 Authentication (Simplified)")
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

    print("👤 Getting profile information...")
    profile_data = get_profile(token_data['access_token'])
    if not profile_data:
        return

    print(f"✅ Profile retrieved")
    print()

    save_token(token_data, profile_data)

    print()
    print("=" * 60)
    print("✅ Authentication Complete!")
    print("=" * 60)
    print()
    print("You can now post to LinkedIn:")
    print("  venv/bin/python3 watchers/linkedin_poster.py")

if __name__ == '__main__':
    main()
