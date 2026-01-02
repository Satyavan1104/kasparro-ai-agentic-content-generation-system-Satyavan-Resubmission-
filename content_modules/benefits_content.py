"""
Benefits Content Block

Generates benefits-related content for products.
"""

from typing import Dict, Any, List

from .content_base import BaseContentBlock


class BenefitsBlock(BaseContentBlock):
    """Content block for generating benefits information"""
    
    def __init__(self):
        super().__init__("benefits")
    
    def generate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate benefits content block"""
        benefits = data.get("benefits", [])
        
        if not benefits:
            return {
                "type": "benefits",
                "content": "No specific benefits information available.",
                "benefits_list": []
            }
        
        # Generate detailed benefits content
        benefits_content = {
            "type": "benefits",
            "main_benefits": benefits,
            "detailed_benefits": self._generate_detailed_benefits(benefits),
            "benefits_summary": f"This product provides {', '.join(benefits[:3])}."
        }
        
        return benefits_content
    
    def get_required_fields(self) -> List[str]:
        """Get required fields for benefits block"""
        return ["benefits"]
    
    def _generate_detailed_benefits(self, benefits: List[str]) -> List[Dict[str, str]]:
        """Generate detailed benefit descriptions"""
        detailed = []
        
        benefit_descriptions = {
            "Brightening": "Helps to brighten and even out skin tone",
            "Fades dark spots": "Reduces the appearance of dark spots and hyperpigmentation",
            "Anti-aging": "Helps to reduce signs of aging",
            "Hydration": "Provides deep hydration to the skin",
            "Firming": "Helps to improve skin firmness and elasticity"
        }
        
        for benefit in benefits:
            description = benefit_descriptions.get(benefit, f"Provides {benefit.lower()} benefits")
            detailed.append({
                "benefit": benefit,
                "description": description
            })
        
        return detailed
