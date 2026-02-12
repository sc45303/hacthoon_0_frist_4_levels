# 🚀 LinkedIn Auto-Poster - Quick Start

## What's Been Built

✅ **Complete LinkedIn posting system ready to use!**

### Files Created:
- `authenticate_linkedin.py` - OAuth2 authentication
- `watchers/linkedin_poster.py` - Auto-posting script
- `run_linkedin_poster.sh` - Launcher script
- `Posts_Queue/` - Post queue directory
- `credentials/linkedin_credentials.json.template` - Credentials template

## Next Steps (15 minutes)

### 1. Create LinkedIn App (5 min)

Visit: https://www.linkedin.com/developers/apps

- Click "Create app"
- Name: "Personal AI Employee"
- Add redirect URL: `http://localhost:8080/callback`
- Request "Share on LinkedIn" product
- Copy Client ID and Client Secret

### 2. Save Credentials (1 min)

```bash
# Copy template
cp credentials/linkedin_credentials.json.template credentials/linkedin_credentials.json

# Edit and add your credentials
nano credentials/linkedin_credentials.json
```

### 3. Authenticate (2 min)

```bash
source venv/bin/activate
python authenticate_linkedin.py
```

Browser will open → Authorize → Done!

### 4. Test Post (2 min)

```bash
# Example post is already in queue
python watchers/linkedin_poster.py
```

Check your LinkedIn profile - post should appear!

## That's It!

Your AI Employee can now post to LinkedIn automatically.

See `LINKEDIN_POSTER_GUIDE.md` for full documentation.
