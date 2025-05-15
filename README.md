# AI Governance Debate Simulator

A sophisticated debate simulation system that facilitates AI-powered discussions on artificial intelligence governance between virtual representatives of major global powers (United States, European Union, and China).

## Overview

This project simulates high-level diplomatic debates on AI governance and regulation using advanced language models. Each participant represents a major global power and maintains consistent policy positions and negotiation styles aligned with their nation's interests and values.

### Key Features

- **Multi-Agent Debate System**: Simulates interactions between AI representatives from different nations
- **Dynamic Response Generation**: Uses OpenRouter API to access various AI models for generating contextually relevant responses
- **Personality-Driven Interactions**: Each agent maintains a consistent personality and policy stance
- **Structured Debate Format**: Supports multi-round debates with different phases (opening statements, deliberation, conclusion)
- **Real-time Response Generation**: Agents respond to each other's arguments in real-time
- **Document Retrieval System**: Agents can access and reference PDF documents for informed arguments
- **Position Paper Generation**: Generate formal position papers in the style of diplomatic documents
- **User-friendly Document Management**: Streamlit interface for easy document uploading and management
- **Advanced Semantic Search**: Uses AI embeddings to find relevant content by meaning, not just keywords

## Prerequisites

- Python 3.8+
- OpenRouter API key
- Internet connection for API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AIwars.git
cd AIwars
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your OpenRouter API key:
```
OPENROUTER_API_KEY=your_api_key_here
```

## Configuration

The system can be configured through `config.yaml`. Key configuration options include:

- Agent personalities and backgrounds
- Model selection for each agent
- Debate parameters (rounds, timing, etc.)
- Custom action sets for each agent

## Usage

### Starting the Debate Simulation

```bash
python run_debate.py
```

Access the web interface:
- Open your browser and navigate to the URL shown in the console
- Default: http://localhost:8501

### Managing Documents for Agent Reference

There are two ways to manage documents:

#### 1. Using the Streamlit Document Manager (Recommended)

```bash
streamlit run document_uploader.py
```

This opens a user-friendly interface where you can:
- Upload PDF documents for each agent
- View all uploaded documents
- Search through document content
- Preview document text
- Delete documents when no longer needed

#### 2. Using the Command-line Interface

```bash
# Upload a document
python document_retrieval.py upload --file path/to/document.pdf --agent United_States --type "regulation" --title "Document Title"

# List documents
python document_retrieval.py list --agent United_States

# Search documents
python document_retrieval.py search --query "AI governance" --agent United_States

# Get semantic search status
python document_retrieval.py status
```

### Generating Position Papers

To generate formatted position papers in the style of diplomatic documents:

```bash
# Generate US position paper
python generate_position_papers.py us

# Generate EU position paper
python generate_position_papers.py eu

# Generate both position papers
python generate_position_papers.py all
```

## Debate Structure

The debate follows a structured format:

1. **Opening Round (1-3)**
   - Agents establish their initial positions
   - Present core principles and priorities

2. **Engagement Round (4-7)**
   - Critical discussion of proposals
   - Challenge and defend positions
   - Explore areas of disagreement

3. **Consensus Building (8+)**
   - Work toward common ground
   - Propose compromise solutions
   - Maintain core national interests

4. **Conclusion**
   - Present final position papers
   - Summarize key agreements and disagreements
   - Outline future cooperation frameworks

## Document Reference System

### How It Works

The document reference system allows debate agents to access policy documents for more informed responses:

1. **Document Upload and Processing**:
   - PDF documents are uploaded for each agent
   - Text is extracted and stored for quick access
   - For semantic search, text is split into optimally-sized chunks
   - Vector embeddings are created for semantic understanding

2. **During Debates**:
   - Agents automatically search for relevant information in their documents
   - They incorporate references to official policies in their responses
   - Citations include specific page numbers, sections, and quotes
   - This makes the debate more factually grounded and realistic

3. **Advanced Semantic Search**:
   - The system uses AI embeddings to understand the meaning of text
   - Searches can find conceptually relevant content (not just keyword matches)
   - Results are ranked by semantic similarity
   - Automatically falls back to keyword search if semantic search is unavailable

4. **Document Types to Upload**:
   - **For US**: Executive Orders, NIST frameworks, national strategies
   - **For EU**: AI Act, regulatory frameworks, innovation initiatives
   - **For China**: Administrative measures, national AI initiatives, white papers

### Configuring Semantic Search

You can configure semantic search in `document_retrieval.py`:

```python
# Configuration for semantic search
ENABLE_SEMANTIC_SEARCH = True  # Set to False to disable semantic search
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Model for creating embeddings
SEMANTIC_CHUNK_SIZE = 300  # Characters per chunk for semantic indexing
SIMILARITY_THRESHOLD = 0.5  # Minimum similarity score for semantic matches
```

To check the status of semantic search:

```bash
python document_retrieval.py status
```

This shows metrics like:
- Number of documents with embeddings
- Total text chunks indexed
- Model being used
- Per-document statistics

### Storage Structure

Documents are stored in the `agent_documents/` directory with agent-specific subfolders:

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

## Customization

You can customize various aspects of the debate:

- Agent personalities in `config.yaml`
- Debate topics and prompts
- Number of rounds
- Response generation parameters
- UI elements and display options
- Document retrieval parameters
- Semantic search options (model, chunk size, thresholds)

## Troubleshooting

Common issues and solutions:

1. **API Connection Issues**
   - Verify your OpenRouter API key
   - Check internet connection
   - Confirm API rate limits

2. **Response Generation Failures**
   - System will use fallback responses
   - Check logs for error messages
   - Verify model availability

3. **Document Processing Issues**
   - Ensure PDFs are readable and not password-protected
   - Check that PyPDF2 is properly installed
   - Verify write permissions in the agent_documents directory

4. **Semantic Search Issues**
   - Run `python document_retrieval.py status` to check if semantic search is enabled
   - Ensure sentence-transformers and torch are installed
   - For better performance, consider using a GPU (though not required)

5. **Performance Issues**
   - Adjust response length limits
   - Modify temperature settings
   - Check system resources

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:

- Bug fixes
- Feature enhancements
- Documentation improvements
- UI/UX suggestions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenRouter for API access
- Various AI models used in the system
- Sentence Transformers library for semantic embeddings
- Contributors and testers

## Contact

For questions, issues, or suggestions, please open an issue in the repository or contact the maintainers.