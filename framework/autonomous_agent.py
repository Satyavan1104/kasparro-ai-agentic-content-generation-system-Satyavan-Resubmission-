"""
Base Agent Class

Defines the autonomous agent interface and common functionality.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .communication_messages import Message, MessageType, AgentState


class AgentCapability:
    """Defines what an agent can do"""
    def __init__(self, name: str, description: str, input_types: List[str], 
                 output_types: List[str], can_initiate: bool = True, can_coordinate: bool = False):
        self.name = name
        self.description = description
        self.input_types = input_types
        self.output_types = output_types
        self.can_initiate = can_initiate
        self.can_coordinate = can_coordinate


class AutonomousAgent(ABC):
    """Base class for autonomous agents with decision-making capabilities"""
    
    def __init__(self, name: str, message_bus):
        self.name = name
        self.state = AgentState.IDLE
        self.message_bus = message_bus
        self.capabilities: List[AgentCapability] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.active_tasks: List[str] = []
        self.completed_tasks: List[str] = []
        
        # Subscribe to relevant message types
        self.message_bus.subscribe(self.name, "*")
    
    @abstractmethod
    def get_capabilities(self) -> List[AgentCapability]:
        """Define what this agent can do"""
        pass
    
    @abstractmethod
    async def process_message(self, message: Message) -> Optional[Message]:
        """Process incoming message and optionally return response"""
        pass
    
    @abstractmethod
    async def decide_next_action(self) -> Optional[Message]:
        """Decide what to do next based on current state and knowledge"""
        pass
    
    async def run(self) -> None:
        """Main agent loop - runs autonomously"""
        self.state = AgentState.PROCESSING
        
        while self.state in [AgentState.PROCESSING, AgentState.WAITING]:
            # Process incoming messages
            messages = self.message_bus.receive(self.name)
            for message in messages:
                await self.handle_message(message)
            
            # Decide on next action
            if self.state == AgentState.PROCESSING:
                next_action = await self.decide_next_action()
                if next_action:
                    await self.send_message(next_action)
                else:
                    # No more work to do
                    if len(self.active_tasks) == 0:
                        self.state = AgentState.IDLE
                        break
                    else:
                        self.state = AgentState.WAITING
            
            # Small delay to prevent busy waiting
            import asyncio
            await asyncio.sleep(0.1)
    
    async def handle_message(self, message: Message) -> None:
        """Handle incoming message"""
        try:
            response = await self.process_message(message)
            if response:
                await self.send_message(response)
        except Exception as e:
            # Send error response
            error_response = Message(
                sender=self.name,
                receiver=message.sender,
                message_type=MessageType.STATUS_UPDATE,
                payload={
                    "status": "error",
                    "error": str(e),
                    "correlation_id": message.correlation_id
                },
                correlation_id=message.correlation_id
            )
            await self.send_message(error_response)
    
    async def send_message(self, message: Message) -> None:
        """Send message to another agent"""
        self.message_bus.send(message)
    
    def update_knowledge(self, key: str, value: Any) -> None:
        """Update agent's knowledge base"""
        self.knowledge_base[key] = value
    
    def get_knowledge(self, key: str) -> Any:
        """Get knowledge from agent's knowledge base"""
        return self.knowledge_base.get(key)
