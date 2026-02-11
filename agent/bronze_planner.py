# from pathlib import Path
# from agent.gemini_brain import think

# BASE_DIR = Path(__file__).resolve().parent.parent
# NEEDS_ACTION = BASE_DIR / "Needs_Action"
# PLANS = BASE_DIR / "Plans"

# def process_task(task_file: Path):
#     task_text = task_file.read_text(encoding="utf-8").strip()

#     if not task_text:
#         return

#     print(f"🧠 Thinking about: {task_file.name}")

#     plan = think(task_text)

#     plan_file = PLANS / task_file.name
#     plan_file.write_text(plan, encoding="utf-8")

#     print(f"📄 Plan saved to Plans/{task_file.name}")

# if __name__ == "__main__":
#     for task in NEEDS_ACTION.glob("*.md"):
#         process_task(task)








# ///////////////////////////////////////

from pathlib import Path
from agent.gemini_brain import think
from agent.memory_manager import add_task_to_memory
from agent.approval_manager import create_approval_request

BASE_DIR = Path(__file__).resolve().parent.parent
NEEDS_ACTION = BASE_DIR / "Needs_Action"
PLANS = BASE_DIR / "Plans"

def process_task(task_file: Path):
    task_text = task_file.read_text(encoding="utf-8").strip()

    if not task_text:
        return

    print(f"🧠 Planning task: {task_file.name}")

    plan = think(task_text)

    # Save plan
    plan_file = PLANS / task_file.name
    plan_file.write_text(plan, encoding="utf-8")

    # Save memory
    add_task_to_memory(
        task_name=task_file.name,
        task_text=task_text,
        plan=plan
    )

    # Ask for approval
    create_approval_request(task_file.name)

    print(f"✋ Approval requested for {task_file.name}")

if __name__ == "__main__":
    for task in NEEDS_ACTION.glob("*.md"):
        process_task(task)
