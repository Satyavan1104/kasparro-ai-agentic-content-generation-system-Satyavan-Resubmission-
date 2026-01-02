"""
Competitor Agent

Autonomous agent that generates fictional competitor product data.
"""

from __future__ import annotations

import asyncio
import random
from typing import Any, Dict, List, Optional

from framework import (
    AutonomousAgent, AgentCapability, Message, MessageType, AgentState
)


class RivalCreationAgent(AutonomousAgent):
    """Autonomous agent that generates competitor data"""
    
    def __init__(self, message_bus):
        super().__init__("RivalCreationAgent", message_bus)
        self.generated_competitors: List[Dict[str, Any]] = []
    
    def get_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="generate_competitor",
                description="Generate fictional competitor product data",
                input_types=["parsed_product", "coordination_request"],
                output_types=["competitor_product", "product_b"],
                can_initiate=False,
                can_coordinate=True
            )
        ]
    
    async def process_message(self, message: Message) -> Optional[Message]:
        if message.message_type == MessageType.COORDINATION_REQUEST:
            action = message.payload.get("action")
            
            if action == "generate_competitor":
                product_data = message.payload.get("product_data")
                competitor = await self._generate_competitor(product_data)
                
                self.generated_competitors.append(competitor)
                self.update_knowledge("latest_competitor", competitor)
                self.update_knowledge("competitor_generated", True)
                
                # Notify content agent that competitor is ready
                await self._notify_competitor_ready(competitor)
                
                return Message(
                    sender=self.name,
                    receiver=message.sender,
                    message_type=MessageType.COORDINATION_RESPONSE,
                    payload={
                        "status": "completed",
                        "competitor": competitor
                    }
                )
        
        elif message.message_type == MessageType.DATA_REQUEST:
            if message.payload.get("request") == "latest_competitor":
                competitor = self.get_knowledge("latest_competitor")
                if competitor:
                    return Message(
                        sender=self.name,
                        receiver=message.sender,
                        message_type=MessageType.DATA_RESPONSE,
                        payload={"competitor": competitor},
                        correlation_id=message.correlation_id
                    )
        
        return None
    
    async def decide_next_action(self) -> Optional[Message]:
        if self.generated_competitors and not self.get_knowledge("notified_content_agent_competitor"):
            return Message(
                sender=self.name,
                receiver="ContentGeneratorAgent",
                message_type=MessageType.COORDINATION_REQUEST,
                payload={
                    "action": "competitor_ready",
                    "competitor": self.get_knowledge("latest_competitor")
                }
            )
        
        return None
    
    async def _generate_competitor(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a fictional competitor product"""
        await asyncio.sleep(0.15)  # Simulate processing time
        
        competitor_names = ["RadiancePlus", "VitaGlow", "Luminex", "BrightenUp"]
        competitor_ingredients = ["Vitamin E", "Niacinamide", "Retinol", "Peptides"]
        
        competitor = {
            "id": "competitor_1",
            "name": random.choice(competitor_names) + " Vitamin C Serum",
            "concentration": "15% Vitamin C",
            "skin_types": ["All Skin Types"],
            "key_ingredients": ["Vitamin C", random.choice(competitor_ingredients), "Antioxidants"],
            "benefits": ["Anti-aging", "Brightening", "Hydration"],
            "usage_instructions": "Apply 4-5 drops in the evening before moisturizer",
            "side_effects": "May cause sensitivity for first-time users",
            "price": "₹899",
            "category": "Serum"
        }
        
        return competitor
    
    async def _notify_competitor_ready(self, competitor: Dict[str, Any]) -> None:
        """Notify other agents that competitor is ready"""
        self.update_knowledge("notified_content_agent_competitor", True)
        
        # Immediately notify content generator
        message = Message(
            sender=self.name,
            receiver="PageAssemblyAgent",
            message_type=MessageType.COORDINATION_REQUEST,
            payload={
                "action": "competitor_ready",
                "competitor": competitor
            }
        )
        await self.send_message(message)
