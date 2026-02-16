#!/usr/bin/env python3
"""
Check Approvals Skill Implementation
Scans approval files and identifies approved tasks
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
NEEDS_ACTION = BASE_DIR / "Needs_Action"
APPROVALS = BASE_DIR / "Approvals"

def check_approvals():
    """
    Check all approval files and categorize tasks

    Returns:
        Dictionary with approved, pending, and rejected tasks
    """
    approved = []
    pending = []
    rejected = []
    orphaned = []

    print("🔍 Checking for approved tasks...")

    # Scan all approval files
    for approval_file in APPROVALS.glob("*.approval.md"):
        # Extract task name (remove .approval.md suffix)
        task_name = approval_file.name.replace(".approval.md", "")

        # Check if task still exists in Needs_Action
        task_file = NEEDS_ACTION / task_name
        if not task_file.exists():
            orphaned.append(task_name)
            continue

        # Read approval status
        try:
            content = approval_file.read_text(encoding="utf-8")

            if "[x] Approved" in content or "[X] Approved" in content:
                approved.append(task_name)
            elif "[x] Rejected" in content or "[X] Rejected" in content:
                rejected.append(task_name)
            else:
                pending.append(task_name)

        except Exception as e:
            print(f"⚠️  Error reading {approval_file.name}: {e}")
            continue

    # Print summary
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║                  APPROVAL STATUS REPORT                    ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    if approved:
        print(f"✅ APPROVED (Ready to Execute): {len(approved)}")
        for task in approved:
            print(f"   → {task}")
        print()

    if pending:
        print(f"⏳ PENDING (Awaiting Human): {len(pending)}")
        for task in pending:
            print(f"   → {task}")
        print()

    if rejected:
        print(f"❌ REJECTED (Will Not Execute): {len(rejected)}")
        for task in rejected:
            print(f"   → {task}")
        print()

    if orphaned:
        print(f"🗑️  ORPHANED (Task deleted but approval exists): {len(orphaned)}")
        for task in orphaned:
            print(f"   → {task}")
        print()

    if not approved and not pending and not rejected:
        print("✨ No approval files found")
    else:
        print(f"NEXT ACTION: Execute {len(approved)} approved task(s)")

    return {
        "approved": approved,
        "pending": pending,
        "rejected": rejected,
        "orphaned": orphaned
    }

if __name__ == '__main__':
    result = check_approvals()

    # Exit with count of approved tasks
    sys.exit(len(result["approved"]))
