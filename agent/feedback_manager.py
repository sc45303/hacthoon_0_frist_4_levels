"""
Gold Level - Feedback Collection System
Allows users to provide feedback on task executions for learning
"""

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
FEEDBACK_DIR = BASE_DIR / "Feedback"
FEEDBACK_DIR.mkdir(exist_ok=True)

def create_feedback_request(task_name):
    """Create a feedback form after task execution"""
    feedback_file = FEEDBACK_DIR / f"{task_name}.feedback.md"

    if feedback_file.exists():
        return

    content = f"""# Feedback Request

Task: {task_name}
Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Quality Rating
Rate the execution quality (1-5):
[ ] 1 - Poor
[ ] 2 - Below Average
[ ] 3 - Average
[ ] 4 - Good
[ ] 5 - Excellent

## Plan Quality
Was the plan appropriate?
[ ] Yes
[ ] No
[ ] Partially

## Execution Quality
Was the execution satisfactory?
[ ] Yes
[ ] No
[ ] Partially

## What went well?


## What could be improved?


## Additional Comments?


---
*This feedback helps the AI learn and improve future performance*
"""
    feedback_file.write_text(content, encoding="utf-8")
    print(f"📋 Feedback request created: {task_name}")

def read_feedback(task_name):
    """Parse feedback from markdown file"""
    feedback_file = FEEDBACK_DIR / f"{task_name}.feedback.md"

    if not feedback_file.exists():
        return None

    text = feedback_file.read_text(encoding="utf-8")

    feedback = {
        "task": task_name,
        "rating": None,
        "plan_quality": None,
        "execution_quality": None,
        "went_well": "",
        "improvements": "",
        "comments": ""
    }

    # Parse rating
    for i in range(1, 6):
        if f"[x] {i}" in text or f"[X] {i}" in text:
            feedback["rating"] = i
            break

    # Parse plan quality
    if "[x] Yes" in text.split("Was the plan appropriate?")[1].split("##")[0]:
        feedback["plan_quality"] = "yes"
    elif "[x] No" in text.split("Was the plan appropriate?")[1].split("##")[0]:
        feedback["plan_quality"] = "no"
    elif "[x] Partially" in text.split("Was the plan appropriate?")[1].split("##")[0]:
        feedback["plan_quality"] = "partially"

    # Parse execution quality
    if "[x] Yes" in text.split("Was the execution satisfactory?")[1].split("##")[0]:
        feedback["execution_quality"] = "yes"
    elif "[x] No" in text.split("Was the execution satisfactory?")[1].split("##")[0]:
        feedback["execution_quality"] = "no"
    elif "[x] Partially" in text.split("Was the execution satisfactory?")[1].split("##")[0]:
        feedback["execution_quality"] = "partially"

    # Parse text sections
    try:
        feedback["went_well"] = text.split("## What went well?")[1].split("##")[0].strip()
        feedback["improvements"] = text.split("## What could be improved?")[1].split("##")[0].strip()
        feedback["comments"] = text.split("## Additional Comments?")[1].split("---")[0].strip()
    except:
        pass

    return feedback

def save_feedback_to_history(feedback):
    """Save parsed feedback to learning database"""
    feedback_db = BASE_DIR / "Memory" / "feedback_history.json"

    if feedback_db.exists():
        data = json.loads(feedback_db.read_text(encoding="utf-8"))
    else:
        data = {"feedbacks": []}

    feedback["timestamp"] = datetime.now().isoformat()
    data["feedbacks"].append(feedback)

    feedback_db.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )

    print(f"✅ Feedback saved to learning database")
