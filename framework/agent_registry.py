"""
Agent Registry

Manages registration and discovery of agents in the system.
"""

from typing import Dict, List, Optional

from .autonomous_agent import AutonomousAgent


class AgentRegistry:
    """Registry for managing available agents"""
    
    def __init__(self):
        self._agents: Dict[str, AutonomousAgent] = {}
    
    def register(self, agent: AutonomousAgent) -> None:
        """Register an agent"""
        self._agents[agent.name] = agent
    
    def get_agent(self, name: str) -> Optional[AutonomousAgent]:
        """Get agent by name"""
        return self._agents.get(name)
    
    def list_agents(self) -> List[str]:
        """List all registered agent names"""
        return list(self._agents.keys())
    
    def get_all_capabilities(self) -> Dict[str, Dict[str, str]]:
        """Get capabilities of all registered agents"""
        return {name: agent.get_capabilities() for name, agent in self._agents.items()}


# Global agent registry instance
agent_registry = AgentRegistry()
