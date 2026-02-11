"""
Silver Level Orchestrator - The Executor
Coordinates the complete workflow: Watch → Plan → Approve → Execute
"""

import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from agent.bronze_planner import process_task
from agent.silver_executor import process_approved_tasks

BASE_DIR = Path(__file__).resolve().parent.parent
NEEDS_ACTION = BASE_DIR / "Needs_Action"
APPROVALS = BASE_DIR / "Approvals"


class SilverHandler(FileSystemEventHandler):
    """Handles file system events for Silver level workflow"""

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # New task in Needs_Action
        if file_path.parent == NEEDS_ACTION and file_path.suffix == ".md":
            print(f"\n📥 New task detected: {file_path.name}")
            time.sleep(0.5)  # Wait for file to be written
            process_task(file_path)

    def on_modified(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Approval file modified
        if file_path.parent == APPROVALS and file_path.suffix == ".md":
            print(f"\n✅ Approval updated: {file_path.name}")
            time.sleep(0.5)
            process_approved_tasks()


def run_silver_agent():
    """Main entry point for Silver level AI Employee"""

    print("=" * 60)
    print("🤖 SILVER LEVEL AI EMPLOYEE - THE EXECUTOR")
    print("=" * 60)
    print("\nCapabilities:")
    print("  ✓ Watch for new tasks")
    print("  ✓ Generate execution plans")
    print("  ✓ Request human approval")
    print("  ✓ Execute approved tasks")
    print("  ✓ Track task history")
    print("  ✓ Log execution results")
    print("\nFolders:")
    print(f"  📂 Needs_Action: {NEEDS_ACTION}")
    print(f"  📂 Plans: {BASE_DIR / 'Plans'}")
    print(f"  📂 Approvals: {APPROVALS}")
    print(f"  📂 Done: {BASE_DIR / 'Done'}")
    print(f"  📂 Logs: {BASE_DIR / 'Logs'}")
    print("\n" + "=" * 60)
    print("👀 Watching for tasks and approvals...")
    print("=" * 60 + "\n")

    # Process any existing approved tasks first
    process_approved_tasks()

    # Start watching
    observer = Observer()
    handler = SilverHandler()

    observer.schedule(handler, NEEDS_ACTION, recursive=False)
    observer.schedule(handler, APPROVALS, recursive=False)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down Silver AI Employee...")
        observer.stop()

    observer.join()
    print("👋 Goodbye!")


if __name__ == "__main__":
    run_silver_agent()
