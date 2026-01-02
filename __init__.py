"""
Agentic Content Generation System

A true multi-agent system for automated content generation.
"""

__version__ = "1.0.0"
__author__ = "Multi-Agent System Developer"
__description__ = "Autonomous multi-agent content generation system"

# Core imports
from .framework import (
    WorkflowCoordinator, MessageHub, AutonomousAgent, 
    AgentCapability, Message, MessageType, AgentState
)

# Data models
from .data_structures import (
    ProductModel, QuestionModel, PageModel,
    FAQPageModel, ProductPageModel, ComparisonPageModel
)

# Content modules
from .content_modules import (
    BaseContentBlock, BenefitsBlock, UsageBlock,
    IngredientsBlock, SafetyBlock, ComparisonBlock
)

# Page templates
from .page_templates import (
    TemplateProcessor, FAQLayout, ProductLayout, ComparisonLayout
)

# Agents
from .agents_system import (
    ProductDataAgent, QueryGenerationAgent,
    RivalCreationAgent, PageAssemblyAgent
)

__all__ = [
    # Core framework
    "WorkflowCoordinator",
    "MessageHub", 
    "AutonomousAgent",
    "AgentCapability",
    "Message",
    "MessageType",
    "AgentState",
    
    # Data models
    "ProductModel",
    "QuestionModel", 
    "PageModel",
    "FAQPageModel",
    "ProductPageModel",
    "ComparisonPageModel",
    
    # Content modules
    "BaseContentBlock",
    "BenefitsBlock",
    "UsageBlock",
    "IngredientsBlock", 
    "SafetyBlock",
    "ComparisonBlock",
    
    # Page templates
    "TemplateProcessor",
    "FAQLayout",
    "ProductLayout",
    "ComparisonLayout",
    
    # Agents
    "ProductDataAgent",
    "QueryGenerationAgent",
    "RivalCreationAgent",
    "PageAssemblyAgent"
]
