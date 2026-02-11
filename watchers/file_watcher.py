import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

# Get absolute path safely
BASE_DIR = Path(__file__).resolve().parent.parent
WATCH_FOLDER = BASE_DIR / "Needs_Action"


class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        task_path = Path(event.src_path)

        if task_path.suffix != ".md":
            return

        task_text = task_path.read_text(encoding="utf-8").strip()

        if not task_text:
            return  # ignore empty saves

        print(f"📥 Task ready: {task_path.name}")
        print("📄 Task content:")
        print(task_text)

    def on_created(self, event):
        if event.is_directory:
            return

        task_path = Path(event.src_path)
        print(f"📥 New task detected: {task_path.name}")

        # Wait briefly for file to be fully written
        time.sleep(0.3)

        task_text = task_path.read_text(encoding="utf-8").strip()

        print("📄 Task content:")
        print(task_text if task_text else "[EMPTY FILE]")
if __name__ == "__main__":
    observer = Observer()
    observer.schedule(Handler(), WATCH_FOLDER, recursive=False)
    observer.start()
    print("👀 Watching Needs_Action folder...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
