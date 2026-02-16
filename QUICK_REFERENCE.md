# 🤖 Personal AI Employee - Quick Reference

**Your AI Employee at a Glance**

---

## 📊 Current Status

All 4 tiers complete and running:
- 🥉 **Bronze**: AI planning with Gemini
- 🥈 **Silver**: Autonomous execution
- 🥇 **Gold**: Gmail monitoring (every 2 minutes)
- 💎 **Platinum**: LinkedIn auto-posting (hourly)

---

## 🚀 Quick Commands

### Check System Status
```bash
bash status.sh
```

### Manual Operations
```bash
# Run Gmail watcher manually
python watchers/gmail_watcher.py

# Run LinkedIn poster manually
python watchers/linkedin_poster.py

# Create plans for tasks
source venv/bin/activate
python -m agent.bronze_planner

# Execute approved tasks
python -m agent.silver_executor
```

### Post to LinkedIn
```bash
# Quick post
./quick_post.sh "Your message here #hashtags"

# Or create in queue
cat > Posts_Queue/my_post.md << 'EOF'
---
type: text
visibility: PUBLIC
---
Your post content here
