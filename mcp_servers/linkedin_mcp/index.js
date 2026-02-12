#!/usr/bin/env node
/**
 * LinkedIn MCP Server
 * Provides LinkedIn posting capabilities via MCP protocol
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import axios from 'axios';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Paths
const TOKEN_PATH = path.join(__dirname, '../../credentials/linkedin_token.json');

// LinkedIn API
const API_URL = 'https://api.linkedin.com/v2/ugcPosts';
const REQUIRED_HEADERS = {
  'X-Restli-Protocol-Version': '2.0.0',
  'Content-Type': 'application/json'
};

class LinkedInMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'linkedin-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.tokenData = null;
    this.setupHandlers();
  }

  loadToken() {
    try {
      if (!fs.existsSync(TOKEN_PATH)) {
        throw new Error(`Token file not found: ${TOKEN_PATH}. Run authenticate_linkedin.py first.`);
      }

      const data = fs.readFileSync(TOKEN_PATH, 'utf8');
      this.tokenData = JSON.parse(data);

      if (!this.tokenData.access_token || !this.tokenData.person_urn) {
        throw new Error('Invalid token data. Missing access_token or person_urn.');
      }

      return true;
    } catch (error) {
      console.error('Error loading token:', error.message);
      return false;
    }
  }

  setupHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'post_to_linkedin',
          description: 'Post a text update to LinkedIn. The post will be visible to your network based on the visibility setting.',
          inputSchema: {
            type: 'object',
            properties: {
              text: {
                type: 'string',
                description: 'The text content of the post. Can include hashtags and mentions.',
              },
              visibility: {
                type: 'string',
                enum: ['PUBLIC', 'CONNECTIONS'],
                description: 'Who can see the post. PUBLIC = anyone on LinkedIn, CONNECTIONS = only 1st-degree connections. Default: PUBLIC',
                default: 'PUBLIC'
              }
            },
            required: ['text'],
          },
        },
        {
          name: 'post_article_to_linkedin',
          description: 'Post an article or URL to LinkedIn with a preview card. Great for sharing blog posts, articles, or web content.',
          inputSchema: {
            type: 'object',
            properties: {
              text: {
                type: 'string',
                description: 'Commentary text to accompany the article link.',
              },
              url: {
                type: 'string',
                description: 'The URL of the article to share.',
              },
              title: {
                type: 'string',
                description: 'Optional custom title for the article preview card.',
              },
              description: {
                type: 'string',
                description: 'Optional custom description for the article preview card.',
              },
              visibility: {
                type: 'string',
                enum: ['PUBLIC', 'CONNECTIONS'],
                description: 'Who can see the post. Default: PUBLIC',
                default: 'PUBLIC'
              }
            },
            required: ['text', 'url'],
          },
        },
      ],
    }));

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        // Load token for each request
        if (!this.loadToken()) {
          throw new Error('Failed to load LinkedIn authentication token');
        }

        switch (name) {
          case 'post_to_linkedin':
            return await this.postToLinkedIn(args);
          case 'post_article_to_linkedin':
            return await this.postArticleToLinkedIn(args);
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

  async postToLinkedIn(args) {
    const { text, visibility = 'PUBLIC' } = args;

    if (!text || text.trim().length === 0) {
      throw new Error('Post text cannot be empty');
    }

    const payload = {
      author: this.tokenData.person_urn,
      lifecycleState: 'PUBLISHED',
      specificContent: {
        'com.linkedin.ugc.ShareContent': {
          shareCommentary: {
            text: text
          },
          shareMediaCategory: 'NONE'
        }
      },
      visibility: {
        'com.linkedin.ugc.MemberNetworkVisibility': visibility
      }
    };

    try {
      const response = await axios.post(API_URL, payload, {
        headers: {
          ...REQUIRED_HEADERS,
          'Authorization': `Bearer ${this.tokenData.access_token}`
        }
      });

      const postId = response.headers['x-restli-id'] || 'unknown';

      return {
        content: [
          {
            type: 'text',
            text: `✅ Successfully posted to LinkedIn!\n\nPost ID: ${postId}\nVisibility: ${visibility}\n\nPreview:\n${text.substring(0, 200)}${text.length > 200 ? '...' : ''}`,
          },
        ],
      };
    } catch (error) {
      const errorMsg = error.response?.data?.message || error.message;
      throw new Error(`Failed to post to LinkedIn: ${errorMsg}`);
    }
  }

  async postArticleToLinkedIn(args) {
    const { text, url, title, description, visibility = 'PUBLIC' } = args;

    if (!text || text.trim().length === 0) {
      throw new Error('Post text cannot be empty');
    }

    if (!url || !url.startsWith('http')) {
      throw new Error('Invalid URL. Must start with http:// or https://');
    }

    const media = {
      status: 'READY',
      originalUrl: url
    };

    if (title) {
      media.title = { text: title };
    }

    if (description) {
      media.description = { text: description };
    }

    const payload = {
      author: this.tokenData.person_urn,
      lifecycleState: 'PUBLISHED',
      specificContent: {
        'com.linkedin.ugc.ShareContent': {
          shareCommentary: {
            text: text
          },
          shareMediaCategory: 'ARTICLE',
          media: [media]
        }
      },
      visibility: {
        'com.linkedin.ugc.MemberNetworkVisibility': visibility
      }
    };

    try {
      const response = await axios.post(API_URL, payload, {
        headers: {
          ...REQUIRED_HEADERS,
          'Authorization': `Bearer ${this.tokenData.access_token}`
        }
      });

      const postId = response.headers['x-restli-id'] || 'unknown';

      return {
        content: [
          {
            type: 'text',
            text: `✅ Successfully posted article to LinkedIn!\n\nPost ID: ${postId}\nURL: ${url}\nVisibility: ${visibility}\n\nPreview:\n${text.substring(0, 200)}${text.length > 200 ? '...' : ''}`,
          },
        ],
      };
    } catch (error) {
      const errorMsg = error.response?.data?.message || error.message;
      throw new Error(`Failed to post article to LinkedIn: ${errorMsg}`);
    }
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('LinkedIn MCP server running on stdio');
  }
}

// Start server
const server = new LinkedInMCPServer();
server.run().catch(console.error);
