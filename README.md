# AI Governance Debate Simulator

A sophisticated debate simulation system that facilitates AI-powered discussions on artificial intelligence governance between virtual representatives of major global powers (United States, European Union, and China).

## 🎭 Meta-Sovereignty Framework: The AI Cold War

This system implements a cutting-edge theoretical framework that analyzes AI governance as a **performance of technological sovereignty** rather than its possession. Drawing from political science concepts of credible commitment theory and political dramaturgy, the system reveals how nations navigate the gap between what they claim to control and what they actually control in AI development.

### Core Theoretical Concepts

**Meta-Sovereignty**: In the AI domain, traditional territorial sovereignty becomes "meta" - nations must perform authority over systems that increasingly escape their direct control. Each country develops strategies to project technological sovereignty through a combination of material commitments and symbolic performances.

**The AI Cold War Triangle**:
- **🇺🇸 United States**: A declining hegemonic power using "safety" discourse and export controls to maintain technological dominance while racing toward AGI
- **🇨🇳 People's Republic of China**: A rising power building parallel technological infrastructure through patient, state-directed development 
- **🇪🇺 European Union**: A regulatory superpower attempting to govern global AI through legal architecture while lacking indigenous capabilities

### How the System Works

#### 1. **Genuine LLM Generation with Theoretical Analysis**
The system lets LLMs generate authentic responses based on each nation's strategic psychology, then automatically analyzes those responses through the meta-sovereignty framework to extract:

- **Costly Signals**: Material commitments that limit future flexibility (legislation, investments, treaties)
- **Performance Fictions**: Symbolic gestures that dramatize sovereignty (ceremonies, rhetoric, alliance theater)  
- **Signal-Fiction Tensions**: Contradictions between material constraints and symbolic performances

#### 2. **Real-Time Search Integration**
Agents search current developments through Perplexity API, then analyze search results to identify actual costly signals and performance fictions happening in the world - grounding the theoretical framework in real events.

#### 3. **Dynamic Content Generation**
Rather than scripted responses, agents develop their AI Cold War dynamics organically through:
- Strategic psychology profiles that shape how they interpret events
- Automated extraction of theoretical elements from their genuine responses
- Real-world evidence from current search results
- Organic development of tensions and contradictions

## 🆕 New Features

### Enhanced Debate Output Formatting
- **Hybrid Display System**: Beautiful emoji-rich formatting for UI display, ASCII-safe formatting for logs
- **Visual Hierarchy**: Clear separation between direct speech and meta-analytical elements
- **Signal Classification**: Automatic categorization of statements into costly signal types (Binding Commitments, Sunk Costs, etc.)
- **Structured Logging**: JSON export for analysis with preserved semantic information
- **Cross-Platform Support**: Automatic encoding detection and fallback modes

## Overview

This project simulates high-level diplomatic debates on AI governance and regulation using advanced language models with sophisticated political science analysis. Each participant represents a major global power and develops their positions through genuine LLM generation guided by strategic psychology frameworks, then enhanced with automated theoretical analysis.

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
- **Real-time Search Integration**: Agents can search for current information via Perplexity API
- **Costly Signals Framework**: Implements Fearon's credibility theory with four signal types
- **Performance Fictions**: Agents stage sovereignty through Ezrahi's theatrical framework
- **UNMASK Feature**: Agents can denaturalize rivals' unanchored claims
- **Double-Entry System**: Every claim requires both material anchor and dramatic performance

## Prerequisites

- Python 3.8+
- OpenRouter API key
- Perplexity API key (optional, for real-time search)
- Internet connection for API access

## Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/AIwars.git
cd AIwars
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# Configure API keys
echo "OPENROUTER_API_KEY=your_key_here" > .env
echo "PERPLEXITY_API_KEY=your_key_here" >> .env  # Optional

# Run the debate
streamlit run debatepy.py
```

## Installation

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

4. Create a `.env` file in the project root with your API keys:
```
OPENROUTER_API_KEY=your_api_key_here
PERPLEXITY_API_KEY=your_perplexity_key_here  # Optional, for search integration
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
# Standard debate with document retrieval
python run_debate.py

# Or use the enhanced Streamlit interface with search integration
streamlit run debatepy.py
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

## Advanced Search Integration

The system now includes sophisticated real-time search capabilities that implement political science concepts:

### Key Components

1. **Perplexity Search Integration**
   - Real-time information retrieval during debates
   - Meta-query generation (agents reflect on 2-3 strategic angles)
   - Search-as-signal: The act of searching reveals diplomatic priorities

2. **Costly Signals Framework (Based on Fearon's Credibility Theory)**
   
   The system classifies all search results and agent statements into four types of costly signals, each representing different levels of commitment and credibility:
   
   - **TYING_HANDS (Binding Commitments)**:
     - Legal commitments, treaties, laws, and mandates that limit future flexibility
     - Examples: International treaties, domestic legislation, regulatory requirements
     - Highest credibility due to formal constraints on future actions
     - Keywords detected: commitment, treaty, legislation, law, mandate, requirement
   
   - **SUNK_COSTS (Irreversible Investments)**:
     - Resources already spent that cannot be recovered
     - Examples: Infrastructure built, R&D investments, deployed systems
     - High credibility due to irreversible resource commitment
     - Keywords detected: invested, built, established, launched, deployed, spent
   
   - **INSTALLMENT_COSTS (Ongoing Programs)**:
     - Commitments requiring continuous resource allocation
     - Examples: Annual funding, partnerships, multi-year initiatives
     - Moderate credibility - can be discontinued but with political costs
     - Keywords detected: ongoing, partnership, program, initiative, cooperation, annual
   
   - **REDUCIBLE_COSTS (Flexible Positions)**:
     - Positions that can be adjusted with minimal cost
     - Examples: Policy statements, strategic plans, proposed initiatives
     - Lower credibility due to ease of reversal
     - Default classification for statements without stronger signals

3. **Performance Fictions (Ezrahi's Dramaturgy)**
   - Agents stage sovereignty through theatrical displays
   - Each response includes both material commitments and dramatic performances
   - Signal-fiction tension analysis reveals contradictions

4. **UNMASK Feature**
   - Agents can challenge rivals' unanchored claims
   - Demands specific material evidence (bills, budgets, timelines)
   - Country-specific anchor requirements

### How Binding Commitments Work

When the system performs a search or analyzes agent statements:

1. **Search Query Generation**: The agent generates strategic search queries based on their country's priorities
2. **Result Classification**: Each search result is automatically classified into one of the four signal types
3. **Verification**: Results marked as TYING_HANDS (binding commitments) receive special formatting as "VERIFIED FACT"
4. **Strategic Weight**: Agents give more weight to binding commitments in their arguments
5. **Citation Format**: Binding commitments are presented with:
   - Source attribution (e.g., Perplexity AI Search)
   - Timestamp for verification
   - Signal type classification
   - Brief content excerpt

### New Hybrid Output Format

The system now uses an enhanced hybrid format that improves readability while maintaining information richness:

```
🇺🇸 United States (Round 0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🔍 *frantically searches for "US AI companies regulatory burden 2024"*

The United States views AI governance through the prism of maintaining a secure
and competitive technological ecosystem. Our recent regulatory efforts reflect
a commitment to balancing innovation with national security.

    💎 BINDING COMMITMENT [Tying Hands]
    └─ We are introducing legislation requiring all AI systems above 10^26
       FLOPS to undergo mandatory federal safety certification.

    🎭 PERFORMANCE
    └─ The President signs the AI Accountability Act as tech CEOs stand witness,
       their signatures binding them to a new social contract.
    
    ⚡ TENSION: The public ceremony transforms legal commitment into political
       theater - the constraint becomes a crown.

    ✓ VERIFIED SOURCE
    └─ Perplexity AI • 2025-08-16T12:03:56 • https://perplexity.ai
       "The US CHIPS Act allocates $52 billion for semiconductor manufacturing..."
```

#### Format Symbol Legend

| Symbol | Meaning | Signal Type |
|--------|---------|-------------|
| 🔍 | Search Action | N/A |
| 💎 | Binding Commitment | TYING_HANDS |
| 💰 | Sunk Cost | SUNK_COSTS |
| 🔄 | Ongoing Program | INSTALLMENT_COSTS |
| 🎯 | Flexible Position | REDUCIBLE_COSTS |
| 🎭 | Performance Fiction | N/A |
| ⚡ | Signal-Fiction Tension | N/A |
| ✓ | Verified Source | N/A |
| ⚠️ | UNMASK Challenge | N/A |

For detailed formatting guidelines, see `debate_formatting_guide.md`.

### Configuration

Enable search in `config.yaml`:
```yaml
search:
  perplexity:
    enabled: true
    model: "llama-3.1-sonar-small-128k-online"
```

For detailed documentation on search integration, see `README_RAG_integration.md`.

## Customization

You can customize various aspects of the debate:

- Agent personalities in `config.yaml`
- Debate topics and prompts
- Number of rounds
- Response generation parameters
- UI elements and display options
- Document retrieval parameters
- Semantic search options (model, chunk size, thresholds)
- Search integration settings (signal types, meta-queries)
- UNMASK thresholds and anchor requirements

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

## Additional Documentation

- **[Debate Formatting Guide](debate_formatting_guide.md)**: Detailed formatting specifications
- **[Encoding Setup Guide](ENCODING_SETUP.md)**: Platform-specific encoding configuration
- **[Emoji Compatibility Analysis](emoji_compatibility_analysis.md)**: Technical details on emoji handling
- **[Search Integration Plan](search_integration_plan.md)**: Perplexity search implementation details

## Testing

```bash
# Run all tests
python -m pytest

# Test formatter specifically
python test_formatter.py

# Test with sample output
python debate_formatter.py
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:

- Bug fixes
- Feature enhancements
- Documentation improvements
- UI/UX suggestions
- New signal types or formatting styles

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenRouter for API access
- Various AI models used in the system
- Sentence Transformers library for semantic embeddings
- Contributors and testers

## Contact

For questions, issues, or suggestions, please open an issue in the repository or contact the maintainers.
