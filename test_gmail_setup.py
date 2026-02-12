"""
Test Gmail Watcher Setup
Verifies all components are ready
"""

import sys
from pathlib import Path

def test_setup():
    """Test Gmail watcher setup"""
    print("=" * 60)
    print("🧪 Testing Gmail Watcher Setup")
    print("=" * 60)
    print()

    vault_path = Path(__file__).parent
    all_ok = True

    # Test 1: Check credentials directory
    print("1. Checking credentials directory...")
    creds_dir = vault_path / 'credentials'
    if creds_dir.exists():
        print("   ✅ credentials/ directory exists")
    else:
        print("   ❌ credentials/ directory missing")
        all_ok = False

    # Test 2: Check credentials file
    print("\n2. Checking gmail_credentials.json...")
    creds_file = creds_dir / 'gmail_credentials.json'
    if creds_file.exists():
        print("   ✅ gmail_credentials.json found")
    else:
        print("   ❌ gmail_credentials.json not found")
        print("      Place it in: credentials/gmail_credentials.json")
        all_ok = False

    # Test 3: Check dependencies
    print("\n3. Checking dependencies...")
    try:
        import google.auth
        print("   ✅ google-auth installed")
    except ImportError:
        print("   ❌ google-auth not installed")
        print("      Run: pip install google-auth google-auth-oauthlib google-api-python-client")
        all_ok = False

    try:
        import google_auth_oauthlib
        print("   ✅ google-auth-oauthlib installed")
    except ImportError:
        print("   ❌ google-auth-oauthlib not installed")
        all_ok = False

    try:
        import googleapiclient
        print("   ✅ google-api-python-client installed")
    except ImportError:
        print("   ❌ google-api-python-client not installed")
        all_ok = False

    # Test 4: Check watcher script
    print("\n4. Checking watcher script...")
    watcher_file = vault_path / 'watchers' / 'gmail_watcher.py'
    if watcher_file.exists():
        print("   ✅ gmail_watcher.py exists")
    else:
        print("   ❌ gmail_watcher.py not found")
        all_ok = False

    # Test 5: Check Needs_Action directory
    print("\n5. Checking Needs_Action directory...")
    needs_action = vault_path / 'Needs_Action'
    if needs_action.exists():
        print("   ✅ Needs_Action/ directory exists")
    else:
        print("   ❌ Needs_Action/ directory missing")
        all_ok = False

    # Test 6: Check Memory directory
    print("\n6. Checking Memory directory...")
    memory_dir = vault_path / 'Memory'
    if memory_dir.exists():
        print("   ✅ Memory/ directory exists")
    else:
        print("   ❌ Memory/ directory missing")
        all_ok = False

    # Summary
    print("\n" + "=" * 60)
    if all_ok:
        print("✅ ALL TESTS PASSED")
        print("\n🚀 Ready to run Gmail Watcher!")
        print("\nNext steps:")
        print("1. Run: python watchers/gmail_watcher.py")
        print("2. Authenticate with Google (first time only)")
        print("3. Send yourself a test email")
        print("4. Check Needs_Action/ for task file")
        print("\nOr use quick start:")
        print("   ./start_gmail_watcher.sh")
    else:
        print("❌ SETUP INCOMPLETE")
        print("\nPlease fix the issues above.")
        print("See: GMAIL_WATCHER_SETUP.md for detailed instructions")
    print("=" * 60)

    return all_ok

if __name__ == "__main__":
    success = test_setup()
    sys.exit(0 if success else 1)
