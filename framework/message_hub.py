"""
Message Hub (Blackboard Pattern)

Central message passing system for agent communication.
"""

from typing import Dict, List, Set, Optional

from .communication_messages import Message


class MessageHub:
    """Central message bus for agent communication using Blackboard pattern"""
    
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
    
    def broadcast(self, sender: str, message_type, payload: Dict[str, str]) -> None:
        """Broadcast message to all subscribers"""
        from .messages import MessageType
        
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
    
    def get_message_log(self) -> List[Dict[str, str]]:
        """Get log of all messages"""
        return [msg.to_dict() for msg in self._message_log]
