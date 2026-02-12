#!/usr/bin/env python3
"""
Convert Gmail token from pickle to JSON format
This allows the MCP server to use the same credentials
"""

import pickle
import json
from pathlib import Path

vault_path = Path(__file__).parent.parent
token_pickle = vault_path / 'credentials' / 'gmail_token.pickle'
token_json = vault_path / 'credentials' / 'gmail_token.json'

if not token_pickle.exists():
    print("❌ Error: gmail_token.pickle not found!")
    print("   Please run the Gmail watcher first to authenticate.")
    exit(1)

# Load pickle token
with open(token_pickle, 'rb') as f:
    creds = pickle.load(f)

# Convert to JSON format
token_data = {
    'access_token': creds.token,
    'refresh_token': creds.refresh_token,
    'token_uri': creds.token_uri,
    'client_id': creds.client_id,
    'client_secret': creds.client_secret,
    'scopes': creds.scopes,
    'expiry': creds.expiry.isoformat() if creds.expiry else None
}

# Save as JSON
with open(token_json, 'w') as f:
    json.dump(token_data, f, indent=2)

print(f"✅ Token converted successfully!")
print(f"   Saved to: {token_json}")
