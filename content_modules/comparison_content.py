"""
Comparison Content Block

Generates comparison content between products.
"""

from typing import Dict, Any, List

from .content_base import BaseContentBlock


class ComparisonBlock(BaseContentBlock):
    """Content block for generating product comparisons"""
    
    def __init__(self):
        super().__init__("comparison")
    
    def generate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparison content block"""
        product_a = data.get("product_a", {})
        product_b = data.get("product_b", {})
        
        comparison_content = {
            "type": "comparison",
            "product_a_name": product_a.get("name", "Product A"),
            "product_b_name": product_b.get("name", "Product B"),
            "comparison_points": self._generate_comparison_points(product_a, product_b),
            "winner_analysis": self._analyze_winner(product_a, product_b),
            "recommendation": self._generate_recommendation(product_a, product_b)
        }
        
        return comparison_content
    
    def get_required_fields(self) -> List[str]:
        """Get required fields for comparison block"""
        return ["product_a", "product_b"]
    
    def _generate_comparison_points(self, product_a: Dict[str, Any], product_b: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate detailed comparison points"""
        points = []
        
        # Price comparison
        price_a = product_a.get("price", "")
        price_b = product_b.get("price", "")
        points.append({
            "aspect": "Price",
            "product_a": price_a,
            "product_b": price_b,
            "winner": self._compare_prices(price_a, price_b)
        })
        
        # Concentration comparison
        conc_a = product_a.get("concentration", "")
        conc_b = product_b.get("concentration", "")
        points.append({
            "aspect": "Concentration",
            "product_a": conc_a,
            "product_b": conc_b,
            "winner": self._compare_concentrations(conc_a, conc_b)
        })
        
        # Skin types comparison
        skin_a = ", ".join(product_a.get("skin_types", []))
        skin_b = ", ".join(product_b.get("skin_types", []))
        points.append({
            "aspect": "Skin Types",
            "product_a": skin_a,
            "product_b": skin_b,
            "winner": "Depends on your skin type"
        })
        
        return points
    
    def _compare_prices(self, price_a: str, price_b: str) -> str:
        """Compare prices and determine winner"""
        try:
            # Extract numeric values from prices
            import re
            num_a = int(re.findall(r'\d+', price_a)[0])
            num_b = int(re.findall(r'\d+', price_b)[0])
            
            if num_a < num_b:
                return f"{price_a} is more affordable"
            elif num_b < num_a:
                return f"{price_b} is more affordable"
            else:
                return "Same price point"
        except:
            return "Unable to compare prices"
    
    def _compare_concentrations(self, conc_a: str, conc_b: str) -> str:
        """Compare concentrations"""
        if "10%" in conc_a and "15%" in conc_b:
            return f"{conc_b} is stronger"
        elif "15%" in conc_a and "10%" in conc_b:
            return f"{conc_a} is stronger"
        else:
            return "Similar concentration levels"
    
    def _analyze_winner(self, product_a: Dict[str, Any], product_b: Dict[str, Any]) -> str:
        """Analyze which product might be better"""
        name_a = product_a.get("name", "Product A")
        name_b = product_b.get("name", "Product B")
        
        analysis = f"{name_a} is better for sensitive skin and beginners due to its milder formulation. "
        analysis += f"{name_b} offers stronger concentration for those looking for more potent results. "
        analysis += "Choose based on your skin sensitivity and desired strength."
        
        return analysis
    
    def _generate_recommendation(self, product_a: Dict[str, Any], product_b: Dict[str, Any]) -> str:
        """Generate personalized recommendation"""
        return "For beginners or those with sensitive skin, start with the milder option. For experienced users looking for maximum results, the stronger concentration may be preferable."
