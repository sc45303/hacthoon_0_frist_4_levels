"""
Platinum Level - Task Decomposer
Breaks complex tasks into subtasks for delegation
"""

from agent.gemini_brain import client
from typing import List, Dict, Any

class TaskDecomposer:
    """Decomposes complex tasks into subtasks for specialized agents"""

    def decompose_task(self, task_description: str) -> Dict[str, Any]:
        """Break down a complex task into subtasks"""

        print(f"🔨 Decomposing task: {task_description}")

        prompt = f"""
You are a Task Decomposition AI in a multi-agent system.

Available agent types:
- Researcher: Research, data gathering, fact-checking
- Writer: Content creation, writing, editing
- Analyst: Data analysis, insights, evaluation
- Coder: Code generation, debugging, technical tasks

Complex Task: {task_description}

Your job:
1. Analyze if this task needs multiple agents or just one
2. Break it down into subtasks
3. Assign each subtask to the appropriate agent type
4. Identify dependencies (which tasks must complete before others)
5. Determine which tasks can run in parallel

Respond in this JSON format:
{{
  "requires_collaboration": true/false,
  "subtasks": [
    {{
      "subtask_id": "1",
      "description": "...",
      "agent_type": "Researcher/Writer/Analyst/Coder",
      "depends_on": [],
      "can_run_parallel": true/false
    }}
  ],
  "execution_order": ["1", "2", "3"]
}}
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            result_text = response.text.strip()

            # Extract JSON from response
            import json
            import re

            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # Fallback: simple task
                result = {
                    "requires_collaboration": False,
                    "subtasks": [{
                        "subtask_id": "1",
                        "description": task_description,
                        "agent_type": "Writer",
                        "depends_on": [],
                        "can_run_parallel": True
                    }],
                    "execution_order": ["1"]
                }

            print(f"✅ Task decomposed into {len(result['subtasks'])} subtask(s)")
            return result

        except Exception as e:
            print(f"⚠️  Decomposition error: {e}")
            # Fallback to simple execution
            return {
                "requires_collaboration": False,
                "subtasks": [{
                    "subtask_id": "1",
                    "description": task_description,
                    "agent_type": "Writer",
                    "depends_on": [],
                    "can_run_parallel": True
                }],
                "execution_order": ["1"]
            }
