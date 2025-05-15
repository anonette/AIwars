# Document Retrieval System for AI Debate

This module provides a document retrieval system that enables AI debate agents to access and reference PDF documents during deliberations.

## Features

- Upload and process PDF documents for each debate agent (US, EU, China)
- Extract and store text content from PDF files
- Search documents by keyword or semantic similarity
- Integrate document references into agent responses and conclusions
- Command-line interface for document management

## Setup

1. Install required dependencies:

```bash
pip install -r requirements.txt
```

2. For semantic search functionality (optional but recommended), ensure you have PyTorch and sentence-transformers installed:

```bash
pip install torch sentence-transformers
```

## Usage

### Command-line Interface

The document retrieval system provides a command-line interface for managing documents:

#### Upload a document

```bash
python document_retrieval.py upload --file path/to/document.pdf --agent United_States --type "regulation" --title "AI Executive Order" --desc "US Executive Order on AI Governance"
```

Available agents:
- United_States
- European_Union  
- Peoples_Republic_of_China

Document types can be anything descriptive, such as "regulation", "strategy", "policy", "whitepaper", etc.

#### List documents

```bash
# List all documents
python document_retrieval.py list

# List documents for a specific agent
python document_retrieval.py list --agent United_States
```

#### Search documents

```bash
# Search all documents
python document_retrieval.py search --query "governance framework"

# Search documents for a specific agent
python document_retrieval.py search --query "regulatory standards" --agent European_Union
```

#### Get document content

```bash
python document_retrieval.py get --id [document_id]
```

#### Delete a document

```bash
python document_retrieval.py delete --id [document_id]
```

### Integration with Debate Agents

To use document-enabled debate agents in your application:

1. Import the necessary classes:

```python
from document_integration import DocumentEnabledDebateAgent, create_document_enabled_agents
from document_retrieval import DocumentStore
```

2. Create a document store:

```python
document_store = DocumentStore()
```

3. Create document-enabled agents:

```python
# Using a config.yaml file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

agents = create_document_enabled_agents(config, document_store)
```

4. Use the agents in your debate manager:

```python
from debate_manager import DebateManager

debate = DebateManager(agents=agents, topic="AI Governance Summit")
```

## Document Organization

Documents are stored in the following directory structure:

```
agent_documents/
├── United_States/
│   ├── document1.txt
│   └── document2.txt
├── European_Union/
│   └── document3.txt
├── Peoples_Republic_of_China/
│   └── document4.txt
└── document_index.json
```

The `document_index.json` file contains metadata about all uploaded documents.

## How It Works

1. When a PDF document is uploaded, the system:
   - Extracts text content from the PDF
   - Stores the text content in a .txt file
   - Creates embeddings for semantic search (if available)
   - Updates the document index

2. During debates, agents can:
   - Search for relevant documents based on the debate topic
   - Find specific information related to the current discussion
   - Reference document content in their responses
   - Incorporate document references in their final position papers

## Example Documents to Upload

For the United States:
- Executive Order on Safe, Secure, and Trustworthy AI
- NIST AI Risk Management Framework
- National AI Research and Development Strategic Plan

For the European Union:
- EU AI Act
- European Declaration on Digital Rights and Principles
- EU AI Innovation Package

For China:
- Administrative Measures for Generative AI Services
- Global AI Governance Initiative
- China's digital governance white papers

## License

This software is provided under the same license as the parent AI Debate project. 