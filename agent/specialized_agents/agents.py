"""
Specialized Agents for Platinum Level
"""

from agent.gemini_brain import client
from agent.agent_registry import get_registry
from agent.communication_bus import get_communication_bus
from typing import Dict, Any

class BaseAgent:
    """Base class for all specialized agents"""

    def __init__(self, agent_id: str, agent_type: str, capabilities: list):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.capabilities = capabilities
        self.registry = get_registry()
        self.comm_bus = get_communication_bus()

        # Register with registry
        self.registry.register_agent(agent_id, agent_type, capabilities)

    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task - to be overridden by subclasses"""
        raise NotImplementedError

    def send_message(self, to_agent: str, message_type: str, content: Dict):
        """Send a message to another agent"""
        return self.comm_bus.send_message(
            self.agent_id, to_agent, message_type, content
        )

    def get_messages(self):
        """Get messages for this agent"""
        return self.comm_bus.get_messages_for_agent(self.agent_id)


class ResearcherAgent(BaseAgent):
    """Agent specialized in research and information gathering"""

    def __init__(self, agent_id: str = "researcher_001"):
        super().__init__(
            agent_id=agent_id,
            agent_type="Researcher",
            capabilities=["research", "data_gathering", "fact_checking", "analysis"]
        )

    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research task"""
        self.registry.update_agent_status(self.agent_id, 'busy', task.get('description'))

        print(f"🔍 {self.agent_id}: Starting research task...")

        prompt = f"""
You are a Researcher Agent in a multi-agent AI system.

Your task: {task.get('description')}

Your role:
- Gather relevant information
- Research facts and data
- Provide comprehensive findings
- Cite sources when possible

Provide detailed research findings.
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            result = {
                "agent_id": self.agent_id,
                "agent_type": self.agent_type,
                "task": task.get('description'),
                "findings": response.text.strip(),
                "status": "completed"
            }

            self.registry.update_agent_status(self.agent_id, 'idle')
            print(f"✅ {self.agent_id}: Research completed")

            return result

        except Exception as e:
            self.registry.update_agent_status(self.agent_id, 'idle')
            return {
                "agent_id": self.agent_id,
                "status": "failed",
                "error": str(e)
            }


class WriterAgent(BaseAgent):
    """Agent specialized in content writing and creation"""

    def __init__(self, agent_id: str = "writer_001"):
        super().__init__(
            agent_id=agent_id,
            agent_type="Writer",
            capabilities=["writing", "content_creation", "editing", "storytelling"]
        )

    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute writing task"""
        self.registry.update_agent_status(self.agent_id, 'busy', task.get('description'))

        print(f"✍️  {self.agent_id}: Starting writing task...")

        # Check if there's research data from other agents
        research_data = task.get('research_data', '')

        prompt = f"""
You are a Writer Agent in a multi-agent AI system.

Your task: {task.get('description')}

{f"Research data provided: {research_data}" if research_data else ""}

Your role:
- Create engaging, well-structured content
- Write clearly and professionally
- Adapt tone to the audience
- Ensure coherence and flow

Provide the written content.
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            result = {
                "agent_id": self.agent_id,
                "agent_type": self.agent_type,
                "task": task.get('description'),
                "content": response.text.strip(),
                "status": "completed"
            }

            self.registry.update_agent_status(self.agent_id, 'idle')
            print(f"✅ {self.agent_id}: Writing completed")

            return result

        except Exception as e:
            self.registry.update_agent_status(self.agent_id, 'idle')
            return {
                "agent_id": self.agent_id,
                "status": "failed",
                "error": str(e)
            }


class AnalystAgent(BaseAgent):
    """Agent specialized in data analysis and insights"""

    def __init__(self, agent_id: str = "analyst_001"):
        super().__init__(
            agent_id=agent_id,
            agent_type="Analyst",
            capabilities=["analysis", "data_interpretation", "insights", "evaluation"]
        )

    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analysis task"""
        self.registry.update_agent_status(self.agent_id, 'busy', task.get('description'))

        print(f"📊 {self.agent_id}: Starting analysis task...")

        data_to_analyze = task.get('data', '')

        prompt = f"""
You are an Analyst Agent in a multi-agent AI system.

Your task: {task.get('description')}

{f"Data to analyze: {data_to_analyze}" if data_to_analyze else ""}

Your role:
- Analyze data and information
- Identify patterns and trends
- Provide actionable insights
- Make recommendations

Provide detailed analysis and insights.
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            result = {
                "agent_id": self.agent_id,
                "agent_type": self.agent_type,
                "task": task.get('description'),
                "analysis": response.text.strip(),
                "status": "completed"
            }

            self.registry.update_agent_status(self.agent_id, 'idle')
            print(f"✅ {self.agent_id}: Analysis completed")

            return result

        except Exception as e:
            self.registry.update_agent_status(self.agent_id, 'idle')
            return {
                "agent_id": self.agent_id,
                "status": "failed",
                "error": str(e)
            }


class CoderAgent(BaseAgent):
    """Agent specialized in code generation and technical tasks"""

    def __init__(self, agent_id: str = "coder_001"):
        super().__init__(
            agent_id=agent_id,
            agent_type="Coder",
            capabilities=["coding", "debugging", "code_review", "technical_writing"]
        )

    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute coding task"""
        self.registry.update_agent_status(self.agent_id, 'busy', task.get('description'))

        print(f"💻 {self.agent_id}: Starting coding task...")

        specifications = task.get('specifications', '')

        prompt = f"""
You are a Coder Agent in a multi-agent AI system.

Your task: {task.get('description')}

{f"Specifications: {specifications}" if specifications else ""}

Your role:
- Write clean, efficient code
- Follow best practices
- Add comments where needed
- Ensure code quality

Provide the code solution.
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            result = {
                "agent_id": self.agent_id,
                "agent_type": self.agent_type,
                "task": task.get('description'),
                "code": response.text.strip(),
                "status": "completed"
            }

            self.registry.update_agent_status(self.agent_id, 'idle')
            print(f"✅ {self.agent_id}: Coding completed")

            return result

        except Exception as e:
            self.registry.update_agent_status(self.agent_id, 'idle')
            return {
                "agent_id": self.agent_id,
                "status": "failed",
                "error": str(e)
            }
