"""
Ingredients Content Block

Generates ingredients-related content for products.
"""

from typing import Dict, Any, List

from .content_base import BaseContentBlock


class IngredientsBlock(BaseContentBlock):
    """Content block for generating ingredients information"""
    
    def __init__(self):
        super().__init__("ingredients")
    
    def generate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate ingredients content block"""
        key_ingredients = data.get("key_ingredients", [])
        concentration = data.get("concentration", "")
        
        if not key_ingredients:
            return {
                "type": "ingredients",
                "content": "No specific ingredients information available.",
                "key_ingredients": []
            }
        
        ingredients_content = {
            "type": "ingredients",
            "key_ingredients": key_ingredients,
            "concentration": concentration,
            "ingredient_details": self._generate_ingredient_details(key_ingredients),
            "ingredient_summary": f"Key ingredients include {', '.join(key_ingredients[:2])}."
        }
        
        return ingredients_content
    
    def get_required_fields(self) -> List[str]:
        """Get required fields for ingredients block"""
        return ["key_ingredients"]
    
    def _generate_ingredient_details(self, ingredients: List[str]) -> List[Dict[str, str]]:
        """Generate detailed ingredient information"""
        details = []
        
        ingredient_info = {
            "Vitamin C": "Powerful antioxidant that brightens skin and fights free radicals",
            "Hyaluronic Acid": "Provides intense hydration and plumps the skin",
            "Vitamin E": "Antioxidant that protects and nourishes the skin",
            "Niacinamide": "Helps to even out skin tone and reduce inflammation",
            "Retinol": "Promotes cell turnover and reduces signs of aging",
            "Peptides": "Help to firm and rejuvenate the skin",
            "Antioxidants": "Protect skin from environmental damage"
        }
        
        for ingredient in ingredients:
            info = ingredient_info.get(ingredient, f"Beneficial ingredient for skin health")
            details.append({
                "ingredient": ingredient,
                "benefit": info
            })
        
        return details
