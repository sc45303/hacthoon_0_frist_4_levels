#!/usr/bin/env python3
"""
Plan Task Skill Implementation
Wraps existing bronze_planner.py functionality as an Agent Skill
"""
import sys
from pathlib import Path

# Add base directory to Python path for imports
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from agent.gemini_brain import think
from agent.memory_manager import add_task_to_memory
from agent.approval_manager import create_approval_request

NEEDS_ACTION = BASE_DIR / "Needs_Action"
PLANS = BASE_DIR / "Plans"

def plan_task(task_file_path):
    """
    Create execution plan for a task

    Args:
        task_file_path: Path to task file in Needs_Action folder

    Returns:
        Success message or error
    """
    task_file = Path(task_file_path)

    if not task_file.exists():
        return f"❌ Error: Task file not found: {task_file_path}"

    # Read task content
    task_text = task_file.read_text(encoding="utf-8").strip()

    if not task_text:
        return f"❌ Error: Task file is empty: {task_file.name}"

    print(f"🧠 Planning task: {task_file.name}")

    try:
        # Generate plan using Gemini
        plan = think(task_text)

        # Save plan
        plan_file = PLANS / task_file.name
        plan_file.write_text(plan, encoding="utf-8")

        # Save to memory
        add_task_to_memory(
            task_name=task_file.name,
            task_text=task_text,
            plan=plan
        )

        # Create approval request
        create_approval_request(task_file.name)

        print(f"✋ Approval requested for {task_file.name}")

        return f"✅ Plan created: Plans/{task_file.name}\n✅ Approval requested: Approvals/{task_file.name}.approval.md"

    except Exception as e:
        error_msg = f"❌ Error planning task: {str(e)}"
        print(error_msg)
        return error_msg

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python plan_task.py <task_file_path>")
        print("Example: python plan_task.py Needs_Action/EMAIL_Test_19c66ef2.md")
        sys.exit(1)

    result = plan_task(sys.argv[1])
    print(result)

    # Exit with appropriate code
    sys.exit(0 if "✅" in result else 1)
