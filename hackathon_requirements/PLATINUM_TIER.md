# Platinum Tier: Always-On Cloud + Local Executive

**Estimated time:** 60+ hours

## Requirements

### All Gold Requirements Plus:

### 1. Cloud Deployment
- [ ] Run AI Employee on Cloud 24/7
- [ ] Always-on watchers + orchestrator
- [ ] Health monitoring
- [ ] Deploy on Cloud VM (Oracle/AWS/etc.)

### 2. Work-Zone Specialization
- [ ] Cloud owns: Email triage, draft replies, social post drafts
- [ ] Local owns: Approvals, WhatsApp, payments/banking, final send/post
- [ ] Draft-only on Cloud (requires Local approval before send/post)

### 3. Delegation via Synced Vault
- [ ] Agents communicate via files:
  - /Needs_Action/<domain>/
  - /Plans/<domain>/
  - /Pending_Approval/<domain>/
- [ ] Prevent double-work:
  - /In_Progress/<agent>/ claim-by-move rule
  - Single-writer rule for Dashboard.md (Local)
- [ ] Cloud writes to /Updates/ or /Signals/
- [ ] Local merges into Dashboard.md
- [ ] Vault sync via Git or Syncthing

### 4. Security
- [ ] Vault sync includes only markdown/state
- [ ] Secrets never sync (.env, tokens, WhatsApp sessions, banking creds)
- [ ] Cloud never stores WhatsApp sessions, banking credentials, or payment tokens

### 5. Odoo on Cloud
- [ ] Deploy Odoo Community on Cloud VM (24/7)
- [ ] HTTPS enabled
- [ ] Backups configured
- [ ] Health monitoring
- [ ] Cloud Agent integrates with Odoo via MCP
- [ ] Draft-only accounting actions
- [ ] Local approval for posting invoices/payments

### 6. Optional A2A Upgrade (Phase 2)
- [ ] Replace file handoffs with direct A2A messages
- [ ] Keep vault as audit record

### 7. Platinum Demo (Minimum Passing Gate)
- [ ] Email arrives while Local is offline
- [ ] Cloud drafts reply + writes approval file
- [ ] When Local returns, user approves
- [ ] Local executes send via MCP
- [ ] Logs action
- [ ] Moves task to /Done

## Current Status

### ✅ What You Have (from Silver)
- Gmail watcher ✓
- LinkedIn auto-posting ✓
- Email MCP server ✓
- Human-in-the-loop approval ✓
- Cron automation ✓

### ❌ What's Missing for Platinum
- No cloud deployment
- No work-zone specialization
- No vault syncing
- No Odoo on cloud
- No distributed agent architecture
- All Gold tier requirements also missing

## Gap Analysis

**Current Level:** Silver tier functionality (local only)

**To Reach Platinum, You Need:**
1. Complete ALL Gold tier requirements first
2. Deploy to cloud VM (Oracle/AWS)
3. Implement work-zone specialization (Cloud vs Local)
4. Set up vault syncing (Git/Syncthing)
5. Deploy Odoo on cloud
6. Implement distributed agent communication
7. Add health monitoring and backups

**Estimated Additional Work:** 50-60 hours beyond Silver

**Verdict:** You are at **Silver tier**. Platinum is 2-3 tiers away.
