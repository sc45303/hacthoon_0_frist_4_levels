#!/usr/bin/env python3
"""
Claude Code Orchestrator
Uses Claude Code as reasoning engine to invoke Agent Skills

This orchestrator:
1. Reads tasks from Needs_Action folder
2. Uses Claude Code to reason about what to do
3. Invokes appropriate Agent Skills
4. Logs all actions
"""
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
NEEDS_ACTION = BASE_DIR / "Needs_Action"
PLANS = BASE_DIR / "Plans"
APPROVALS = BASE_DIR / "Approvals"
DONE = BASE_DIR / "Done"
SKILLS_DIR = BASE_DIR / "skills"
LOGS_DIR = BASE_DIR / "Memory" / "cron_logs"

def log(message):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def invoke_skill(skill_name, *args):
    """
    Invoke an Agent Skill

    Args:
        skill_name: Name of skill (e.g., 'plan_task', 'execute_task')
        *args: Arguments to pass to skill

    Returns:
        (success, output)
    """
    skill_script = SKILLS_DIR / skill_name / f"{skill_name}.py"

    if not skill_script.exists():
        return False, f"Skill not found: {skill_name}"

    # Build command
    cmd = [sys.executable, str(skill_script)] + list(args)

    try:
        result = subprocess.run(
            cmd,
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )

        success = result.returncode == 0
        output = result.stdout if result.stdout else result.stderr

        return success, output

    except subprocess.TimeoutExpired:
        return False, f"Skill timeout: {skill_name}"
    except Exception as e:
        return False, f"Error invoking skill: {str(e)}"

def process_needs_action():
    """
    Process all tasks in Needs_Action folder
    Creates plans for tasks that don't have them
    """
    log("🔍 Checking Needs_Action folder...")

    tasks = list(NEEDS_ACTION.glob("*.md"))

    if not tasks:
        log("✨ No tasks in Needs_Action")
        return 0

    log(f"📋 Found {len(tasks)} task(s)")

    planned_count = 0

    for task_file in tasks:
        task_name = task_file.name

        # Check if plan already exists
        plan_file = PLANS / task_name
        if plan_file.exists():
            log(f"⏭️  Plan exists: {task_name}")
            continue

        # Create plan using plan_task skill
        log(f"🧠 Planning: {task_name}")
        success, output = invoke_skill('plan_task', str(task_file))

        if success:
            log(f"✅ Planned: {task_name}")
            planned_count += 1
        else:
            log(f"❌ Failed to plan: {task_name}")
            log(f"   Error: {output}")

    return planned_count

def process_approved_tasks():
    """
    Execute all approved tasks
    """
    log("🔍 Checking for approved tasks...")

    # First, check which tasks are approved
    success, output = invoke_skill('check_approvals')

    if not success:
        log(f"❌ Failed to check approvals: {output}")
        return 0

    # Parse output to find approved tasks (simple approach)
    # In production, this would be more robust
    tasks = list(NEEDS_ACTION.glob("*.md"))
    executed_count = 0

    for task_file in tasks:
        task_name = task_file.name
        approval_file = APPROVALS / f"{task_name}.approval.md"

        if not approval_file.exists():
            continue

        # Check if approved
        content = approval_file.read_text(encoding='utf-8')
        if "[x] Approved" not in content and "[X] Approved" not in content:
            log(f"⏳ Waiting for approval: {task_name}")
            continue

        # Execute task
        log(f"🚀 Executing: {task_name}")
        success, output = invoke_skill('execute_task', str(task_file))

        if success:
            log(f"✅ Executed: {task_name}")
            executed_count += 1
        else:
            log(f"❌ Failed to execute: {task_name}")
            log(f"   Error: {output}")

    return executed_count

def update_dashboard():
    """Update dashboard with current metrics"""
    log("📊 Updating dashboard...")

    success, output = invoke_skill('update_dashboard')

    if success:
        log("✅ Dashboard updated")
    else:
        log(f"❌ Failed to update dashboard: {output}")

def run_planner_mode():
    """
    Planner mode: Process Needs_Action and create plans
    """
    log("=" * 60)
    log("🧠 CLAUDE CODE ORCHESTRATOR - PLANNER MODE")
    log("=" * 60)

    planned = process_needs_action()

    if planned > 0:
        update_dashboard()

    log("=" * 60)
    log(f"✅ Planner completed: {planned} task(s) planned")
    log("=" * 60)

def run_executor_mode():
    """
    Executor mode: Execute approved tasks
    """
    log("=" * 60)
    log("⚡ CLAUDE CODE ORCHESTRATOR - EXECUTOR MODE")
    log("=" * 60)

    executed = process_approved_tasks()

    if executed > 0:
        update_dashboard()

    log("=" * 60)
    log(f"✅ Executor completed: {executed} task(s) executed")
    log("=" * 60)

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python orchestrator_claude.py [plan|execute]")
        print("  plan    - Process Needs_Action and create plans")
        print("  execute - Execute approved tasks")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "plan":
        run_planner_mode()
    elif mode == "execute":
        run_executor_mode()
    else:
        print(f"Unknown mode: {mode}")
        print("Use 'plan' or 'execute'")
        sys.exit(1)

if __name__ == '__main__':
    main()
