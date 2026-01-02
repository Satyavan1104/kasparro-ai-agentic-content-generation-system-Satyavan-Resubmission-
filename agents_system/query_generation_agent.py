"""
Question Generator Agent

Autonomous agent that generates categorized user questions about products.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

from framework import (
    AutonomousAgent, AgentCapability, Message, MessageType, AgentState
)


class QueryGenerationAgent(AutonomousAgent):
    """Autonomous agent that generates questions and decides what to question"""
    
    def __init__(self, message_bus):
        super().__init__("QueryGenerationAgent", message_bus)
        self.generated_questions: List[Dict[str, Any]] = []
    
    def get_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="generate_questions",
                description="Generate categorized user questions about products",
                input_types=["parsed_product", "coordination_request"],
                output_types=["questions_list", "categorized_questions"],
                can_initiate=False,
                can_coordinate=True
            )
        ]
    
    async def process_message(self, message: Message) -> Optional[Message]:
        if message.message_type == MessageType.COORDINATION_REQUEST:
            action = message.payload.get("action")
            
            if action == "generate_questions":
                product_data = message.payload.get("product_data")
                questions = await self._generate_questions(product_data)
                
                self.generated_questions.extend(questions)
                self.update_knowledge("latest_questions", questions)
                self.update_knowledge("questions_generated", True)
                
                # Notify other agents that questions are ready
                await self._notify_questions_ready(questions)
                
                return Message(
                    sender=self.name,
                    receiver=message.sender,
                    message_type=MessageType.COORDINATION_RESPONSE,
                    payload={
                        "status": "completed",
                        "questions": questions,
                        "total_questions": len(questions)
                    }
                )
        
        elif message.message_type == MessageType.DATA_REQUEST:
            if message.payload.get("request") == "latest_questions":
                questions = self.get_knowledge("latest_questions")
                if questions:
                    return Message(
                        sender=self.name,
                        receiver=message.sender,
                        message_type=MessageType.DATA_RESPONSE,
                        payload={"questions": questions},
                        correlation_id=message.correlation_id
                    )
        
        return None
    
    async def decide_next_action(self) -> Optional[Message]:
        # This agent decides when it has enough information to generate questions
        # and coordinates with content generation when ready
        
        if self.generated_questions and not self.get_knowledge("notified_content_agent"):
            # Notify content agent that we have questions
            return Message(
                sender=self.name,
                receiver="ContentGeneratorAgent",
                message_type=MessageType.COORDINATION_REQUEST,
                payload={
                    "action": "questions_ready",
                    "questions": self.get_knowledge("latest_questions")
                }
            )
        
        return None
    
    async def _generate_questions(self, product_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate categorized questions about the product"""
        await asyncio.sleep(0.2)  # Simulate thinking time
        
        questions = []
        
        # Informational questions (3 questions)
        questions.extend([
            {"category": "Informational", "question": f"What is {product_data['name']}?", "answer": f"{product_data['name']} is a {product_data.get('category', 'skincare product')} with {product_data['concentration']}."},
            {"category": "Informational", "question": f"What are the key ingredients in {product_data['name']}?", "answer": f"The key ingredients in {product_data['name']} include {', '.join(product_data['key_ingredients'])}."},
            {"category": "Informational", "question": f"What type of product is {product_data['name']}?", "answer": f"{product_data['name']} is a {product_data.get('category', 'skincare')} serum designed for daily use."}
        ])
        
        # Usage questions (4 questions)
        questions.extend([
            {"category": "Usage", "question": f"How do I use {product_data['name']}?", "answer": product_data['usage_instructions']},
            {"category": "Usage", "question": f"Is {product_data['name']} suitable for {', '.join(product_data['skin_types'])} skin?", "answer": f"Yes, {product_data['name']} is formulated for {', '.join(product_data['skin_types'])} skin types."},
            {"category": "Usage", "question": f"When should I apply {product_data['name']}?", "answer": f"Apply {product_data['name']} in the morning before sunscreen for best results."},
            {"category": "Usage", "question": f"How many drops of {product_data['name']} should I use?", "answer": "Use 2-3 drops of the serum and gently massage into your face."}
        ])
        
        # Safety questions (3 questions)
        questions.extend([
            {"category": "Safety", "question": f"What are the side effects of {product_data['name']}?", "answer": product_data['side_effects']},
            {"category": "Safety", "question": f"Is {product_data['name']} safe for sensitive skin?", "answer": f"{product_data['name']} may cause mild tingling for sensitive skin, but is generally safe for most skin types."},
            {"category": "Safety", "question": f"Can I use {product_data['name']} with other skincare products?", "answer": f"Yes, {product_data['name']} can be used with other skincare products, but apply it before heavier creams."}
        ])
        
        # Benefits questions (3 questions)
        for benefit in product_data['benefits']:
            questions.append({
                "category": "Benefits",
                "question": f"How does {product_data['name']} help with {benefit}?",
                "answer": f"The key ingredients in {product_data['name']} work together to provide {benefit} benefits."
            })
        
        # Purchase questions (3 questions)
        questions.extend([
            {"category": "Purchase", "question": f"Where can I buy {product_data['name']}?", "answer": f"{product_data['name']} is available for {product_data['price']}."},
            {"category": "Purchase", "question": f"Is {product_data['name']} worth the price?", "answer": f"At {product_data['price']}, {product_data['name']} offers good value for its benefits."},
            {"category": "Purchase", "question": f"How long does one bottle of {product_data['name']} last?", "answer": f"One bottle of {product_data['name']} typically lasts 1-2 months with daily use."}
        ])
        
        return questions
    
    async def _notify_questions_ready(self, questions: List[Dict[str, Any]]) -> None:
        """Notify other agents that questions are ready"""
        self.update_knowledge("notified_content_agent", True)
        
        # Immediately notify content generator
        message = Message(
            sender=self.name,
            receiver="PageAssemblyAgent",
            message_type=MessageType.COORDINATION_REQUEST,
            payload={
                "action": "questions_ready",
                "questions": questions
            }
        )
        await self.send_message(message)
