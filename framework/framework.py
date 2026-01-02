"""
Multi-Agent System Framework

Implements a true multi-agent system with:
- Message passing between agents
- Dynamic agent coordination
- Agent autonomy and decision-making
- Emergent workflow behavior
"""

from __future__ import annotations

import asyncio
import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from uuid import uuid4


class MessageType(Enum):
    """Types of messages between agents"""
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    DATA_REQUEST = "data_request"
    DATA_RESPONSE = "data_response"
    COORDINATION_REQUEST = "coordination_request"
    COORDINATION_RESPONSE = "coordination_response"
    STATUS_UPDATE = "status_update"
    WORKFLOW_COMPLETE = "workflow_complete"


class AgentState(Enum):
    """Agent execution states"""
    IDLE = "idle"
    PROCESSING = "processing"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Message:
    """Message passed between agents"""
    id: str = field(default_factory=lambda: str(uuid4()))
    sender: str = ""
    receiver: str = ""
    message_type: MessageType = MessageType.TASK_REQUEST
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    correlation_id: Optional[str] = None  # For request-response pairs
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "message_type": self.message_type.value,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id
        }


@dataclass
class AgentCapability:
    """Defines what an agent can do"""
    name: str
    description: str
    input_types: List[str]
    output_types: List[str]
    can_initiate: bool = True  # Can start workflows
    can_coordinate: bool = False  # Can coordinate other agents


class MessageBus:
    """Central message bus for agent communication"""
    
    def __init__(self):
        self._queues: Dict[str, List[Message]] = {}
        self._subscribers: Dict[str, Set[str]] = {}  # topic -> agents
        self._message_log: List[Message] = []
    
    def subscribe(self, agent_name: str, topic: str = "*") -> None:
        """Subscribe agent to messages (topic or all)"""
        if topic not in self._subscribers:
            self._subscribers[topic] = set()
        self._subscribers[topic].add(agent_name)
    
    def unsubscribe(self, agent_name: str, topic: str = "*") -> None:
        """Unsubscribe agent from messages"""
        if topic in self._subscribers:
            self._subscribers[topic].discard(agent_name)
    
    def send(self, message: Message) -> None:
        """Send message to specific agent"""
        if message.receiver not in self._queues:
            self._queues[message.receiver] = []
        self._queues[message.receiver].append(message)
        self._message_log.append(message)
    
    def broadcast(self, sender: str, message_type: MessageType, payload: Dict[str, Any]) -> None:
        """Broadcast message to all subscribers"""
        message = Message(
            sender=sender,
            receiver="broadcast",
            message_type=message_type,
            payload=payload
        )
        
        # Send to all subscribers of this message type
        topic = message_type.value
        recipients = self._subscribers.get(topic, set())
        recipients.update(self._subscribers.get("*", set()))  # Also send to universal subscribers
        
        for recipient in recipients:
            if recipient != sender:  # Don't send to self
                msg = Message(
                    sender=sender,
                    receiver=recipient,
                    message_type=message_type,
                    payload=payload
                )
                self.send(msg)
    
    def receive(self, agent_name: str) -> List[Message]:
        """Get all messages for an agent"""
        messages = self._queues.get(agent_name, [])
        self._queues[agent_name] = []
        return messages
    
    def get_message_log(self) -> List[Dict[str, Any]]:
        """Get log of all messages"""
        return [msg.to_dict() for msg in self._message_log]


class AutonomousAgent(ABC):
    """Base class for autonomous agents with decision-making capabilities"""
    
    def __init__(self, name: str, message_bus: MessageBus):
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


class WorkflowOrchestrator:
    """Coordinates multi-agent workflows through message passing"""
    
    def __init__(self, message_bus: MessageBus):
        self.message_bus = message_bus
        self.agents: Dict[str, AutonomousAgent] = {}
        self.workflow_goals: List[Dict[str, Any]] = []
        self.workflow_state: Dict[str, Any] = {}
    
    def register_agent(self, agent: AutonomousAgent) -> None:
        """Register an agent with the orchestrator"""
        self.agents[agent.name] = agent
        
        # Log agent capabilities
        capabilities = [cap.name for cap in agent.get_capabilities()]
        print(f"Registered agent: {agent.name} with capabilities: {capabilities}")
    
    async def start_workflow(self, goal: Dict[str, Any]) -> None:
        """Start a new workflow by broadcasting goal to capable agents"""
        self.workflow_goals.append(goal)
        self.workflow_state["current_goal"] = goal
        self.workflow_state["status"] = "running"
        
        # Find agents that can initiate this type of work
        capable_agents = []
        for agent in self.agents.values():
            for cap in agent.get_capabilities():
                if cap.can_initiate and goal.get("type") in cap.input_types:
                    capable_agents.append(agent.name)
                    break
        
        # Send task request to capable agents
        for agent_name in capable_agents:
            message = Message(
                sender="orchestrator",
                receiver=agent_name,
                message_type=MessageType.TASK_REQUEST,
                payload=goal
            )
            self.message_bus.send(message)
    
    async def run_workflow(self, goal: Dict[str, Any], timeout: float = 30.0) -> Dict[str, Any]:
        """Run workflow and wait for completion"""
        await self.start_workflow(goal)
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Check for workflow completion messages
            messages = self.message_bus.receive("orchestrator")
            for message in messages:
                if message.message_type == MessageType.WORKFLOW_COMPLETE:
                    return message.payload
            
            await asyncio.sleep(0.5)
        
        return {"status": "timeout", "error": "Workflow did not complete in time"}
    
    async def run_all_agents(self) -> None:
        """Run all registered agents concurrently"""
        tasks = [agent.run() for agent in self.agents.values()]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    def get_system_state(self) -> Dict[str, Any]:
        """Get current state of the multi-agent system"""
        return {
            "agents": {
                name: {
                    "state": agent.state.value,
                    "capabilities": [cap.name for cap in agent.get_capabilities()],
                    "active_tasks": len(agent.active_tasks),
                    "completed_tasks": len(agent.completed_tasks),
                    "knowledge_keys": list(agent.knowledge_base.keys())
                }
                for name, agent in self.agents.items()
            },
            "workflow_state": self.workflow_state,
            "message_log": self.message_bus.get_message_log()[-10:]  # Last 10 messages
        }
