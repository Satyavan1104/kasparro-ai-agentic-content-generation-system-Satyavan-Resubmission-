"""
Content Generator Agent

Autonomous agent that generates content pages when it has all required data.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

from framework import (
    AutonomousAgent, AgentCapability, Message, MessageType, AgentState
)


class PageAssemblyAgent(AutonomousAgent):
    """Autonomous agent that generates content when it has all required data"""
    
    def __init__(self, message_bus):
        super().__init__("PageAssemblyAgent", message_bus)
        self.generated_pages: List[Dict[str, Any]] = []
        self.required_data = {
            "product_data": False,
            "questions": False,
            "competitor": False
        }
    
    def get_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="generate_content",
                description="Generate structured pages from product data",
                input_types=["coordination_request", "data_response"],
                output_types=["faq_page", "product_page", "comparison_page"],
                can_initiate=False,
                can_coordinate=True
            )
        ]
    
    async def process_message(self, message: Message) -> Optional[Message]:
        """Process incoming messages and decide on responses"""
        if message.message_type == MessageType.COORDINATION_REQUEST:
            action = message.payload.get("action")
            
            if action == "questions_ready":
                self.required_data["questions"] = True
                self.update_knowledge("questions", message.payload.get("questions"))
                
            elif action == "competitor_ready":
                self.required_data["competitor"] = True
                self.update_knowledge("competitor", message.payload.get("competitor"))
        
        elif message.message_type == MessageType.DATA_RESPONSE:
            # Handle data responses from other agents
            if "parsed_product" in message.payload:
                self.required_data["product_data"] = True
                self.update_knowledge("product_data", message.payload["parsed_product"])
        
        # Check if we have all required data
        if all(self.required_data.values()) and not self.generated_pages:
            await self._generate_all_pages()
        
        # If we have questions and competitor but no product data, request it
        if self.required_data["questions"] and self.required_data["competitor"] and not self.required_data["product_data"]:
            return Message(
                sender=self.name,
                receiver="ProductDataAgent",
                message_type=MessageType.DATA_REQUEST,
                payload={"request": "latest_product"}
            )
        
        return None
    
    async def decide_next_action(self) -> Optional[Message]:
        # This agent decides when to request missing data
        if not self.required_data["product_data"]:
            # Request product data from parser
            return Message(
                sender=self.name,
                receiver="ProductDataAgent",
                message_type=MessageType.DATA_REQUEST,
                payload={"request": "latest_product"}
            )
        
        return None
    
    async def _generate_all_pages(self) -> None:
        """Generate all pages when data is ready"""
        await asyncio.sleep(0.3)  # Simulate processing time
        
        product_data = self.get_knowledge("product_data")
        questions = self.get_knowledge("questions")
        competitor = self.get_knowledge("competitor")
        
        # Generate FAQ page
        faq_page = {
            "page_type": "FAQ",
            "title": f"Frequently Asked Questions - {product_data['name']}",
            "questions": questions,  # All 15+ questions
            "total_questions": len(questions)
        }
        
        # Generate Product page
        product_page = {
            "page_type": "Product",
            "title": product_data['name'],
            "product_info": {
                "name": product_data['name'],
                "concentration": product_data['concentration'],
                "category": product_data.get('category', 'Skincare'),
                "price": product_data['price'],
                "skin_types": product_data['skin_types'],
                "key_ingredients": product_data['key_ingredients'],
                "benefits": product_data['benefits'],
                "usage": product_data['usage_instructions'],
                "side_effects": product_data['side_effects']
            }
        }
        
        # Generate Comparison page
        comparison_page = {
            "page_type": "Comparison",
            "title": f"{product_data['name']} vs {competitor['name']}",
            "product_a": product_data,
            "product_b": competitor,
            "comparison_points": [
                {"aspect": "Price", "product_a": product_data['price'], "product_b": competitor['price']},
                {"aspect": "Concentration", "product_a": product_data['concentration'], "product_b": competitor['concentration']},
                {"aspect": "Skin Types", "product_a": ", ".join(product_data.get('skin_types', [])), "product_b": ", ".join(competitor.get('skin_types', []))}
            ]
        }
        
        self.generated_pages = [faq_page, product_page, comparison_page]
        self.update_knowledge("generated_pages", self.generated_pages)
        
        # Notify orchestrator that workflow is complete
        await self._notify_workflow_complete()
    
    async def _notify_workflow_complete(self) -> None:
        """Notify orchestrator that workflow is complete"""
        message = Message(
            sender=self.name,
            receiver="orchestrator",
            message_type=MessageType.WORKFLOW_COMPLETE,
            payload={
                "status": "completed",
                "pages": self.generated_pages,
                "total_pages": len(self.generated_pages)
            }
        )
        self.message_bus.send(message)  # Use direct send instead of await
