#!/usr/bin/env node
/**
 * Test script for LinkedIn MCP Server
 * Verifies authentication and basic functionality
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const TOKEN_PATH = path.join(__dirname, '../../credentials/linkedin_token.json');

console.log('='.repeat(60));
console.log('🧪 Testing LinkedIn MCP Server');
console.log('='.repeat(60));

// Test 1: Check token file
console.log('\nTest 1: Checking token file...');
if (fs.existsSync(TOKEN_PATH)) {
  console.log('✅ Token file found');

  try {
    const tokenData = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));

    if (tokenData.access_token) {
      console.log('✅ Access token present');
    } else {
      console.log('❌ Access token missing');
    }

    if (tokenData.person_urn) {
      console.log('✅ Person URN present:', tokenData.person_urn);
    } else {
      console.log('❌ Person URN missing');
    }

    if (tokenData.name) {
      console.log('✅ Authenticated as:', tokenData.name);
    }

    if (tokenData.email) {
      console.log('✅ Email:', tokenData.email);
    }

  } catch (error) {
    console.log('❌ Error parsing token file:', error.message);
  }
} else {
  console.log('❌ Token file not found');
  console.log('   Run: python authenticate_linkedin.py');
}

// Test 2: Check dependencies
console.log('\nTest 2: Checking dependencies...');
try {
  await import('@modelcontextprotocol/sdk/server/index.js');
  console.log('✅ MCP SDK installed');
} catch (error) {
  console.log('❌ MCP SDK not installed');
  console.log('   Run: npm install');
}

try {
  await import('axios');
  console.log('✅ Axios installed');
} catch (error) {
  console.log('❌ Axios not installed');
  console.log('   Run: npm install');
}

console.log('\n' + '='.repeat(60));
console.log('✅ LinkedIn MCP Server Tests Complete');
console.log('='.repeat(60));

console.log('\nNext steps:');
console.log('1. Add to MCP config: ~/.config/claude-code/mcp_config.json');
console.log('2. Restart Claude Code');
console.log('3. Use tools: post_to_linkedin, post_article_to_linkedin');
