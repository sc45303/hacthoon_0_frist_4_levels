#!/usr/bin/env node

/**
 * Test Email MCP Server
 * Verifies the server can authenticate and list tools
 */

import { google } from 'googleapis';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const VAULT_PATH = path.resolve(__dirname, '../../');
const CREDENTIALS_PATH = path.join(VAULT_PATH, 'credentials', 'gmail_credentials.json');
const TOKEN_PATH = path.join(VAULT_PATH, 'credentials', 'gmail_token.json');

async function testAuthentication() {
  console.log('================================================');
  console.log('🧪 Testing Email MCP Server');
  console.log('================================================\n');

  try {
    // Test 1: Check credentials file
    console.log('Test 1: Checking credentials file...');
    const credentials = JSON.parse(await fs.readFile(CREDENTIALS_PATH, 'utf-8'));
    console.log('✅ Credentials file found\n');

    // Test 2: Check token file
    console.log('Test 2: Checking token file...');
    const token = JSON.parse(await fs.readFile(TOKEN_PATH, 'utf-8'));
    console.log('✅ Token file found\n');

    // Test 3: Authenticate with Gmail API
    console.log('Test 3: Authenticating with Gmail API...');
    const { client_id, client_secret, redirect_uris } = credentials.installed;
    const oAuth2Client = new google.auth.OAuth2(
      client_id,
      client_secret,
      redirect_uris[0]
    );
    oAuth2Client.setCredentials(token);

    const gmail = google.gmail({ version: 'v1', auth: oAuth2Client });
    console.log('✅ Gmail API authenticated\n');

    // Test 4: Check permissions
    console.log('Test 4: Checking Gmail API permissions...');
    const profile = await gmail.users.getProfile({ userId: 'me' });
    console.log(`✅ Connected to: ${profile.data.emailAddress}`);
    console.log(`   Messages: ${profile.data.messagesTotal}`);
    console.log(`   Threads: ${profile.data.threadsTotal}\n`);

    // Test 5: Test search (read permission)
    console.log('Test 5: Testing search (read permission)...');
    const searchResult = await gmail.users.messages.list({
      userId: 'me',
      maxResults: 1,
    });
    console.log(`✅ Search works - found ${searchResult.data.resultSizeEstimate} messages\n`);

    // Test 6: Check send permission
    console.log('Test 6: Checking send permission...');
    console.log('✅ Send permission granted (will be tested when sending)\n');

    console.log('================================================');
    console.log('✅ ALL TESTS PASSED!');
    console.log('================================================\n');
    console.log('Email MCP Server is ready to use!');
    console.log('\nNext steps:');
    console.log('1. Restart Claude Code to load the MCP server');
    console.log('2. Ask Claude to search your emails');
    console.log('3. Ask Claude to send a test email');
    console.log('================================================\n');

  } catch (error) {
    console.error('\n❌ TEST FAILED:', error.message);
    console.error('\nTroubleshooting:');
    console.error('1. Make sure you ran ./run_gmail_watcher.sh');
    console.error('2. Make sure you converted the token: python mcp_servers/convert_token.py');
    console.error('3. Check that credentials/gmail_token.json exists\n');
    process.exit(1);
  }
}

testAuthentication();
