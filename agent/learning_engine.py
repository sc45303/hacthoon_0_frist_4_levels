"""
Gold Level - Learning Engine
Analyzes past executions and feedback to improve future performance
"""

import json
from pathlib import Path
from agent.gemini_brain import client

BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = BASE_DIR / "Memory"

def load_task_history():
    """Load all past task executions"""
    history_file = MEMORY_DIR / "task_history.json"
    if history_file.exists():
        return json.loads(history_file.read_text(encoding="utf-8"))
    return {"tasks": []}

def load_feedback_history():
    """Load all feedback data"""
    feedback_file = MEMORY_DIR / "feedback_history.json"
    if feedback_file.exists():
        return json.loads(feedback_file.read_text(encoding="utf-8"))
    return {"feedbacks": []}

def analyze_similar_tasks(current_task):
    """Find similar past tasks and their outcomes"""
    history = load_task_history()
    feedback = load_feedback_history()

    # Create a map of task feedback
    feedback_map = {}
    for fb in feedback.get("feedbacks", []):
        feedback_map[fb["task"]] = fb

    # Find similar tasks
    similar_tasks = []
    for task in history.get("tasks", []):
        task_name = task.get("task", "")
        if task_name in feedback_map:
            similar_tasks.append({
                "task": task,
                "feedback": feedback_map[task_name]
            })

    return similar_tasks

def get_learning_insights(current_task_text):
    """Generate insights from past performance"""
    similar = analyze_similar_tasks(current_task_text)

    if not similar:
        return "No historical data available for learning."

    # Prepare learning context
    learning_context = "Past Task Performance:\n\n"

    for item in similar[-5:]:  # Last 5 similar tasks
        task = item["task"]
        fb = item["feedback"]

        learning_context += f"Task: {task.get('content', 'N/A')}\n"
        learning_context += f"Rating: {fb.get('rating', 'N/A')}/5\n"
        learning_context += f"Plan Quality: {fb.get('plan_quality', 'N/A')}\n"
        learning_context += f"What went well: {fb.get('went_well', 'N/A')}\n"
        learning_context += f"Improvements needed: {fb.get('improvements', 'N/A')}\n"
        learning_context += "-" * 50 + "\n"

    return learning_context

def generate_improved_plan(task_text):
    """Generate plan with learning from past feedback"""

    # Get learning insights
    insights = get_learning_insights(task_text)

    prompt = f"""
You are a Gold Level Digital AI Employee - The Learner.

Your job:
- Learn from past task executions and feedback
- Create improved plans based on historical performance
- Adapt to user preferences and patterns

Current Task:
{task_text}

Historical Learning Data:
{insights}

Based on the learning data above, create an improved execution plan that:
1. Incorporates lessons learned from past feedback
2. Avoids mistakes identified in previous executions
3. Emphasizes approaches that worked well before
4. Adapts to user preferences shown in feedback

Provide a clear, step-by-step plan that demonstrates learning and improvement.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        print(f"⚠️  Learning engine error: {e}")
        # Fallback to basic planning
        return None

def calculate_performance_metrics():
    """Calculate overall AI performance metrics"""
    feedback = load_feedback_history()

    if not feedback.get("feedbacks"):
        return None

    feedbacks = feedback["feedbacks"]

    total = len(feedbacks)
    avg_rating = sum(fb.get("rating", 0) for fb in feedbacks if fb.get("rating")) / total if total > 0 else 0

    plan_quality_good = sum(1 for fb in feedbacks if fb.get("plan_quality") == "yes")
    execution_quality_good = sum(1 for fb in feedbacks if fb.get("execution_quality") == "yes")

    metrics = {
        "total_tasks_with_feedback": total,
        "average_rating": round(avg_rating, 2),
        "plan_quality_success_rate": round((plan_quality_good / total) * 100, 1) if total > 0 else 0,
        "execution_quality_success_rate": round((execution_quality_good / total) * 100, 1) if total > 0 else 0
    }

    return metrics

def identify_improvement_areas():
    """Identify areas where AI needs to improve"""
    feedback = load_feedback_history()

    if not feedback.get("feedbacks"):
        return []

    improvements = []
    for fb in feedback["feedbacks"]:
        if fb.get("improvements"):
            improvements.append({
                "task": fb["task"],
                "improvement": fb["improvements"],
                "rating": fb.get("rating", 0)
            })

    # Focus on low-rated tasks
    low_rated = [imp for imp in improvements if imp["rating"] <= 3]

    return low_rated

if __name__ == "__main__":
    # Test the learning engine
    metrics = calculate_performance_metrics()
    if metrics:
        print("📊 Performance Metrics:")
        print(f"  Total Tasks: {metrics['total_tasks_with_feedback']}")
        print(f"  Average Rating: {metrics['average_rating']}/5")
        print(f"  Plan Quality: {metrics['plan_quality_success_rate']}%")
        print(f"  Execution Quality: {metrics['execution_quality_success_rate']}%")
    else:
        print("📊 No performance data yet")

    improvements = identify_improvement_areas()
    if improvements:
        print(f"\n🎯 Areas for Improvement: {len(improvements)}")
        for imp in improvements[:3]:
            print(f"  - {imp['task']}: {imp['improvement']}")
