# Personal AI Employee - Autonomous Multi-Agent System

[![Status](https://img.shields.io/badge/Status-Complete-success)]()
[![Levels](https://img.shields.io/badge/Levels-4%2F4-blue)]()
[![Agents](https://img.shields.io/badge/Agents-4-orange)]()

> A complete autonomous AI employee system with multi-agent collaboration, learning capabilities, and Obsidian integration.

---

## 🎯 Project Overview

This project implements a fully autonomous AI employee system that can:
- 📋 Plan complex tasks intelligently
- 🤖 Execute tasks autonomously
- 🧠 Learn from feedback and improve over time
- 🤝 Coordinate multiple specialized agents for complex problems

**Hackathon:** Personal AI Employee - Building Autonomous FTEs in 2026
**Status:** All 4 Levels Complete ✅

---

## 🏆 Implemented Levels

### 🥉 Bronze - The Planner
Automated task detection, AI-powered planning, approval workflow, and memory management.

### 🥈 Silver - The Executor
Autonomous task execution with detailed logging and lifecycle management.

### 🥇 Gold - The Learner
Learning from feedback, performance tracking, and adaptive planning with proven improvement.

### 💎 Platinum - The Collaborator
Multi-agent coordination with 4 specialized agents (Researcher, Writer, Analyst, Coder).

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Gemini API key
- Obsidian (optional, for GUI)

### Installation

```bash
# 1. Clone/navigate to project
cd AI_Employee_Vault

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API key
echo "GEMINI_API_KEY=your_key_here" > .env
```

### Run the System

```bash
# Start the AI Employee (Platinum level)
python main.py
```

---

## 📖 Usage

### Basic Workflow

1. **Create a Task**
   ```bash
   echo "Your task description" > Needs_Action/my_task.md
   ```

2. **System Generates Plan**
   - Automatically creates plan in `Plans/`
   - Creates approval request in `Approvals/`

3. **Approve the Task**
   - Open `Approvals/my_task.md.approval.md`
   - Change `[ ] Approved` to `[x] Approved`

4. **System Executes**
   - Automatically executes approved tasks
   - Moves completed task to `Done/`
   - Creates execution log in `Logs/`
   - For complex tasks, creates collaboration log in `Collaboration_Logs/`

5. **Provide Feedback** (Optional)
   - Fill out feedback form in `Feedback/`
   - System learns and improves future performance

### Example: Simple Task

```bash
# Create task
echo "Write a haiku about technology" > Needs_Action/haiku.md

# Generate plan
python -m agent.gold_planner

# Approve
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/haiku.md.approval.md

# Execute
python -m agent.platinum_executor

# Check results
cat Done/haiku.md
cat Logs/haiku.md.execution.log
```

### Example: Complex Task (Multi-Agent)

```bash
# Create complex task
echo "Research AI trends and write an article about them" > Needs_Action/article.md

# System will automatically:
# 1. Decompose into subtasks
# 2. Assign to specialized agents (Researcher, Writer)
# 3. Execute in coordination
# 4. Aggregate results

# Check collaboration
cat Collaboration_Logs/article.md.collaboration.json
```

---

## 🏗️ Architecture

```
User Input → Task Decomposer → Single/Multi-Agent → Execution → Learning
                                      ↓
                    ┌─────────────────┼─────────────────┐
                    ↓                 ↓                 ↓
              Researcher          Writer           Analyst
                Agent             Agent             Agent
```

**Key Components:**
- **Task Decomposer** - Analyzes task complexity
- **Agent Coordinator** - Orchestrates multiple agents
- **Communication Bus** - Inter-agent messaging
- **Learning Engine** - Tracks performance and improves
- **Memory Manager** - Stores task history

---

## 📁 Project Structure

```
AI_Employee_Vault/
├── agent/                    # Core AI modules (21 files)
├── Needs_Action/            # Input: New tasks
├── Plans/                   # Generated execution plans
├── Approvals/               # Approval requests
├── Done/                    # Completed tasks
├── Logs/                    # Execution logs
├── Collaboration_Logs/      # Multi-agent coordination logs
├── Feedback/                # Feedback forms for learning
├── Memory/                  # Learning database
├── .obsidian/              # Obsidian vault configuration
├── main.py                 # Entry point
└── requirements.txt        # Dependencies
```

---

## 🤖 Specialized Agents

| Agent | Capabilities | Use Cases |
|-------|-------------|-----------|
| 🔍 **Researcher** | Research, data gathering, fact-checking | Information collection, analysis |
| ✍️ **Writer** | Content creation, writing, editing | Articles, reports, documentation |
| 📊 **Analyst** | Data analysis, insights, evaluation | Data interpretation, recommendations |
| 💻 **Coder** | Code generation, debugging, technical tasks | Programming, technical solutions |

---

## 📊 Performance Metrics

**Current System Performance:**
- Tasks Completed: 3
- Average Rating: 5.0/5
- Plan Quality: 100%
- Execution Quality: 100%
- Multi-Agent Coordination: Verified ✅

---

## 🎓 Key Features

### ✅ Autonomous Operation
- Detects and processes tasks automatically
- No manual intervention required after approval
- Handles errors gracefully

### ✅ Multi-Agent Collaboration
- Decomposes complex tasks into subtasks
- Coordinates specialized agents
- Aggregates results intelligently

### ✅ Learning System
- Collects feedback after execution
- Tracks performance metrics
- Adapts future behavior based on history
- **Proven learning:** Subsequent tasks reference past feedback

### ✅ Safety Features
- Human-in-the-loop approval workflow
- Detailed audit logging
- Error handling and recovery
- Complete transparency

---

## 🔧 Configuration

### Switching Levels

Edit `main.py`:
```python
CURRENT_LEVEL = "platinum"  # Options: "silver", "gold", "platinum"
```

### API Configuration

Create `.env` file:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 📚 Documentation

- `PROJECT_DOCUMENTATION.md` - Complete technical documentation
- `GOLD_LEVEL_README.md` - Gold level features and usage
- `PLATINUM_LEVEL_README.md` - Platinum level features and usage
- `SIMPLE_TESTING_GUIDE.md` - Step-by-step testing instructions
- `HACKATHON_VERIFICATION.md` - Verification against requirements

---

## 🧪 Testing

### Run Tests

```bash
# Test Silver level
echo "Explain Python in 2 sentences" > Needs_Action/test_silver.md
python -m agent.bronze_planner
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/test_silver.md.approval.md
python -m agent.silver_executor

# Test Gold level (with learning)
echo "Write a motivational quote" > Needs_Action/test_gold.md
python -m agent.gold_planner
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/test_gold.md.approval.md
python -m agent.gold_executor

# Test Platinum level (multi-agent)
echo "Research meditation benefits and write an article" > Needs_Action/test_platinum.md
python -m agent.gold_planner
sed -i 's/\[ \] Approved/[x] Approved/' Approvals/test_platinum.md.approval.md
python -m agent.platinum_executor
```

---

## 🛠️ Technology Stack

**Core:**
- Python 3.8+
- Google Gemini 2.5 Flash
- Obsidian (Markdown-based knowledge base)

**Libraries:**
- `google-generativeai` - LLM integration
- `python-dotenv` - Configuration
- `watchdog` - File monitoring

**Architecture:**
- Multi-agent system
- Event-driven workflow
- File-based communication

---

## ⚠️ Technical Notes

### LLM Choice
This implementation uses **Google Gemini AI** instead of Claude Code. The architecture is LLM-agnostic and can be adapted to other LLMs by modifying the `agent/gemini_brain.py` module.

### Obsidian Integration
The project uses Obsidian as a knowledge base and GUI. The `.obsidian` folder contains vault configuration. You can open the entire `AI_Employee_Vault` folder in Obsidian to view tasks, plans, and logs in a visual interface.

---

## 🐛 Troubleshooting

### API Quota Exceeded
If you see "429 RESOURCE_EXHAUSTED", you've hit the Gemini API free tier limit (20 requests/day). Wait or upgrade your API plan.

### Tasks Not Executing
1. Check that task is approved: `cat Approvals/your_task.md.approval.md | grep "\[x\]"`
2. Verify plan exists: `ls Plans/your_task.md`
3. Check logs for errors: `cat Logs/your_task.md.execution.log`

### Import Errors
Make sure virtual environment is activated:
```bash
source venv/bin/activate
```

---

## 📈 Future Enhancements

- [ ] External service integration (Gmail, WhatsApp, Banking)
- [ ] MCP server support for browser automation
- [ ] Real-time monitoring dashboard
- [ ] Business handover reports
- [ ] Process management (PM2/supervisord)
- [ ] Advanced error recovery

---

## 📝 License

This project is built for the Personal AI Employee Hackathon 2026.

---

## 🙏 Acknowledgments

- Hackathon organizers for the challenge
- Google Gemini for LLM capabilities
- Obsidian for knowledge base platform

---

## 📧 Contact

For questions or issues, please refer to the documentation files or create an issue.

---

**Built with ❤️ for the Personal AI Employee Hackathon 2026**
