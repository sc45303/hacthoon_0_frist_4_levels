from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
APPROVALS_DIR = BASE_DIR / "Approvals"

def create_approval_request(task_name):
    approval_file = APPROVALS_DIR / f"{task_name}.approval.md"

    if approval_file.exists():
        return

    content = f"""# Approval Request

Task: {task_name}

Decision:
[ ] Approved
[ ] Rejected

Notes:
"""
    approval_file.write_text(content, encoding="utf-8")

def read_approval(task_name):
    approval_file = APPROVALS_DIR / f"{task_name}.approval.md"

    if not approval_file.exists():
        return None

    text = approval_file.read_text(encoding="utf-8")

    if "[x] Approved" in text or "[X] Approved" in text:
        return "approved"
    if "[x] Rejected" in text or "[X] Rejected" in text:
        return "rejected"

    return "pending"
