"""
Template Engine

Core template processing engine for generating structured content.
"""

from typing import Dict, Any, List
from abc import ABC, abstractmethod


class BaseTemplate(ABC):
    """Base template class"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def render(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render template with data"""
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Get template schema"""
        pass


class TemplateProcessor:
    """Template processing engine"""
    
    def __init__(self):
        self.templates: Dict[str, BaseTemplate] = {}
    
    def register_template(self, template: BaseTemplate) -> None:
        """Register a template"""
        self.templates[template.name] = template
    
    def render_template(self, template_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render a template with data"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = self.templates[template_name]
        return template.render(data)
    
    def get_template_schema(self, template_name: str) -> Dict[str, Any]:
        """Get template schema"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        return self.templates[template_name].get_schema()
    
    def list_templates(self) -> List[str]:
        """List all registered templates"""
        return list(self.templates.keys())
