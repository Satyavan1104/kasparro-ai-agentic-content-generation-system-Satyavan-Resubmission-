"""
Product Template

Template for generating product pages.
"""

from typing import Dict, Any

from .template_processor import BaseTemplate


class ProductLayout(BaseTemplate):
    """Template for product pages"""
    
    def __init__(self):
        super().__init__("product")
    
    def render(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render product template with data"""
        product = data.get("product", {})
        
        product_page = {
            "page_type": "Product",
            "title": product.get("name", "Product"),
            "product_info": {
                "name": product.get("name", ""),
                "concentration": product.get("concentration", ""),
                "category": product.get("category", ""),
                "price": product.get("price", ""),
                "skin_types": product.get("skin_types", []),
                "key_ingredients": product.get("key_ingredients", []),
                "benefits": product.get("benefits", []),
                "usage": product.get("usage_instructions", ""),
                "side_effects": product.get("side_effects", ""),
                "product_id": product.get("id", "")
            },
            "product_highlights": self._generate_highlights(product),
            "usage_instructions": self._format_usage(product.get("usage_instructions", "")),
            "ingredients_list": self._format_ingredients(product.get("key_ingredients", [])),
            "benefits_list": self._format_benefits(product.get("benefits", []))
        }
        
        return product_page
    
    def get_schema(self) -> Dict[str, Any]:
        """Get product template schema"""
        return {
            "type": "object",
            "properties": {
                "product": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "concentration": {"type": "string"},
                        "category": {"type": "string"},
                        "price": {"type": "string"},
                        "skin_types": {"type": "array"},
                        "key_ingredients": {"type": "array"},
                        "benefits": {"type": "array"},
                        "usage_instructions": {"type": "string"},
                        "side_effects": {"type": "string"},
                        "id": {"type": "string"}
                    }
                }
            },
            "required": ["product"]
        }
    
    def _generate_highlights(self, product: Dict[str, Any]) -> List[str]:
        """Generate product highlights"""
        highlights = []
        
        benefits = product.get("benefits", [])
        if benefits:
            highlights.append(f"Key benefits: {', '.join(benefits[:2])}")
        
        ingredients = product.get("key_ingredients", [])
        if ingredients:
            highlights.append(f"Formulated with {ingredients[0]}")
        
        skin_types = product.get("skin_types", [])
        if skin_types:
            highlights.append(f"Suitable for {', '.join(skin_types)} skin")
        
        return highlights
    
    def _format_usage(self, usage_instructions: str) -> Dict[str, Any]:
        """Format usage instructions"""
        return {
            "instructions": usage_instructions,
            "tips": [
                "Apply to clean, dry skin",
                "Use consistently for best results",
                "Follow with moisturizer if needed"
            ]
        }
    
    def _format_ingredients(self, ingredients: List[str]) -> Dict[str, Any]:
        """Format ingredients list"""
        return {
            "key_ingredients": ingredients,
            "total_count": len(ingredients),
            "featured": ingredients[:3] if len(ingredients) > 3 else ingredients
        }
    
    def _format_benefits(self, benefits: List[str]) -> Dict[str, Any]:
        """Format benefits list"""
        return {
            "main_benefits": benefits,
            "primary_benefit": benefits[0] if benefits else "",
            "benefit_count": len(benefits)
        }
