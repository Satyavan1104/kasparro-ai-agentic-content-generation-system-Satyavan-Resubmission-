"""
Data Models

Defines the data structures used throughout the multi-agent system.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum


class ProductCategory(Enum):
    SERUM = "Serum"
    CREAM = "Cream"
    LOTION = "Lotion"
    OIL = "Oil"
    SKINCARE = "Skincare"


class QuestionCategory(Enum):
    INFORMATIONAL = "Informational"
    SAFETY = "Safety"
    USAGE = "Usage"
    BENEFITS = "Benefits"
    PURCHASE = "Purchase"
    COMPARISON = "Comparison"
    RESULTS = "Results"


@dataclass
class ProductModel:
    """Structured product data model"""
    id: str
    name: str
    concentration: str
    category: ProductCategory
    skin_types: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    usage_instructions: str
    side_effects: Optional[str]
    price: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "concentration": self.concentration,
            "category": self.category.value,
            "skin_types": self.skin_types,
            "key_ingredients": self.key_ingredients,
            "benefits": self.benefits,
            "usage_instructions": self.usage_instructions,
            "side_effects": self.side_effects,
            "price": self.price
        }


@dataclass
class QuestionModel:
    """Question data model"""
    question: str
    answer: str
    category: QuestionCategory
    priority: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "question": self.question,
            "answer": self.answer,
            "category": self.category.value,
            "priority": self.priority
        }


@dataclass
class PageModel:
    """Base page model"""
    page_type: str
    title: str
    content: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_type": self.page_type,
            "title": self.title,
            **self.content
        }


@dataclass
class FAQPageModel(PageModel):
    """FAQ page specific model"""
    questions: List[QuestionModel]
    total_questions: int
    
    def __post_init__(self):
        self.page_type = "FAQ"
        self.total_questions = len(self.questions)
        self.content = {
            "questions": [q.to_dict() for q in self.questions],
            "total_questions": self.total_questions,
            "categories": list(set(q.category.value for q in self.questions))
        }


@dataclass
class ProductPageModel(PageModel):
    """Product page specific model"""
    product: ProductModel
    
    def __post_init__(self):
        self.page_type = "Product"
        self.title = self.product.name
        self.content = {
            "product_info": self.product.to_dict()
        }


@dataclass
class ComparisonPageModel(PageModel):
    """Comparison page specific model"""
    product_a: ProductModel
    product_b: ProductModel
    comparison_points: List[Dict[str, str]]
    
    def __post_init__(self):
        self.page_type = "Comparison"
        self.title = f"{self.product_a.name} vs {self.product_b.name}"
        self.content = {
            "product_a": self.product_a.to_dict(),
            "product_b": self.product_b.to_dict(),
            "comparison_points": self.comparison_points
        }
