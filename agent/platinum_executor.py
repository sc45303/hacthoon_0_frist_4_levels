"""
Platinum Level - Executor with Multi-Agent Collaboration
Executes tasks using coordinated agents
"""

import os
from pathlib import Path
from agent.agent_coordinator import AgentCoordinator
from agent.memory_manager import load_memory, save_memory
from agent.feedback_manager import create_feedback_request
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent.parent
NEEDS_ACTION = BASE_DIR / "Needs_Action"
PLANS = BASE_DIR / "Plans"
APPROVALS = BASE_DIR / "Approvals"
DONE = BASE_DIR / "Done"
LOGS = BASE_DIR / "Logs"
COLLABORATION_LOGS = BASE_DIR / "Collaboration_Logs"
COLLABORATION_LOGS.mkdir(exist_ok=True)

def check_approval(task_name):
    """Check if a task has been approved"""
    approval_file = APPROVALS / f"{task_name}.approval.md"

    if not approval_file.exists():
        return False

    text = approval_file.read_text(encoding="utf-8")
    return "[x] Approved" in text or "[X] Approved" in text

def execute_with_collaboration(task_name, task_content):
    """Execute a task using multi-agent collaboration"""

    print(f"🚀 Executing task with Platinum level: {task_name}")

    # Initialize coordinator
    coordinator = AgentCoordinator()

    try:
        # Execute using multiple agents
        result = coordinator.execute_complex_task(task_content)

        # Save collaboration log
        log_file = COLLABORATION_LOGS / f"{task_name}.collaboration.json"
        log_file.write_text(json.dumps(result, indent=2), encoding="utf-8")

        # Create execution log
        log_file_md = LOGS / f"{task_name}.execution.log"
        log_content = f"""# Platinum Level Execution Log: {task_name}
Timestamp: {datetime.now().isoformat()}

## Task
{task_content}

## Collaboration Details
- Agents Involved: {result.get('agents_involved', 1)}
- Subtasks Completed: {result.get('subtasks_completed', 1)}
- Collaboration: {'Yes' if result.get('collaboration') else 'No'}

## Agent Outputs

"""
        for output in result.get('agent_outputs', []):
            log_content += f"""### {output.get('agent')} Agent
**Subtask:** {output.get('subtask')}
**Status:** {output.get('status')}

**Output:**
{output.get('output', 'No output')}

---

"""

        log_content += f"\nStatus: Completed"
        log_file_md.write_text(log_content, encoding="utf-8")

        print(f"✅ Task executed successfully: {task_name}")
        return True, result

    except Exception as e:
        error_msg = f"Error executing task: {str(e)}"
        print(f"❌ {error_msg}")

        # Log the error
        log_file = LOGS / f"{task_name}.execution.log"
        log_content = f"""# Execution Log: {task_name}
Timestamp: {datetime.now().isoformat()}

## Task
{task_content}

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
            task["execution_report"] = str(report)
            task["executed_at"] = datetime.now().isoformat()
            task["execution_level"] = "platinum"
            break

    save_memory(memory)

def process_approved_tasks():
    """Main execution loop - process all approved tasks with Platinum level"""

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

        # Read task
        task_content = task_file.read_text(encoding="utf-8").strip()

        # Execute with multi-agent collaboration
        success, report = execute_with_collaboration(task_name, task_content)

        # Update memory
        update_memory_execution(task_name, success, report)

        # Move to done if successful
        if success:
            move_to_done(task_name)

            # Request feedback for learning (Gold level feature maintained)
            create_feedback_request(task_name)
            print(f"📋 Feedback requested for learning")

        executed_count += 1

    if executed_count == 0:
        print("✨ No approved tasks to execute")
    else:
        print(f"\n🎉 Executed {executed_count} task(s)")

if __name__ == "__main__":
    process_approved_tasks()
