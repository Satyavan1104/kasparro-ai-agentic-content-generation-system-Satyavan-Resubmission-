"""
Workflow Coordinator

Coordinates multi-agent workflows through message passing.
"""

import asyncio
import time
from typing import Any, Dict

from .message_hub import MessageHub
from .communication_messages import Message, MessageType
from .agent_registry import agent_registry


class WorkflowCoordinator:
    """Coordinates multi-agent workflows through message passing"""
    
    def __init__(self, message_bus: MessageHub):
        self.message_bus = message_bus
        self.agents = agent_registry._agents  # Access registered agents
        self.workflow_goals: List[Dict[str, Any]] = []
        self.workflow_state: Dict[str, Any] = {}
    
    def register_agent(self, agent) -> None:
        """Register an agent with the orchestrator"""
        agent_registry.register(agent)
        
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
