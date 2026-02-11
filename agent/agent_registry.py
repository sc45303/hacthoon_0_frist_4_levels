"""
Platinum Level - Agent Registry
Manages different types of specialized agents
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AgentInfo:
    """Information about a registered agent"""
    agent_id: str
    agent_type: str
    capabilities: List[str]
    status: str  # 'idle', 'busy', 'offline'
    current_task: Optional[str] = None
    registered_at: str = None

class AgentRegistry:
    """Central registry for all agents in the system"""

    def __init__(self):
        self.agents: Dict[str, AgentInfo] = {}

    def register_agent(self, agent_id: str, agent_type: str, capabilities: List[str]):
        """Register a new agent"""
        agent_info = AgentInfo(
            agent_id=agent_id,
            agent_type=agent_type,
            capabilities=capabilities,
            status='idle',
            registered_at=datetime.now().isoformat()
        )
        self.agents[agent_id] = agent_info
        print(f"✅ Registered {agent_type} agent: {agent_id}")

    def get_agent(self, agent_id: str) -> Optional[AgentInfo]:
        """Get agent information"""
        return self.agents.get(agent_id)

    def find_agents_by_capability(self, capability: str) -> List[AgentInfo]:
        """Find all agents with a specific capability"""
        return [
            agent for agent in self.agents.values()
            if capability in agent.capabilities and agent.status == 'idle'
        ]

    def find_agents_by_type(self, agent_type: str) -> List[AgentInfo]:
        """Find all agents of a specific type"""
        return [
            agent for agent in self.agents.values()
            if agent.agent_type == agent_type
        ]

    def update_agent_status(self, agent_id: str, status: str, current_task: Optional[str] = None):
        """Update agent status"""
        if agent_id in self.agents:
            self.agents[agent_id].status = status
            self.agents[agent_id].current_task = current_task

    def get_available_agents(self) -> List[AgentInfo]:
        """Get all idle agents"""
        return [agent for agent in self.agents.values() if agent.status == 'idle']

    def list_all_agents(self) -> List[AgentInfo]:
        """List all registered agents"""
        return list(self.agents.values())

# Global registry instance
_registry = AgentRegistry()

def get_registry() -> AgentRegistry:
    """Get the global agent registry"""
    return _registry
