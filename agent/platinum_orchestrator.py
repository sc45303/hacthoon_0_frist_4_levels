"""
Platinum Level Orchestrator - The Collaborator
Coordinates: Watch → Plan → Approve → Multi-Agent Execute → Feedback → Learn
"""

import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from agent.gold_planner import process_task_with_learning
from agent.platinum_executor import process_approved_tasks
from agent.feedback_processor import process_feedback_forms
from agent.learning_engine import calculate_performance_metrics

BASE_DIR = Path(__file__).resolve().parent.parent
NEEDS_ACTION = BASE_DIR / "Needs_Action"
APPROVALS = BASE_DIR / "Approvals"
FEEDBACK = BASE_DIR / "Feedback"
COLLABORATION_LOGS = BASE_DIR / "Collaboration_Logs"
COLLABORATION_LOGS.mkdir(exist_ok=True)


class PlatinumHandler(FileSystemEventHandler):
    """Handles file system events for Platinum level workflow"""

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # New task in Needs_Action
        if file_path.parent == NEEDS_ACTION and file_path.suffix == ".md":
            print(f"\n📥 New task detected: {file_path.name}")
            time.sleep(0.5)
            process_task_with_learning(file_path)

    def on_modified(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Approval file modified
        if file_path.parent == APPROVALS and file_path.suffix == ".md":
            print(f"\n✅ Approval updated: {file_path.name}")
            time.sleep(0.5)
            process_approved_tasks()

        # Feedback file modified
        if file_path.parent == FEEDBACK and file_path.suffix == ".md":
            print(f"\n📝 Feedback updated: {file_path.name}")
            time.sleep(0.5)
            process_feedback_forms()


def run_platinum_agent():
    """Main entry point for Platinum level AI Employee"""

    print("=" * 70)
    print("🤖 PLATINUM LEVEL AI EMPLOYEE - THE COLLABORATOR")
    print("=" * 70)
    print("\nCapabilities:")
    print("  ✓ Watch for new tasks")
    print("  ✓ Generate plans using historical learning")
    print("  ✓ Request human approval")
    print("  ✓ Multi-agent collaboration")
    print("  ✓ Specialized agents (Researcher, Writer, Analyst, Coder)")
    print("  ✓ Task decomposition and delegation")
    print("  ✓ Parallel execution where possible")
    print("  ✓ Inter-agent communication")
    print("  ✓ Request feedback after execution")
    print("  ✓ Learn from feedback to improve")
    print("  ✓ Track performance metrics")
    print("\nSpecialized Agents:")
    print("  🔍 Researcher - Research, data gathering, fact-checking")
    print("  ✍️  Writer - Content creation, writing, editing")
    print("  📊 Analyst - Data analysis, insights, evaluation")
    print("  💻 Coder - Code generation, debugging, technical tasks")
    print("\nFolders:")
    print(f"  📂 Needs_Action: {NEEDS_ACTION}")
    print(f"  📂 Plans: {BASE_DIR / 'Plans'}")
    print(f"  📂 Approvals: {APPROVALS}")
    print(f"  📂 Done: {BASE_DIR / 'Done'}")
    print(f"  📂 Logs: {BASE_DIR / 'Logs'}")
    print(f"  📂 Collaboration_Logs: {COLLABORATION_LOGS}")
    print(f"  📂 Feedback: {FEEDBACK}")
    print(f"  📂 Memory: {BASE_DIR / 'Memory'}")

    # Show current performance metrics
    print("\n" + "=" * 70)
    metrics = calculate_performance_metrics()
    if metrics:
        print("📊 Current Performance Metrics:")
        print(f"  Tasks with Feedback: {metrics['total_tasks_with_feedback']}")
        print(f"  Average Rating: {metrics['average_rating']}/5")
        print(f"  Plan Quality: {metrics['plan_quality_success_rate']}%")
        print(f"  Execution Quality: {metrics['execution_quality_success_rate']}%")
    else:
        print("📊 No performance data yet - ready to learn!")

    print("\n" + "=" * 70)
    print("👀 Watching for tasks, approvals, and feedback...")
    print("=" * 70 + "\n")

    # Process any existing items first
    process_approved_tasks()
    process_feedback_forms()

    # Start watching
    observer = Observer()
    handler = PlatinumHandler()

    observer.schedule(handler, NEEDS_ACTION, recursive=False)
    observer.schedule(handler, APPROVALS, recursive=False)
    observer.schedule(handler, FEEDBACK, recursive=False)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down Platinum AI Employee...")
        observer.stop()

    observer.join()
    print("👋 Goodbye!")


if __name__ == "__main__":
    run_platinum_agent()
