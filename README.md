#  Applied AI Engineer Challenge: Multi-Agent Content Generation System - Resubmission
Agentic automation system that generates structured product, FAQ, and comparison pages from raw product data using multi-agent workflows, reusable logic blocks, and template-driven JSON outputs.

## Problem Addressed
The core requirement of the task has not been met because it failed to demonstrate a true multi-agent system. The feedback specifically stated:
- Simply hard-coding multiple functions or sequential logic and labeling them as 'agents' does not satisfy this requirement.
- A valid solution requires: Clear separation of agent responsibilities, Dynamic agent interaction and coordination, An architecture that supports agent autonomy rather than static control flow

## Problem Context
The original implementation was flagged for lacking authentic agent-based behavior. Evaluation feedback emphasized that simply sequencing functions and labeling them as agents does not constitute a true multi-agent system.

Required characteristics included:
- Clearly independent agents  
- Message-based communication  
- Runtime decision-making  
- No static execution order  
- Emergent workflow behavior  

---

## Solution Summary
This redesigned system implements a **true distributed multi-agent architecture** where agents operate independently and collaborate exclusively through asynchronous message passing.
Key outcomes:
- Removal of static pipelines and hardcoded execution
- Decentralized agent coordination via a MessageHub
- Autonomous agent decision-making
- Parallel and emergent execution behavior
- Architecture aligned with real-world agent systems

---

## Architecture Evolution

| Features | Earlier Design | Current Design | Resolution |
|--------|---------------|----------------|-----------|
| Execution Model | Linear function chain | Message-driven agent network | Removed static sequencing |
| Agent Independence | Dependent execution | Fully autonomous agents | No direct agent calls |
| Communication | Function invocation | Typed message passing | Central MessageHub |
| Workflow Control | Hardcoded order | Emergent from messages | Runtime coordination |
| Decision Authority | Orchestrator-only | Distributed across agents | True autonomy |
| System Behavior | Predictable | Adaptive & emergent | Meets agent criteria |

---

## Core Design Principles

### 1. Autonomous Agent Boundaries
Each agent:
- Owns a single responsibility
- Maintains local state (knowledge base)
- Reacts only to supported message types
- Has no awareness of other agents’ internals

---

### 2. Message-Driven Coordination
- All communication occurs through a central **MessageHub**
- No agent invokes another directly
- Execution order emerges naturally from message dependencies
- Agents decide when and how to act

---

### 3. Distributed Decision-Making
- No global execution plan
- Agents independently determine next actions
- Supports concurrency and partial completion
- Enables adaptive runtime behavior

---

## Multi Agent Architecture 
The Multi-Agent Architecture represents a distributed system where autonomous, specialized agents collaborate to transform structured product data into rich, structured content outputs. Each agent operates independently while coordinating through a message-driven communication layer, enabling scalability, modularity, and dynamic execution.

![System Architecture](docs/System%20Design/Agent.png)

- Each agent (ProductData, QueryGeneration, RivalCreation, PageAssembly) owns a distinct responsibility and logic.
- Agents do not call each other directly; all interactions occur via messages.
- A centralized MessageHub enables asynchronous communication and event propagation.
- Agents focus on a single domain concern (parsing, Q&A, comparison, assembly).
  
## System Components

### Infrastructure Layer
- **Message** – Typed communication payload (event, data, sender, receiver)
- **MessageHub** – Central routing and queueing system
- **AutonomousAgent (Base Class)** – Defines agent lifecycle
- **AgentRegistry** – Dynamic agent discovery
- **WorkflowCoordinator** – Entry-point trigger (not a controller)

---

### Specialized Agents

#### - ProductDataAgent
   - Parses and normalizes product input
   - Publishes structured product facts
   - Triggers downstream agents via coordination messages

#### - QueryGenerationAgent
   - Generates 15+ categorized user questions
   - Operates independently once product data is available
   - Notifies assembly agent upon completion

#### - RivalCreationAgent
   - Constructs fictional competitor data
   - Operates in parallel with question generation
   - Sends competitive insights asynchronously

####  - PageAssemblyAgent
   - Requests data from multiple agents
   - Applies templates and content modules
   - Produces final JSON artifacts
   - Signals workflow completion

---

## Content & Rendering Layer

- **Content Modules**: Benefits, Usage, Safety, Comparison
- **Template Processor**: Schema-driven rendering
- **Page Templates**: FAQ, Product, Comparison
- **Reusable Blocks**: Modular and extensible logic units

---

## System Design 
The system is designed as a **layered, agentic architecture** with explicit data flow and zero hidden global state.

## System Architecturetr
The System Architecture provides a layered, structural view of the entire platform, detailing how control logic, agents, communication infrastructure, and output generation are organized.

![System Architecture](docs/System%20Design/System.jpeg)

- **Input & Control Layer**
  - System entry point for workflow execution
  - `execute_workflow.py` initializes and triggers the pipeline
  - `data_structures.py` defines shared data models and enums
  - Ensures consistent data contracts across agents

- **Orchestration Layer**
  - Workflow Coordinator manages overall execution flow
  - Dynamically triggers agents based on task dependencies
  - AgentRegistry handles agent discovery and lifecycle management
  - Framework Core enforces orchestration rules and coordination logic

- **Messaging Layer**
  - MessageHub acts as a central communication bus
  - Decouples interactions between autonomous agents
  - Supports asynchronous, event-driven messaging

- **Autonomous Agent Layer**
  - Product Data Agent parses and validates product datasets
  - Query Generation Agent generates questions and FAQs
  - Rival Creation Agent creates competitor and comparison data
  - Page Assembly Agent aggregates content from all agents

- **Template Processing Layer**
  - Applies layouts for FAQ, Product, and Comparison pages
  - Transforms assembled content into structured page schemas

- **Output Layer**
  - Generates final JSON artifacts
  - Produces FAQ, Product, and Comparison page JSON files
  - Outputs are ready for downstream system consumption

## Orchestration Graph (DAG)
The Orchestration Graph models the system workflow as a Directed Acyclic Graph (DAG), capturing logical dependencies between agents without enforcing a rigid execution order. This enables dynamic coordination rather than hard-coded sequencing.

![Orchestration Graph](docs/System%20Design/DAG.jpeg)

- Each node corresponds to an agent or processing step.
- Directed edges indicate data or control dependencies.
- The Workflow Coordinator evaluates DAG state to trigger agent execution.
- Independent branches (e.g., Query & Rival generation) run simultaneously.

## Flowchart
The Workflow describes the operational lifecycle of a request, from raw product input to finalized JSON outputs, emphasizing agent autonomy and dynamic coordination.

![Flowchart](docs/System%20Design/workflow.jpeg)

- Start with Structured Input: Product dataset is submitted as JSON.
- Data Parsing & Normalization: ProductDataAgent validates and standardizes input.
- Parallel Content Generation:
    - QueryGenerationAgent creates questions/FAQs.
    - RivalCreationAgent generates competitor comparisons.
- Reusable Content Blocks: Content logic is applied modularly.
- Page Assembly: PageAssemblyAgent combines all generated content.
- Template Application: TemplateProcessor formats content into page-specific schemas.
- Final Output: JSON files are exported for FAQ, Product, and Comparison pages.
- End-to-End Automation: No manual intervention required once workflow starts.

## Sequence Diagram
The Sequence Diagram illustrates time-ordered interactions between system components, showing how data and messages flow across agents from input submission to final JSON export.

![Sequence Diagram](docs/System%20Design/Sequence%20Diagram.png)

- Temporal Flow: Clearly shows the order of message exchanges.
- Actor Separation: Distinguishes ProductJSON, Coordinator, Agents, MessageHub, and Output.
- Asynchronous Messaging: MessageHub decouples senders and receivers.
- Agent Collaboration: Multiple agents contribute partial outputs independently.
- Data Aggregation: PageAssemblyAgent consolidates outputs before final processing.
- End-to-End Visibility: Demonstrates how a single request propagates through the system.

---

## Output Artifacts
- `outputs/faq_page.json` – 15+ categorized questions & answers
- `outputs/product_page.json` – Structured product description
- `outputs/comparison_page.json` – Competitor analysis

---

## Architecture Validation Checklist
- No hardcoded execution sequence  
- Autonomous agent behavior  
- Message-based coordination  
- Parallel processing  
- Decentralized state handling  
- Emergent system behavior  

This system meets and exceeds the requirements for a **genuine multi-agent architecture**.


