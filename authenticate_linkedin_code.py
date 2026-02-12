#!/usr/bin/env python3
"""
LinkedIn OAuth2 Authentication - Code as Argument
Usage: python authenticate_linkedin_code.py <authorization_code>
"""
import json
import sys
import requests

CREDENTIALS_PATH = 'credentials/linkedin_credentials.json'
TOKEN_PATH = 'credentials/linkedin_token.json'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
USERINFO_URL = 'https://api.linkedin.com/v2/userinfo'

def main():
    if len(sys.argv) < 2:
        print("Usage: python authenticate_linkedin_code.py <authorization_code>")
        sys.exit(1)

    auth_code = sys.argv[1]

    print("=" * 60)
    print("🔐 LinkedIn OAuth2 Authentication")
    print("=" * 60)
    print()

    # Load credentials
    with open(CREDENTIALS_PATH, 'r') as f:
        creds = json.load(f)

    print("🔑 Exchanging code for access token...")

    # Exchange code for token
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
        sys.exit(1)

    token_data = response.json()
    print("✅ Access token received")
    print()

    # Get user info
    print("👤 Getting user information...")
    headers = {'Authorization': f'Bearer {token_data["access_token"]}'}
    response = requests.get(USERINFO_URL, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to get user info: {response.status_code}")
        sys.exit(1)

    user_info = response.json()
    print(f"✅ Authenticated as: {user_info.get('name')}")
    print(f"   Email: {user_info.get('email')}")
    print()

    # Save token
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

    print(f"💾 Token saved to {TOKEN_PATH}")
    print(f"   Person URN: {person_urn}")
    print()
    print("=" * 60)
    print("✅ Authentication Complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
