"""
Gold Level - Intelligent Planner with Learning
Uses historical data and feedback to create improved plans
"""

from pathlib import Path
from agent.gemini_brain import think
from agent.learning_engine import generate_improved_plan, get_learning_insights
from agent.memory_manager import add_task_to_memory
from agent.approval_manager import create_approval_request

BASE_DIR = Path(__file__).resolve().parent.parent
NEEDS_ACTION = BASE_DIR / "Needs_Action"
PLANS = BASE_DIR / "Plans"

def process_task_with_learning(task_file: Path):
    """Process task using learning from past executions"""
    task_text = task_file.read_text(encoding="utf-8").strip()

    if not task_text:
        return

    print(f"🧠 Planning task with learning: {task_file.name}")

    # Try to generate improved plan using learning
    improved_plan = generate_improved_plan(task_text)

    if improved_plan:
        plan = improved_plan
        print(f"✨ Generated improved plan using historical learning")
    else:
        # Fallback to basic planning
        plan = think(task_text)
        print(f"📝 Generated basic plan (no learning data available)")

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
        process_task_with_learning(task)
