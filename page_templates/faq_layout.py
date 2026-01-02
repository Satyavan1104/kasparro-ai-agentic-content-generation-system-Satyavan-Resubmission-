"""
FAQ Template

Template for generating FAQ pages.
"""

from typing import Dict, Any, List

from .template_processor import BaseTemplate


class FAQLayout(BaseTemplate):
    """Template for FAQ pages"""
    
    def __init__(self):
        super().__init__("faq")
    
    def render(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render FAQ template with data"""
        questions = data.get("questions", [])
        product_name = data.get("product_name", "Product")
        
        # Group questions by category
        questions_by_category = self._group_by_category(questions)
        
        faq_page = {
            "page_type": "FAQ",
            "title": f"Frequently Asked Questions - {product_name}",
            "product_name": product_name,
            "introduction": f"Find answers to common questions about {product_name}.",
            "faq_items": questions[:15],  # Ensure minimum 15 questions
            "faq_by_category": questions_by_category,
            "categories": list(questions_by_category.keys()),
            "total_questions": len(questions[:15])
        }
        
        return faq_page
    
    def get_schema(self) -> Dict[str, Any]:
        """Get FAQ template schema"""
        return {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "answer": {"type": "string"},
                            "category": {"type": "string"},
                            "priority": {"type": "integer"}
                        }
                    }
                },
                "product_name": {"type": "string"}
            },
            "required": ["questions", "product_name"]
        }
    
    def _group_by_category(self, questions: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group questions by category"""
        grouped = {}
        
        for question in questions:
            category = question.get("category", "General")
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(question)
        
        # Sort categories by question count
        return dict(sorted(grouped.items(), key=lambda x: len(x[1]), reverse=True))
