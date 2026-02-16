#!/usr/bin/env python3
"""
Execute Task Skill Implementation
Wraps existing silver_executor.py functionality as an Agent Skill
"""
import sys
from pathlib import Path
from datetime import datetime

# Add base directory to Python path for imports
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from agent.gemini_brain import client
from agent.memory_manager import load_memory, save_memory

NEEDS_ACTION = BASE_DIR / "Needs_Action"
PLANS = BASE_DIR / "Plans"
APPROVALS = BASE_DIR / "Approvals"
DONE = BASE_DIR / "Done"
LOGS = BASE_DIR / "Logs"

def check_approval(task_name):
    """Check if a task has been approved"""
    approval_file = APPROVALS / f"{task_name}.approval.md"

    if not approval_file.exists():
        return False, "No approval file found"

    text = approval_file.read_text(encoding="utf-8")

    if "[x] Approved" in text or "[X] Approved" in text:
        return True, "Approved"
    elif "[x] Rejected" in text or "[X] Rejected" in text:
        return False, "Rejected"
    else:
        return False, "Pending approval"

def execute_plan(task_name, plan_text, task_content):
    """Execute a plan using Gemini to interpret and perform actions"""

    print(f"🚀 Executing task: {task_name}")

    prompt = f"""
You are a Digital AI Employee at Silver Level - The Executor.

Your job:
1. Read the task and plan
2. Execute the plan step by step
3. Provide a detailed execution report

Task: {task_content}

Plan:
{plan_text}

Execute this plan and provide:
- What actions you took for each step
- Results of each action
- Any outputs or deliverables created
- Final status (completed/failed)

Respond with a clear execution report.
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

def execute_task(task_file_path):
    """
    Execute an approved task according to its plan

    Args:
        task_file_path: Path to task file in Needs_Action folder

    Returns:
        Success message or error
    """
    task_file = Path(task_file_path)
    task_name = task_file.name

    if not task_file.exists():
        return f"❌ Error: Task file not found: {task_file_path}"

    # Check approval
    approved, status = check_approval(task_name)
    if not approved:
        return f"❌ Cannot execute: {status}"

    # Check if plan exists
    plan_file = PLANS / task_name
    if not plan_file.exists():
        return f"❌ Error: No plan found for {task_name}"

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
        return f"✅ Task executed successfully: {task_name}\n📦 Moved to Done folder\n📝 Log: Logs/{task_name}.execution.log"
    else:
        return f"❌ Task execution failed: {task_name}\n📝 Log: Logs/{task_name}.execution.log"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python execute_task.py <task_file_path>")
        print("Example: python execute_task.py Needs_Action/EMAIL_Test_19c66ef2.md")
        sys.exit(1)

    result = execute_task(sys.argv[1])
    print(result)

    # Exit with appropriate code
    sys.exit(0 if "✅" in result else 1)
