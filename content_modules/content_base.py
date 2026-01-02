"""
Base Content Block

Defines the base interface for all content blocks.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseContentBlock(ABC):
    """Base class for all content blocks"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def generate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content block from data"""
        pass
    
    @abstractmethod
    def get_required_fields(self) -> List[str]:
        """Get list of required fields for this block"""
        pass
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate that required fields are present"""
        required_fields = self.get_required_fields()
        return all(field in data for field in required_fields)
