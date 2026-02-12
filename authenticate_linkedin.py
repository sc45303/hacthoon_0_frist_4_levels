#!/usr/bin/env python3
"""
LinkedIn OAuth2 Authentication Script
Handles the OAuth2 flow to get access token for LinkedIn API
"""
import json
import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urlencode
import requests

# Paths
CREDENTIALS_PATH = 'credentials/linkedin_credentials.json'
TOKEN_PATH = 'credentials/linkedin_token.json'

# OAuth2 URLs
AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
USERINFO_URL = 'https://api.linkedin.com/v2/userinfo'

class CallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth2 callback"""

    def do_GET(self):
        """Handle GET request from OAuth2 redirect"""
        # Parse the authorization code from URL
        query = urlparse(self.path).query
        params = parse_qs(query)

        if 'code' in params:
            self.server.auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <body>
                    <h1>Authentication Successful!</h1>
                    <p>You can close this window and return to the terminal.</p>
                </body>
                </html>
            """)
        elif 'error' in params:
            self.server.auth_code = None
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error = params['error'][0]
            self.wfile.write(f"""
                <html>
                <body>
                    <h1>Authentication Failed</h1>
                    <p>Error: {error}</p>
                </body>
                </html>
            """.encode())

    def log_message(self, format, *args):
        """Suppress log messages"""
        pass

def load_credentials():
    """Load LinkedIn app credentials"""
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"❌ Credentials file not found: {CREDENTIALS_PATH}")
        print(f"   Please create it using the template and add your Client ID and Secret")
        return None

    with open(CREDENTIALS_PATH, 'r') as f:
        creds = json.load(f)

    if creds['client_id'] == 'YOUR_CLIENT_ID_HERE':
        print(f"❌ Please update {CREDENTIALS_PATH} with your actual credentials")
        return None

    return creds

def get_authorization_code(creds):
    """Step 1: Get authorization code via browser"""
    print("\n🔐 Step 1: Getting authorization code...")

    # Build authorization URL
    params = {
        'response_type': 'code',
        'client_id': creds['client_id'],
        'redirect_uri': creds['redirect_uri'],
        'scope': 'w_member_social profile openid email'
    }
    auth_url = f"{AUTH_URL}?{urlencode(params)}"

    print(f"\n📱 Opening browser for LinkedIn authorization...")
    print(f"   If browser doesn't open, visit this URL:")
    print(f"   {auth_url}\n")

    # Start local server to receive callback
    server = HTTPServer(('localhost', 8080), CallbackHandler)
    server.auth_code = None

    # Open browser
    webbrowser.open(auth_url)

    # Wait for callback
    print("⏳ Waiting for authorization...")
    server.handle_request()

    if server.auth_code:
        print("✅ Authorization code received")
        return server.auth_code
    else:
        print("❌ Authorization failed")
        return None

def exchange_code_for_token(creds, auth_code):
    """Step 2: Exchange authorization code for access token"""
    print("\n🔑 Step 2: Exchanging code for access token...")

    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'redirect_uri': creds['redirect_uri']
    }

    response = requests.post(TOKEN_URL, data=data)

    if response.status_code == 200:
        token_data = response.json()
        print("✅ Access token received")
        return token_data
    else:
        print(f"❌ Failed to get access token: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def get_user_info(access_token):
    """Step 3: Get user's Person URN"""
    print("\n👤 Step 3: Getting user information...")

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(USERINFO_URL, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        print(f"✅ User info retrieved")
        print(f"   Name: {user_info.get('name', 'N/A')}")
        print(f"   Email: {user_info.get('email', 'N/A')}")
        print(f"   Sub (Person ID): {user_info.get('sub', 'N/A')}")
        return user_info
    else:
        print(f"❌ Failed to get user info: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def save_token(token_data, user_info):
    """Save token and user info to file"""
    print("\n💾 Step 4: Saving token...")

    # Create Person URN from sub
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
    """Main authentication flow"""
    print("=" * 60)
    print("🔐 LinkedIn OAuth2 Authentication")
    print("=" * 60)

    # Load credentials
    creds = load_credentials()
    if not creds:
        return

    # Step 1: Get authorization code
    auth_code = get_authorization_code(creds)
    if not auth_code:
        return

    # Step 2: Exchange for access token
    token_data = exchange_code_for_token(creds, auth_code)
    if not token_data:
        return

    # Step 3: Get user info
    user_info = get_user_info(token_data['access_token'])
    if not user_info:
        return

    # Step 4: Save token
    save_token(token_data, user_info)

    print("\n" + "=" * 60)
    print("✅ Authentication Complete!")
    print("=" * 60)
    print("\nYou can now use the LinkedIn poster to post content.")
    print("Run: python watchers/linkedin_poster.py")

if __name__ == '__main__':
    main()
