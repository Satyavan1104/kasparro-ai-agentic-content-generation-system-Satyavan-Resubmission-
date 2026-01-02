"""
Safety Content Block

Generates safety-related content for products.
"""

from typing import Dict, Any, List

from .content_base import BaseContentBlock


class SafetyBlock(BaseContentBlock):
    """Content block for generating safety information"""
    
    def __init__(self):
        super().__init__("safety")
    
    def generate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate safety content block"""
        side_effects = data.get("side_effects", "")
        
        safety_content = {
            "type": "safety",
            "side_effects": side_effects,
            "precautions": self._generate_precautions(side_effects),
            "patch_test_advice": "Always perform a patch test before using new products",
            "safety_rating": self._generate_safety_rating(side_effects)
        }
        
        return safety_content
    
    def get_required_fields(self) -> List[str]:
        """Get required fields for safety block"""
        return []  # Side effects are optional
    
    def _generate_precautions(self, side_effects: str) -> List[str]:
        """Generate safety precautions"""
        precautions = [
            "Keep out of reach of children",
            "Store in a cool, dry place",
            "Avoid contact with eyes"
        ]
        
        if side_effects and "tingling" in side_effects.lower():
            precautions.append("May cause mild tingling sensation initially")
            precautions.append("Discontinue use if irritation persists")
        
        if side_effects and "sensitive" in side_effects.lower():
            precautions.append("Suitable for most skin types but caution for sensitive skin")
        
        return precautions
    
    def _generate_safety_rating(self, side_effects: str) -> str:
        """Generate safety rating based on side effects"""
        if not side_effects:
            return "Generally safe for most users"
        elif "mild" in side_effects.lower():
            return "Safe with mild potential side effects"
        else:
            return "Use with caution - consult dermatologist if concerned"
