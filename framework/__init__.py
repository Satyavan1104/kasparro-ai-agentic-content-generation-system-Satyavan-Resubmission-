"""
Core Framework Package

Contains the core multi-agent framework components.
"""

from .autonomous_agent import AutonomousAgent, AgentCapability
from .communication_messages import Message, MessageType, AgentState
from .message_hub import MessageHub
from .agent_registry import AgentRegistry
from .workflow_coordinator import WorkflowCoordinator

__all__ = [
    "AutonomousAgent",
    "AgentCapability", 
    "Message",
    "MessageType",
    "AgentState",
    "MessageHub",
    "AgentRegistry",
    "WorkflowCoordinator"
]
