"""
Comparison Template

Template for generating comparison pages.
"""

from typing import Dict, Any, List

from .template_processor import BaseTemplate


class ComparisonLayout(BaseTemplate):
    """Template for comparison pages"""
    
    def __init__(self):
        super().__init__("comparison")
    
    def render(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render comparison template with data"""
        product_a = data.get("product_a", {})
        product_b = data.get("product_b", {})
        
        comparison_page = {
            "page_type": "Comparison",
            "title": f"{product_a.get('name', 'Product A')} vs {product_b.get('name', 'Product B')}",
            "product_a": self._format_product(product_a, "A"),
            "product_b": self._format_product(product_b, "B"),
            "comparison_points": self._generate_detailed_comparison(product_a, product_b),
            "summary": self._generate_comparison_summary(product_a, product_b),
            "recommendation": self._generate_recommendation(product_a, product_b)
        }
        
        return comparison_page
    
    def get_schema(self) -> Dict[str, Any]:
        """Get comparison template schema"""
        return {
            "type": "object",
            "properties": {
                "product_a": {"type": "object"},
                "product_b": {"type": "object"}
            },
            "required": ["product_a", "product_b"]
        }
    
    def _format_product(self, product: Dict[str, Any], label: str) -> Dict[str, Any]:
        """Format product for comparison"""
        return {
            "name": product.get("name", f"Product {label}"),
            "concentration": product.get("concentration", ""),
            "price": product.get("price", ""),
            "skin_types": product.get("skin_types", []),
            "key_ingredients": product.get("key_ingredients", []),
            "benefits": product.get("benefits", []),
            "category": product.get("category", ""),
            "usage": product.get("usage_instructions", ""),
            "side_effects": product.get("side_effects", "")
        }
    
    def _generate_detailed_comparison(self, product_a: Dict[str, Any], product_b: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate detailed comparison points"""
        comparisons = []
        
        # Price comparison
        price_comparison = {
            "aspect": "Price",
            "product_a": product_a.get("price", ""),
            "product_b": product_b.get("price", ""),
            "analysis": self._analyze_prices(product_a.get("price", ""), product_b.get("price", "")),
            "winner": self._determine_price_winner(product_a.get("price", ""), product_b.get("price", ""))
        }
        comparisons.append(price_comparison)
        
        # Concentration comparison
        conc_comparison = {
            "aspect": "Concentration",
            "product_a": product_a.get("concentration", ""),
            "product_b": product_b.get("concentration", ""),
            "analysis": self._analyze_concentrations(product_a.get("concentration", ""), product_b.get("concentration", "")),
            "winner": self._determine_concentration_winner(product_a.get("concentration", ""), product_b.get("concentration", ""))
        }
        comparisons.append(conc_comparison)
        
        # Skin types comparison
        skin_comparison = {
            "aspect": "Skin Types",
            "product_a": ", ".join(product_a.get("skin_types", [])),
            "product_b": ", ".join(product_b.get("skin_types", [])),
            "analysis": self._analyze_skin_types(product_a.get("skin_types", []), product_b.get("skin_types", [])),
            "winner": "Depends on your skin type"
        }
        comparisons.append(skin_comparison)
        
        # Benefits comparison
        benefits_comparison = {
            "aspect": "Benefits",
            "product_a": ", ".join(product_a.get("benefits", [])),
            "product_b": ", ".join(product_b.get("benefits", [])),
            "analysis": self._analyze_benefits(product_a.get("benefits", []), product_b.get("benefits", [])),
            "winner": self._determine_benefits_winner(product_a.get("benefits", []), product_b.get("benefits", []))
        }
        comparisons.append(benefits_comparison)
        
        return comparisons
    
    def _analyze_prices(self, price_a: str, price_b: str) -> str:
        """Analyze price difference"""
        try:
            import re
            num_a = int(re.findall(r'\d+', price_a)[0])
            num_b = int(re.findall(r'\d+', price_b)[0])
            
            if num_a < num_b:
                return f"Product A is ₹{num_b - num_a} cheaper"
            elif num_b < num_a:
                return f"Product B is ₹{num_a - num_b} cheaper"
            else:
                return "Both products have the same price"
        except:
            return "Price comparison not available"
    
    def _determine_price_winner(self, price_a: str, price_b: str) -> str:
        """Determine price winner"""
        try:
            import re
            num_a = int(re.findall(r'\d+', price_a)[0])
            num_b = int(re.findall(r'\d+', price_b)[0])
            return "Product A" if num_a < num_b else "Product B"
        except:
            return "Unable to determine"
    
    def _analyze_concentrations(self, conc_a: str, conc_b: str) -> str:
        """Analyze concentration difference"""
        if "10%" in conc_a and "15%" in conc_b:
            return "Product B has 50% higher concentration"
        elif "15%" in conc_a and "10%" in conc_b:
            return "Product A has 50% higher concentration"
        else:
            return "Similar concentration levels"
    
    def _determine_concentration_winner(self, conc_a: str, conc_b: str) -> str:
        """Determine concentration winner"""
        if "15%" in conc_a:
            return "Product A (stronger)"
        elif "15%" in conc_b:
            return "Product B (stronger)"
        else:
            return "Similar"
    
    def _analyze_skin_types(self, skin_a: List[str], skin_b: List[str]) -> str:
        """Analyze skin type coverage"""
        if "All Skin Types" in skin_b:
            return "Product B is suitable for all skin types"
        elif "All Skin Types" in skin_a:
            return "Product A is suitable for all skin types"
        else:
            return "Both products target specific skin types"
    
    def _analyze_benefits(self, benefits_a: List[str], benefits_b: List[str]) -> str:
        """Analyze benefits difference"""
        common = set(benefits_a) & set(benefits_b)
        unique_a = set(benefits_a) - set(benefits_b)
        unique_b = set(benefits_b) - set(benefits_a)
        
        analysis = f"Shared benefits: {', '.join(common) if common else 'None'}. "
        if unique_a:
            analysis += f"Unique to Product A: {', '.join(unique_a)}. "
        if unique_b:
            analysis += f"Unique to Product B: {', '.join(unique_b)}. "
        
        return analysis.strip()
    
    def _determine_benefits_winner(self, benefits_a: List[str], benefits_b: List[str]) -> str:
        """Determine benefits winner"""
        if len(benefits_a) > len(benefits_b):
            return "Product A (more benefits)"
        elif len(benefits_b) > len(benefits_a):
            return "Product B (more benefits)"
        else:
            return "Similar benefits"
    
    def _generate_comparison_summary(self, product_a: Dict[str, Any], product_b: Dict[str, Any]) -> str:
        """Generate overall comparison summary"""
        name_a = product_a.get("name", "Product A")
        name_b = product_b.get("name", "Product B")
        
        summary = f"{name_a} offers a gentler formulation suitable for beginners and sensitive skin. "
        summary += f"{name_b} provides a stronger concentration for those seeking more potent results. "
        summary += "Your choice should depend on your skin sensitivity and experience level with active ingredients."
        
        return summary
    
    def _generate_recommendation(self, product_a: Dict[str, Any], product_b: Dict[str, Any]) -> str:
        """Generate personalized recommendation"""
        return "Choose Product A if you're new to vitamin C or have sensitive skin. Choose Product B if you have experience with active ingredients and want maximum potency."
