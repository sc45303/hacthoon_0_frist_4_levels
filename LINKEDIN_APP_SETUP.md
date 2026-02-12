# LinkedIn App Setup Guide

## Step 1: Create LinkedIn App

1. **Go to LinkedIn Developer Portal**
   - Open: https://www.linkedin.com/developers/apps
   - Sign in with your LinkedIn account

2. **Create New App**
   - Click "Create app" button
   - Fill in the required information:
     - **App name**: "Personal AI Employee" (or your preferred name)
     - **LinkedIn Page**: Select your company page (or create one if needed)
     - **App logo**: Upload a logo (optional but recommended)
     - **Legal agreement**: Check the box to agree to terms

3. **Note Your Credentials**
   After creating the app, you'll see:
   - **Client ID**: Copy this (looks like: 86xxxxxxxxxxxxxx)
   - **Client Secret**: Click "Show" and copy this
   - **App ID**: Note this for reference

## Step 2: Configure OAuth Settings

1. **Go to Auth Tab**
   - In your app dashboard, click the "Auth" tab

2. **Add Redirect URLs**
   - Click "Add redirect URL"
   - Add: `http://localhost:8080/callback`
   - Click "Update"

## Step 3: Request API Access

1. **Go to Products Tab**
   - Click the "Products" tab in your app dashboard

2. **Add "Share on LinkedIn" Product**
   - Find "Share on LinkedIn" in the list
   - Click "Request access" or "Add to app"
   - This grants you the `w_member_social` permission

3. **Wait for Approval** (if required)
   - Some products require LinkedIn review
   - "Share on LinkedIn" is usually instant for personal use

## Step 4: Verify Permissions

1. **Go to Settings Tab**
   - Check that you have these permissions:
     - ✅ `r_liteprofile` (read basic profile)
     - ✅ `w_member_social` (post on behalf of member)

## Step 5: Save Credentials

Create a file at: `credentials/linkedin_credentials.json`

```json
{
  "client_id": "YOUR_CLIENT_ID_HERE",
  "client_secret": "YOUR_CLIENT_SECRET_HERE",
  "redirect_uri": "http://localhost:8080/callback"
}
```

**IMPORTANT**: Replace `YOUR_CLIENT_ID_HERE` and `YOUR_CLIENT_SECRET_HERE` with your actual credentials.

## Troubleshooting

### "I don't have a LinkedIn Page"
- You need a LinkedIn Page to create an app
- Create one at: https://www.linkedin.com/company/setup/new/
- You can create a personal brand page

### "Share on LinkedIn product not available"
- Make sure your LinkedIn account is complete
- Verify your email address
- Try using a different LinkedIn account

### "Redirect URI mismatch error"
- Make sure the redirect URI in your app settings exactly matches: `http://localhost:8080/callback`
- No trailing slash
- Use `http` not `https` for localhost

## Next Steps

After completing this setup:
1. Save your credentials to `credentials/linkedin_credentials.json`
2. Run the authentication script to get your access token
3. Test posting to LinkedIn

---

**Ready to proceed?** Once you have your Client ID and Client Secret, let me know and we'll continue with the authentication flow.
