"""
Page Templates Package

Contains template definitions for generating structured pages.
"""

from .template_processor import TemplateProcessor
from .faq_layout import FAQLayout
from .product_layout import ProductLayout
from .comparison_layout import ComparisonLayout

__all__ = [
    "TemplateProcessor",
    "FAQLayout",
    "ProductLayout",
    "ComparisonLayout"
]
