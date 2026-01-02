"""
Usage Content Block

Generates usage-related content for products.
"""

from typing import Dict, Any, List

from .content_base import BaseContentBlock


class UsageBlock(BaseContentBlock):
    """Content block for generating usage information"""
    
    def __init__(self):
        super().__init__("usage")
    
    def generate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate usage content block"""
        usage_instructions = data.get("usage_instructions", "")
        skin_types = data.get("skin_types", [])
        
        if not usage_instructions:
            return {
                "type": "usage",
                "content": "No specific usage instructions available.",
                "instructions": []
            }
        
        usage_content = {
            "type": "usage", 
            "instructions": usage_instructions,
            "suitable_for": skin_types,
            "usage_tips": self._generate_usage_tips(skin_types),
            "frequency": self._infer_frequency(usage_instructions)
        }
        
        return usage_content
    
    def get_required_fields(self) -> List[str]:
        """Get required fields for usage block"""
        return ["usage_instructions"]
    
    def _generate_usage_tips(self, skin_types: List[str]) -> List[str]:
        """Generate usage tips based on skin types"""
        tips = []
        
        if "Oily" in skin_types:
            tips.append("Use sparingly on oily areas")
        if "Sensitive" in skin_types:
            tips.append("Patch test before full application")
        if "Combination" in skin_types:
            tips.append("Focus on drier areas of the face")
        
        return tips or ["Apply to clean, dry skin"]
    
    def _infer_frequency(self, instructions: str) -> str:
        """Infer usage frequency from instructions"""
        instructions_lower = instructions.lower()
        
        if "morning" in instructions_lower and "evening" in instructions_lower:
            return "Twice daily"
        elif "morning" in instructions_lower:
            return "Once daily (morning)"
        elif "evening" in instructions_lower:
            return "Once daily (evening)"
        else:
            return "As needed"
