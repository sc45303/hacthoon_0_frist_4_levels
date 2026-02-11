"""
Platinum Level - Communication Bus
Enables inter-agent messaging and coordination
"""

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
from queue import Queue
import json

@dataclass
class Message:
    """Message structure for inter-agent communication"""
    message_id: str
    from_agent: str
    to_agent: str
    message_type: str  # 'request', 'response', 'notification', 'broadcast'
    content: Dict
    timestamp: str
    reply_to: Optional[str] = None

class CommunicationBus:
    """Central message bus for agent communication"""

    def __init__(self):
        self.message_queue: Queue = Queue()
        self.message_history: List[Message] = []
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_counter = 0

    def send_message(self, from_agent: str, to_agent: str, message_type: str,
                     content: Dict, reply_to: Optional[str] = None) -> str:
        """Send a message from one agent to another"""
        self.message_counter += 1
        message_id = f"msg_{self.message_counter}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        message = Message(
            message_id=message_id,
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            content=content,
            timestamp=datetime.now().isoformat(),
            reply_to=reply_to
        )

        self.message_queue.put(message)
        self.message_history.append(message)

        print(f"📨 Message sent: {from_agent} → {to_agent} ({message_type})")

        return message_id

    def broadcast_message(self, from_agent: str, message_type: str, content: Dict) -> str:
        """Broadcast a message to all agents"""
        return self.send_message(from_agent, "ALL", message_type, content)

    def get_messages_for_agent(self, agent_id: str) -> List[Message]:
        """Get all messages for a specific agent"""
        messages = []
        temp_queue = Queue()

        while not self.message_queue.empty():
            msg = self.message_queue.get()
            if msg.to_agent == agent_id or msg.to_agent == "ALL":
                messages.append(msg)
            else:
                temp_queue.put(msg)

        # Put back messages not for this agent
        while not temp_queue.empty():
            self.message_queue.put(temp_queue.get())

        return messages

    def get_conversation(self, agent1: str, agent2: str) -> List[Message]:
        """Get conversation history between two agents"""
        return [
            msg for msg in self.message_history
            if (msg.from_agent == agent1 and msg.to_agent == agent2) or
               (msg.from_agent == agent2 and msg.to_agent == agent1)
        ]

    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        """Get a specific message by ID"""
        for msg in self.message_history:
            if msg.message_id == message_id:
                return msg
        return None

    def clear_messages(self):
        """Clear all messages"""
        self.message_queue = Queue()
        self.message_history = []
        print("🧹 Message bus cleared")

# Global communication bus instance
_bus = CommunicationBus()

def get_communication_bus() -> CommunicationBus:
    """Get the global communication bus"""
    return _bus
