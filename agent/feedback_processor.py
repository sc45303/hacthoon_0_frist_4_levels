"""
Gold Level - Feedback Processor
Watches for completed feedback forms and processes them for learning
"""

from pathlib import Path
from agent.feedback_manager import read_feedback, save_feedback_to_history
from agent.learning_engine import calculate_performance_metrics

BASE_DIR = Path(__file__).resolve().parent.parent
FEEDBACK_DIR = BASE_DIR / "Feedback"

def process_feedback_forms():
    """Process all completed feedback forms"""

    print("📊 Processing feedback for learning...")

    processed_count = 0

    for feedback_file in FEEDBACK_DIR.glob("*.feedback.md"):
        task_name = feedback_file.stem.replace(".feedback", "")

        # Read and parse feedback
        feedback = read_feedback(task_name)

        if not feedback:
            continue

        # Check if feedback is complete (has rating)
        if feedback.get("rating") is None:
            print(f"⏳ Waiting for feedback: {task_name}")
            continue

        # Save to learning database
        save_feedback_to_history(feedback)

        # Archive the feedback form
        archive_dir = FEEDBACK_DIR / "Processed"
        archive_dir.mkdir(exist_ok=True)

        archive_file = archive_dir / feedback_file.name
        feedback_file.rename(archive_file)

        print(f"✅ Processed feedback: {task_name} (Rating: {feedback['rating']}/5)")
        processed_count += 1

    if processed_count == 0:
        print("✨ No new feedback to process")
    else:
        print(f"\n🎉 Processed {processed_count} feedback(s)")

        # Show updated metrics
        metrics = calculate_performance_metrics()
        if metrics:
            print("\n📈 Updated Performance Metrics:")
            print(f"  Average Rating: {metrics['average_rating']}/5")
            print(f"  Plan Quality: {metrics['plan_quality_success_rate']}%")
            print(f"  Execution Quality: {metrics['execution_quality_success_rate']}%")

if __name__ == "__main__":
    process_feedback_forms()
