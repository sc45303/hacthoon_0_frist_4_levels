"""
Gold Level - Executor with Feedback Collection
Executes tasks and requests feedback for learning
"""

import os
from pathlib import Path
from agent.gemini_brain import client
from agent.memory_manager import load_memory, save_memory
from agent.feedback_manager import create_feedback_request
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
NEEDS_ACTION = BASE_DIR / "Needs_Action"
PLANS = BASE_DIR / "Plans"
APPROVALS = BASE_DIR / "Approvals"
DONE = BASE_DIR / "Done"
LOGS = BASE_DIR / "Logs"

def check_approval(task_name):
    """Check if a task has been approved"""
    approval_file = APPROVALS / f"{task_name}.approval.md"

    if not approval_file.exists():
        return False

    text = approval_file.read_text(encoding="utf-8")
    return "[x] Approved" in text or "[X] Approved" in text

def execute_plan(task_name, plan_text, task_content):
    """Execute a plan using LLM to interpret and perform actions"""

    print(f"🚀 Executing task: {task_name}")

    prompt = f"""
You are a Gold Level Digital AI Employee - The Learner.

Your job:
1. Execute the plan step by step
2. Provide detailed execution report
3. Reflect on what could be improved for future learning

Task: {task_content}

Plan:
{plan_text}

Execute this plan and provide:
- What actions you took for each step
- Results of each action
- Any outputs or deliverables created
- Self-reflection: What worked well and what could be improved
- Final status (completed/failed)

Respond with a clear execution report including self-reflection.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        execution_report = response.text.strip()

        # Log the execution
        log_file = LOGS / f"{task_name}.execution.log"
        log_content = f"""# Execution Log: {task_name}
Timestamp: {datetime.now().isoformat()}

## Task
{task_content}

## Plan
{plan_text}

## Execution Report
{execution_report}

Status: Completed
"""
        log_file.write_text(log_content, encoding="utf-8")

        print(f"✅ Task executed successfully: {task_name}")
        return True, execution_report

    except Exception as e:
        error_msg = f"Error executing task: {str(e)}"
        print(f"❌ {error_msg}")

        # Log the error
        log_file = LOGS / f"{task_name}.execution.log"
        log_content = f"""# Execution Log: {task_name}
Timestamp: {datetime.now().isoformat()}

## Task
{task_content}

## Plan
{plan_text}

## Error
{error_msg}

Status: Failed
"""
        log_file.write_text(log_content, encoding="utf-8")

        return False, error_msg

def move_to_done(task_name):
    """Move completed task from Needs_Action to Done"""
    source = NEEDS_ACTION / task_name
    dest = DONE / task_name

    if source.exists():
        source.rename(dest)
        print(f"📦 Moved {task_name} to Done folder")

def update_memory_execution(task_name, success, report):
    """Update memory with execution results"""
    memory = load_memory()

    for task in memory["tasks"]:
        if task["task"] == task_name and task["status"] == "planned":
            task["status"] = "completed" if success else "failed"
            task["execution_report"] = report
            task["executed_at"] = datetime.now().isoformat()
            break

    save_memory(memory)

def process_approved_tasks():
    """Main execution loop - process all approved tasks"""

    print("🔍 Checking for approved tasks...")

    executed_count = 0

    for task_file in NEEDS_ACTION.glob("*.md"):
        task_name = task_file.name

        # Check if approved
        if not check_approval(task_name):
            print(f"⏳ Waiting for approval: {task_name}")
            continue

        # Check if plan exists
        plan_file = PLANS / task_name
        if not plan_file.exists():
            print(f"⚠️  No plan found for: {task_name}")
            continue

        # Read task and plan
        task_content = task_file.read_text(encoding="utf-8").strip()
        plan_text = plan_file.read_text(encoding="utf-8").strip()

        # Execute the plan
        success, report = execute_plan(task_name, plan_text, task_content)

        # Update memory
        update_memory_execution(task_name, success, report)

        # Move to done if successful
        if success:
            move_to_done(task_name)

            # Request feedback for learning (Gold Level feature)
            create_feedback_request(task_name)
            print(f"📋 Feedback requested for learning")

        executed_count += 1

    if executed_count == 0:
        print("✨ No approved tasks to execute")
    else:
        print(f"\n🎉 Executed {executed_count} task(s)")

if __name__ == "__main__":
    process_approved_tasks()
