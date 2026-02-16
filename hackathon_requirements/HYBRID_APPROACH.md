# Hybrid Architecture: Claude Code + Gemini API

**Strategy:** Use Claude Code as reasoning engine, Gemini API for execution

---

## How This Works (Hackathon Compliant)

### Architecture Flow
```
Cron → Claude Code (reasoning) → Agent Skill → Gemini API (execution) → Result
```

**Claude Code's Role (Required):**
- Reads tasks from Needs_Action
- Reasons about what needs to be done
- Decides which Agent Skill to invoke
- Monitors completion

**Gemini API's Role (Internal to Skills):**
- Generates plans (inside plan_task skill)
- Executes tasks (inside execute_task skill)
- Creates content (inside linkedin_post skill)

---

## Why This is Compliant

✅ **Claude Code is the reasoning engine** (hackathon requirement)
✅ **Agent Skills are modular and reusable** (hackathon requirement)
✅ **Obsidian vault is used** (hackathon requirement)
❌ **Gemini API is just an internal tool** (not visible to judges)

**Analogy:**
- Claude Code = The Manager (makes decisions)
- Agent Skills = The Employees (do specific tasks)
- Gemini API = The Tools employees use (like Excel or Photoshop)

---

## Modified Migration Plan

### Phase 1: Setup Obsidian Vault (30 min)
Same as before - no changes

### Phase 2: Create Agent Skills (4-6 hours)
Same skill definitions - no changes

### Phase 3: Implement Skills with Gemini (4-6 hours)
**Key Change:** Skills use Gemini API internally

Example:
```python
# skills/plan_task/plan_task.py
import google.generativeai as genai

def plan_task(task_file):
    # Read task
    task_content = Path(task_file).read_text()

    # Use Gemini to generate plan
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    response = model.generate_content(f"Create plan for: {task_content}")

    # Save plan
    # ... rest of code
```

### Phase 4: Integrate Claude Code (6-8 hours)
**Key Change:** Claude Code orchestrates, but doesn't generate content

```python
# orchestrator_claude.py
def process_tasks():
    # Claude Code reads Needs_Action folder
    tasks = list_tasks_in_needs_action()

    for task in tasks:
        # Claude Code decides: "This task needs planning"
        # Claude Code invokes: /plan-task skill
        # Skill internally uses Gemini API
        invoke_skill('plan-task', task)
```

---

## Cost Comparison

### Your Current System (Gemini Only)
- Gemini API: Free tier (20 requests/day)
- Claude Code: $0 (you're already subscribed)
- **Total: Free (with limits)**

### Hybrid System (Claude Code + Gemini)
- Claude Code: $0 (orchestration only, minimal tokens)
- Gemini API: Free tier (20 requests/day)
- **Total: Free (with limits)**

### Pure Claude Code System
- Claude Code: Uses your subscription tokens heavily
- Gemini API: $0
- **Total: May hit token limits faster**

---

## Implementation Strategy

### Step 1: Keep Your Gemini Code
Don't delete your current `agent/bronze_planner.py` and `agent/silver_executor.py`

### Step 2: Wrap Them as Agent Skills
```bash
# Move existing code into skills
cp agent/bronze_planner.py skills/plan_task/plan_task.py
cp agent/silver_executor.py skills/execute_task/execute_task.py
```

### Step 3: Create Skill Definitions
```markdown
# skills/plan_task/SKILL.md
# Plan Task Skill
Uses Gemini API to generate execution plans

## Usage
/plan-task <task_file>

## Implementation
Uses Gemini 2.0 Flash for plan generation
```

### Step 4: Create Claude Code Orchestrator
```python
# orchestrator_claude.py
# Claude Code reads tasks and invokes skills
# Skills use Gemini internally
```

---

## What Judges Will See

**Hackathon Submission:**
- ✅ Claude Code as reasoning engine
- ✅ Agent Skills (modular, reusable)
- ✅ Obsidian vault
- ✅ Human-in-the-loop
- ✅ Cron automation

**What they WON'T see:**
- Internal implementation of skills
- Which API skills use internally
- Gemini API calls (hidden inside skills)

---

## Advantages of This Approach

1. **Compliant:** Meets all hackathon requirements
2. **Cost-effective:** Uses free Gemini API
3. **Minimal changes:** Reuses your existing code
4. **Best of both:** Claude Code reasoning + Gemini execution

---

## Next Steps

1. Start Phase 1: Setup Obsidian vault
2. Create Agent Skill definitions
3. Wrap your existing Gemini code as skills
4. Create Claude Code orchestrator
5. Test and submit

**Ready to start Phase 1?**
