"""
Product Data Agent

Autonomous agent that parses product data and decides when to coordinate with other agents.
"""

from __future__ import annotations

import asyncio
import random
from typing import Any, Dict, List, Optional

from framework import (
    AutonomousAgent, AgentCapability, Message, MessageType, AgentState
)


class ProductDataAgent(AutonomousAgent):
    """Autonomous agent that parses product data and decides when to coordinate"""
    
    def __init__(self, message_bus):
        super().__init__("ProductDataAgent", message_bus)
        self.parsed_products: List[Dict[str, Any]] = []
    
    def get_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="parse_product_data",
                description="Parse raw product data into structured format",
                input_types=["raw_product_data", "product_dataset"],
                output_types=["parsed_product", "structured_product"],
                can_initiate=True,
                can_coordinate=False
            ),
            AgentCapability(
                name="validate_data",
                description="Validate parsed product data",
                input_types=["parsed_product"],
                output_types=["validation_result"],
                can_initiate=False,
                can_coordinate=False
            )
        ]
    
    async def process_message(self, message: Message) -> Optional[Message]:
        """Process incoming messages and decide on responses"""
        if message.message_type == MessageType.TASK_REQUEST:
            task_type = message.payload.get("type")
            
            if task_type in ["raw_product_data", "product_dataset"]:
                # Parse the product data
                raw_data = message.payload.get("data")
                parsed_product = await self._parse_product_data(raw_data)
                
                # Store in knowledge base
                self.update_knowledge("latest_parsed_product", parsed_product)
                self.parsed_products.append(parsed_product)
                
                # Decide what to do next - coordinate with other agents
                await self._coordinate_next_steps(parsed_product)
                
                return Message(
                    sender=self.name,
                    receiver=message.sender,
                    message_type=MessageType.TASK_RESPONSE,
                    payload={
                        "status": "completed",
                        "parsed_product": parsed_product,
                        "product_id": parsed_product.get("id")
                    },
                    correlation_id=message.correlation_id
                )
        
        elif message.message_type == MessageType.DATA_REQUEST:
            # Another agent is asking for parsed data
            requested_data = message.payload.get("request")
            
            if requested_data == "latest_product":
                latest = self.get_knowledge("latest_parsed_product")
                if latest:
                    return Message(
                        sender=self.name,
                        receiver=message.sender,
                        message_type=MessageType.DATA_RESPONSE,
                        payload={"parsed_product": latest},
                        correlation_id=message.correlation_id
                    )
        
        return None
    
    async def decide_next_action(self) -> Optional[Message]:
        """Decide what to do next based on current state"""
        # If we have parsed data but haven't generated questions yet
        if len(self.parsed_products) > 0 and not self.get_knowledge("questions_generated"):
            # Request question generation
            return Message(
                sender=self.name,
                receiver="QueryGenerationAgent",
                message_type=MessageType.COORDINATION_REQUEST,
                payload={
                    "action": "generate_questions",
                    "product_data": self.get_knowledge("latest_parsed_product")
                }
            )
        
        # If we have parsed data but no competitor yet
        if len(self.parsed_products) > 0 and not self.get_knowledge("competitor_generated"):
            # Request competitor generation
            return Message(
                sender=self.name,
                receiver="RivalCreationAgent", 
                message_type=MessageType.COORDINATION_REQUEST,
                payload={
                    "action": "generate_competitor",
                    "product_data": self.get_knowledge("latest_parsed_product")
                }
            )
        
        return None
    
    async def _parse_product_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse raw product data into structured format"""
        await asyncio.sleep(0.1)  # Simulate processing time
        
        # Extract and clean data
        parsed = {
            "id": f"product_{len(self.parsed_products) + 1}",
            "name": raw_data.get("Product Name", "").strip(),
            "concentration": raw_data.get("Concentration", "").strip(),
            "skin_types": self._parse_list(raw_data.get("Skin Type", "")),
            "key_ingredients": self._parse_list(raw_data.get("Key Ingredients", "")),
            "benefits": self._parse_list(raw_data.get("Benefits", "")),
            "usage_instructions": raw_data.get("How to Use", "").strip(),
            "side_effects": raw_data.get("Side Effects", "").strip(),
            "price": raw_data.get("Price", "").strip(),
            "category": self._infer_category(raw_data.get("Product Name", "")),
        }
        
        return parsed
    
    async def _coordinate_next_steps(self, parsed_product: Dict[str, Any]) -> None:
        """Coordinate with other agents for next steps"""
        # This agent decides what needs to happen next
        # and coordinates with other agents autonomously
        
        # Mark that we have parsed data
        self.update_knowledge("has_parsed_data", True)
        
        # Only coordinate if we haven't already done so
        if not self.get_knowledge("coordinated_questions"):
            # Request question generation
            question_msg = Message(
                sender=self.name,
                receiver="QueryGenerationAgent",
                message_type=MessageType.COORDINATION_REQUEST,
                payload={
                    "action": "generate_questions",
                    "product_data": parsed_product
                }
            )
            await self.send_message(question_msg)
            self.update_knowledge("coordinated_questions", True)
        
        if not self.get_knowledge("coordinated_competitor"):
            # Request competitor generation
            competitor_msg = Message(
                sender=self.name,
                receiver="RivalCreationAgent", 
                message_type=MessageType.COORDINATION_REQUEST,
                payload={
                    "action": "generate_competitor",
                    "product_data": parsed_product
                }
            )
            await self.send_message(competitor_msg)
            self.update_knowledge("coordinated_competitor", True)
    
    def _parse_list(self, text: str) -> List[str]:
        """Parse comma-separated lists"""
        if not text:
            return []
        
        import re
        items = re.split(r'[,，|]\s*|\s+and\s+|\s*[-–—]\s*', text)
        return [item.strip() for item in items if item.strip() and len(item.strip()) > 1]
    
    def _infer_category(self, product_name: str) -> str:
        """Infer product category from name"""
        name_lower = product_name.lower()
        if "serum" in name_lower:
            return "Serum"
        elif "cream" in name_lower:
            return "Cream"
        elif "lotion" in name_lower:
            return "Lotion"
        elif "oil" in name_lower:
            return "Oil"
        else:
            return "Skincare"
