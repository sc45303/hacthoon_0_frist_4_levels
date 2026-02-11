"""
Personal AI Employee - Main Entry Point
Run this to start your AI Employee at the current level
"""

import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Import available levels
from agent.silver_orchestrator import run_silver_agent
from agent.gold_orchestrator import run_gold_agent
from agent.platinum_orchestrator import run_platinum_agent

# Configuration - Change this to switch levels
CURRENT_LEVEL = "platinum"  # Options: "silver", "gold", "platinum"

if __name__ == "__main__":
    print("\n🚀 Starting Personal AI Employee...\n")

    if CURRENT_LEVEL == "platinum":
        run_platinum_agent()
    elif CURRENT_LEVEL == "gold":
        run_gold_agent()
    elif CURRENT_LEVEL == "silver":
        run_silver_agent()
    else:
        print(f"❌ Unknown level: {CURRENT_LEVEL}")
        print("Available levels: silver, gold, platinum")
