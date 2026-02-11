import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_FILE = BASE_DIR / "Memory" / "task_history.json"

def load_memory():
    if not MEMORY_FILE.exists():
        return {"tasks": []}
    return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))

def save_memory(memory):
    MEMORY_FILE.write_text(
        json.dumps(memory, indent=2),
        encoding="utf-8"
    )

def add_task_to_memory(task_name, task_text, plan):
    memory = load_memory()

    memory["tasks"].append({
        "task": task_name,
        "content": task_text,
        "plan": plan,
        "status": "planned",
        "timestamp": datetime.now().isoformat()
    })

    save_memory(memory)
