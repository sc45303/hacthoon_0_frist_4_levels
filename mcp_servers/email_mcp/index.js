#!/usr/bin/env node

/**
 * Email MCP Server
 * Provides Gmail operations via Model Context Protocol
 *
 * Tools:
 * - send_email: Send an email via Gmail
 * - draft_reply: Create a draft reply to an email
 * - search_emails: Search Gmail inbox
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { google } from 'googleapis';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Path to credentials (same as Gmail watcher)
const VAULT_PATH = path.resolve(__dirname, '../../');
const CREDENTIALS_PATH = path.join(VAULT_PATH, 'credentials', 'gmail_credentials.json');
const TOKEN_PATH = path.join(VAULT_PATH, 'credentials', 'gmail_token.json');

class EmailMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'email-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.gmail = null;
    this.setupHandlers();
  }

  async authenticate() {
    try {
      // Load credentials
      const credentials = JSON.parse(await fs.readFile(CREDENTIALS_PATH, 'utf-8'));
      const { client_id, client_secret, redirect_uris } = credentials.installed;

      const oAuth2Client = new google.auth.OAuth2(
        client_id,
        client_secret,
        redirect_uris[0]
      );

      // Load token
      const token = JSON.parse(await fs.readFile(TOKEN_PATH, 'utf-8'));
      oAuth2Client.setCredentials(token);

      this.gmail = google.gmail({ version: 'v1', auth: oAuth2Client });

      return true;
    } catch (error) {
      console.error('Authentication failed:', error.message);
      return false;
    }
  }

  setupHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'send_email',
          description: 'Send an email via Gmail',
          inputSchema: {
            type: 'object',
            properties: {
              to: {
                type: 'string',
                description: 'Recipient email address',
              },
              subject: {
                type: 'string',
                description: 'Email subject',
              },
              body: {
                type: 'string',
                description: 'Email body (plain text)',
              },
              cc: {
                type: 'string',
                description: 'CC email addresses (comma-separated)',
              },
            },
            required: ['to', 'subject', 'body'],
          },
        },
        {
          name: 'draft_reply',
          description: 'Create a draft reply to an email',
          inputSchema: {
            type: 'object',
            properties: {
              message_id: {
                type: 'string',
                description: 'Gmail message ID to reply to',
              },
              body: {
                type: 'string',
                description: 'Reply body (plain text)',
              },
            },
            required: ['message_id', 'body'],
          },
        },
        {
          name: 'search_emails',
          description: 'Search Gmail inbox',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'Gmail search query (e.g., "from:user@example.com is:unread")',
              },
              max_results: {
                type: 'number',
                description: 'Maximum number of results (default: 10)',
              },
            },
            required: ['query'],
          },
        },
      ],
    }));

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'send_email':
            return await this.sendEmail(args);
          case 'draft_reply':
            return await this.draftReply(args);
          case 'search_emails':
            return await this.searchEmails(args);
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  async sendEmail(args) {
    const { to, subject, body, cc } = args;

    // Create email message
    const email = [
      `To: ${to}`,
      cc ? `Cc: ${cc}` : '',
      `Subject: ${subject}`,
      '',
      body,
    ].filter(Boolean).join('\n');

    // Encode email in base64
    const encodedEmail = Buffer.from(email)
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');

    // Send email
    const result = await this.gmail.users.messages.send({
      userId: 'me',
      requestBody: {
        raw: encodedEmail,
      },
    });

    return {
      content: [
        {
          type: 'text',
          text: `✅ Email sent successfully!\n\nTo: ${to}\nSubject: ${subject}\nMessage ID: ${result.data.id}`,
        },
      ],
    };
  }

  async draftReply(args) {
    const { message_id, body } = args;

    // Get original message
    const originalMsg = await this.gmail.users.messages.get({
      userId: 'me',
      id: message_id,
    });

    // Extract headers
    const headers = originalMsg.data.payload.headers;
    const getHeader = (name) => headers.find(h => h.name === name)?.value || '';

    const to = getHeader('From');
    const subject = getHeader('Subject');
    const replySubject = subject.startsWith('Re:') ? subject : `Re: ${subject}`;

    // Create reply message
    const email = [
      `To: ${to}`,
      `Subject: ${replySubject}`,
      `In-Reply-To: ${getHeader('Message-ID')}`,
      `References: ${getHeader('References')} ${getHeader('Message-ID')}`,
      '',
      body,
    ].join('\n');

    // Encode email
    const encodedEmail = Buffer.from(email)
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');

    // Create draft
    const result = await this.gmail.users.drafts.create({
      userId: 'me',
      requestBody: {
        message: {
          raw: encodedEmail,
          threadId: originalMsg.data.threadId,
        },
      },
    });

    return {
      content: [
        {
          type: 'text',
          text: `✅ Draft reply created!\n\nTo: ${to}\nSubject: ${replySubject}\nDraft ID: ${result.data.id}`,
        },
      ],
    };
  }

  async searchEmails(args) {
    const { query, max_results = 10 } = args;

    // Search emails
    const result = await this.gmail.users.messages.list({
      userId: 'me',
      q: query,
      maxResults: max_results,
    });

    const messages = result.data.messages || [];

    if (messages.length === 0) {
      return {
        content: [
          {
            type: 'text',
            text: `No emails found matching query: "${query}"`,
          },
        ],
      };
    }

    // Get details for each message
    const emailDetails = await Promise.all(
      messages.map(async (msg) => {
        const details = await this.gmail.users.messages.get({
          userId: 'me',
          id: msg.id,
        });

        const headers = details.data.payload.headers;
        const getHeader = (name) => headers.find(h => h.name === name)?.value || '';

        return {
          id: msg.id,
          from: getHeader('From'),
          subject: getHeader('Subject'),
          date: getHeader('Date'),
          snippet: details.data.snippet,
        };
      })
    );

    const resultText = emailDetails
      .map(
        (email, i) =>
          `${i + 1}. From: ${email.from}\n   Subject: ${email.subject}\n   Date: ${email.date}\n   ID: ${email.id}\n   Preview: ${email.snippet}\n`
      )
      .join('\n');

    return {
      content: [
        {
          type: 'text',
          text: `Found ${messages.length} email(s):\n\n${resultText}`,
        },
      ],
    };
  }

  async run() {
    // Authenticate first
    const authenticated = await this.authenticate();
    if (!authenticated) {
      console.error('Failed to authenticate. Please run Gmail watcher first to set up credentials.');
      process.exit(1);
    }

    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Email MCP Server running on stdio');
  }
}

// Start server
const server = new EmailMCPServer();
server.run().catch(console.error);
