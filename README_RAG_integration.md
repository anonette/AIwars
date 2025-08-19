# RAG (Retrieval-Augmented Generation) Integration for AI Debate System

## Overview

The AI Debate System now includes full RAG (Retrieval-Augmented Generation) capabilities, allowing agents to dynamically reference and cite documents from their knowledge base during debates. This creates more authentic, evidence-based discussions that adapt based on available documents rather than following scripted responses.

## Key Components

### 1. Document Store (`document_retrieval.py`)
- Manages document storage and retrieval
- Supports semantic search using sentence embeddings
- Stores documents in `agent_documents/` directory with agent-specific subdirectories
- Maintains a document index in `agent_documents/document_index.json`

### 2. Document-Enabled Agents (`document_integration.py`)
- `DocumentEnabledDebateAgent` class extends the base `DebateAgent`
- Automatically searches for relevant documents before generating responses
- Includes document citations in responses
- Tracks which documents were used for transparency

### 3. Document Sources

#### `agent_documents/` Directory
- **United_States/**: US policy documents (CHIPS Act, NIST frameworks, etc.)
- **European_Union/**: EU regulations and strategies (AI Act, etc.)
- **Peoples_Republic_of_China/**: Chinese AI governance documents

#### `TEXTS/` Directory
- Additional research papers, analyses, and reports
- Can be loaded into the document store using `load_texts_documents.py`

## How It Works

### Document Processing Pipeline

When documents are loaded (using `load_texts_documents.py`):
1. **PDF Extraction**: The system uses PyPDF2 to extract text from PDF files, preserving page numbers
2. **Text Chunking**: Documents are split into semantic chunks (around 1000 characters) at paragraph boundaries
3. **Embedding Creation**: Each chunk is converted into a vector embedding using the `all-MiniLM-L6-v2` model for semantic search
4. **Storage**: Documents are organized by agent (US, China, EU) in the `agent_documents/` directory

### Document Retrieval Process

When an agent needs to respond during a debate:

1. **Query Formation**: The system combines:
   - The debate topic
   - The last message from another agent
   - Creates a search query like: "climate change policy China's position on carbon emissions"

2. **Dual Search Strategy**:
   - **Semantic Search** (Primary): Uses cosine similarity between query embeddings and document chunk embeddings
   - **Keyword Search** (Fallback): Simple text matching if semantic search fails

3. **Relevance Filtering**:
   - Only searches documents assigned to that specific agent
   - Returns top 3-5 most relevant document chunks
   - Filters by similarity threshold (0.3) to ensure quality

### Integration into Agent Responses

The `DocumentEnabledDebateAgent` class:

```python
# When generating a response:
1. Searches for relevant documents based on the current context
2. Retrieves document snippets (limited to 300 characters each)
3. Augments the agent's personality with document context:
   "Based on your policy documents, consider these relevant points:
   • China's Belt and Road Initiative focuses on... (Source: BRI_Policy.pdf)
   • Economic cooperation through infrastructure... (Source: China_Trade.pdf)"
4. Generates response using this augmented context
5. Adds citations to the response
```

### Example Flow

When the US agent is asked about climate policy:
1. System searches US documents for "climate policy"
2. Finds relevant chunks from uploaded PDFs like "US_Climate_Strategy.pdf"
3. Extracts key points: "The US commits to 50% emission reduction by 2030..."
4. Agent incorporates this into response: "According to our climate strategy, we are committed to a 50% emission reduction by 2030, as outlined in our national policy framework."

### Key Features

- **Agent-Specific Knowledge**: Each agent only accesses their own documents
- **Dynamic Context**: Agents reference different documents based on the topic
- **Source Attribution**: Responses include citations to specific documents
- **Semantic Understanding**: The embedding model understands conceptual relationships, not just keywords
- **Fallback Mechanism**: If document retrieval fails, agents still function with base personalities

## Setting Up RAG

### 1. Ensure Documents Are Loaded

Check if documents are already in the system:
```bash
# Check the document index
cat agent_documents/document_index.json
```

### 2. Load Additional Documents from TEXTS

If you want to load documents from the TEXTS directory:
```bash
python load_texts_documents.py
```

This script will:
- Scan the TEXTS directory for relevant documents
- Assign documents to appropriate agents based on content
- Upload PDFs to the document store
- Create searchable text versions

### 3. Enable RAG in Debates

The system automatically uses RAG if documents are available. The `debatepy.py` file has been updated to:
- Initialize the document store
- Create document-enabled agents
- Fall back to standard agents if documents aren't available

## Configuration

### Simplified Personalities (config.yaml)

The agent personalities have been simplified to be document-driven:

```yaml
agents:
  openai:
    personality: |
      You are a representative of the United States...
      Your primary directive: Generate all positions based on documents...
```

### Document Search Settings

In `document_retrieval.py`:
- `ENABLE_SEMANTIC_SEARCH`: Enable/disable semantic search (default: True)
- `EMBEDDING_MODEL`: Model for embeddings (default: "all-MiniLM-L6-v2")
- `SIMILARITY_THRESHOLD`: Minimum similarity score (default: 0.5)

## Usage Example

When agents debate, they now:

1. **Search documents**: 
   ```
   *searches through document database*
   ```

2. **Quote sources**:
   ```
   As stated in the CHIPS Act (page 15): "Advanced semiconductor manufacturing 
   is critical to national security..."
   ```

3. **Include citations**:
   ```
   _Sources referenced: 'US CHIPS and Science Act' (legislation, p. 15), 
   'NIST AI Standards' (standards, pp. 23-24)._
   ```

## Benefits

1. **Dynamic Responses**: Agents adapt based on available documents
2. **Evidence-Based**: All positions are grounded in actual policy documents
3. **Transparency**: Clear citations show which documents informed each response
4. **Flexibility**: Easy to add new documents to shape agent positions
5. **Authenticity**: More realistic simulation of how nations actually form positions

## Troubleshooting

### No Documents Found
- Check if `agent_documents/document_index.json` exists and contains entries
- Run `python load_texts_documents.py` to load documents
- Verify PDF files are readable and not corrupted

### Semantic Search Not Working
- Install required dependencies: `pip install sentence-transformers torch`
- Check if embedding model downloads successfully
- Set `ENABLE_SEMANTIC_SEARCH = False` in `document_retrieval.py` to use keyword search

### Documents Not Being Used
- Ensure `use_documents=True` in `StreamlitDebateManager` initialization
- Check agent names match directory names (e.g., "United_States" not "United States")
- Verify documents are assigned to correct agents in the index

## Adding New Documents

1. **Manual Upload**: Use `document_uploader.py` Streamlit app
2. **Bulk Upload**: Modify `load_texts_documents.py` to include new patterns
3. **Direct Copy**: Place PDFs in appropriate `agent_documents/[Agent_Name]/` folder and run indexing

## Future Enhancements

- Support for more document formats (DOCX, TXT, MD)
- Real-time document updates during debates
- Cross-agent document sharing for collaborative scenarios
- Document quality scoring and relevance ranking

## Advanced Search Integration (Perplexity API)

### Overview

The AI Debate System now includes real-time search capabilities through Perplexity API integration, implementing sophisticated concepts from political science:

- **Costly Signals (Fearon)**: Agents must pay credibility costs when making commitments
- **Performance Fictions (Ezrahi)**: Agents stage sovereignty through theatrical displays
- **Double-Entry System**: Every claim requires both material anchor and dramatic performance
- **UNMASK Feature**: Agents can denaturalize rivals' pure stagecraft

### Key Components

#### 1. Perplexity Search Client (`perplexity_search.py`)

The search system implements:

- **Meta-Query Generation**: Agents reflect on 2-3 strategic angles before searching
- **Signal Type Classification**: Based on CSET framework (tying hands, sunk costs, installment costs, reducible costs)
- **Poster Hook Generation**: Transforms search results into political imagery
- **Search-as-Signal**: The act of searching becomes a performative diplomatic gesture

```python
# Example meta-query generation
meta_queries = [
    "latest US semiconductor export controls China 2024",
    "Biden administration AI chip restrictions enforcement",
    "impact semiconductor sanctions Chinese AI development"
]
```

#### 2. Search-Enabled Debate Agent (`search_enabled_debate_agent.py`)

Extends `DocumentEnabledDebateAgent` with:

- **Strategic Search Decision**: Determines when to search vs. use documents
- **Double-Entry Response**: Generates both costly signal and performance fiction
- **UNMASK Capability**: Identifies and challenges unanchored claims
- **Multi-Format Citations**: Distinguishes "hard facts" from "performative claims"

### The Double-Entry System

Every agent response now includes:

1. **Costly Signal** (Credibility Ledger):
   - TYING_HANDS: Legal commitments that limit future flexibility
   - SUNK_COSTS: Irreversible investments already made
   - INSTALLMENT_COSTS: Ongoing commitments requiring renewal
   - REDUCIBLE_COSTS: Flexible positions that can be adjusted

2. **Performance Fiction** (Sovereignty Theater):
   - Staging: The physical or institutional setting
   - Spectacle: The dramatic performance
   - Description: How authority is naturalized

3. **Signal-Fiction Tension Analysis**:
   - Evaluates whether signal and fiction reinforce or contradict
   - Identifies when theatrical claims lack material anchors

### UNMASK Feature

Agents can challenge rivals' unanchored claims by demanding specific material evidence:

```
[UNMASK] China's claim to 'guarantee AI safety through comprehensive governance'
operates as pure stagecraft - a performance without material substrate.
Minimum anchors for credibility:
(1) State Council directive number,
(2) Responsible ministry/commission,
(3) Five-Year Plan section reference,
(4) Provincial implementation quotas
```

Each country has specific anchor requirements:
- **US**: Congressional bills, federal agencies, budget allocations, GAO audits
- **China**: State Council directives, ministry assignments, Five-Year Plan references
- **EU**: Commission proposals, Council decisions, member state deadlines, ECJ enforcement

### Search Integration Flow

1. **Context Analysis**: Agent evaluates if current information is needed
2. **Meta-Query Generation**: Reflects on strategic search angles
3. **Search Execution**: Performs search with signal type classification
4. **Result Integration**: Combines search results with document knowledge
5. **Response Generation**: Creates double-entry response with citations

### Configuration

In `config.yaml`:

```yaml
search:
  perplexity:
    enabled: true
    api_key: ${PERPLEXITY_API_KEY}
    model: "llama-3.1-sonar-small-128k-online"
    max_results: 5
    
  signal_types:
    tying_hands:
      keywords: ["legislation", "treaty", "agreement", "law", "regulation"]
    sunk_costs:
      keywords: ["invested", "built", "established", "deployed", "operational"]
    installment_costs:
      keywords: ["annual", "ongoing", "program", "initiative", "funding"]
    reducible_costs:
      keywords: ["considering", "exploring", "may", "could", "potential"]
```

### Usage Example

When agents debate with search enabled:

```
United States: *searches for "latest semiconductor export controls China 2024"*

[SEARCH NARRATION]: The US delegate's fingers move across the tablet with practiced
precision, each keystroke a calculated revelation. The search for "semiconductor
export controls" signals both our technological anxieties and regulatory arsenal.

According to recent developments, the October 2024 restrictions on advanced AI chips...

[COSTLY SIGNAL - SUNK_COSTS]: We've already invested $52 billion through the CHIPS Act,
with Intel's Ohio fabs coming online in 2025.

[PERFORMANCE FICTION]: The President signs the AI Accountability Act as tech CEOs
stand witness, their signatures binding them to a new social contract where
innovation serves democracy.

[SIGNAL-FICTION TENSION]: Physical infrastructure provides the stage for sovereignty
performance - concrete anchors abstract authority.

BINDING COMMITMENTS (Verified Sources):
[1] Reuters (2024-10-15): VERIFIED FACT - https://reuters.com/tech/us-chips-act
[2] ESTABLISHED POLICY - US CHIPS and Science Act
```

### Advanced Features

#### Search-as-Signal Narration

Each search generates theatrical narration revealing diplomatic anxieties:

```python
narration_templates = {
    "defensive": "fingers hover uncertainly before typing '{query}' - the search itself an admission",
    "assertive": "types '{query}' with deliberate keystrokes, each click a sovereign declaration",
    "exploratory": "crafts the query '{query}' like a diplomatic probe, testing the waters"
}
```

#### Poster Hook Generation

High-tension moments generate political poster concepts:

```
[POSTER CONCEPT]:
INSCRIPTIO: "SILICON SOVEREIGNTY"
PICTURA: A microchip transforms into a fortress, its circuits becoming walls,
         its pathways becoming moats. The American eagle perches atop,
         wings spread to shield the technology within.
SUBSCRIPTIO: "Our chips, our rules, our future"
```

#### Citation Formatting

Citations distinguish between binding and flexible claims:

- **Hard Facts** (for TYING_HANDS, SUNK_COSTS):
  `[1] Reuters (2024-10-15): VERIFIED FACT - https://...`

- **Performative Claims** (for INSTALLMENT_COSTS, REDUCIBLE_COSTS):
  `[1] TechCrunch (2024-10-14): STRATEGIC POSITION - https://...`

### Setting Up Search Integration

1. **Add Perplexity API Key**:
   ```bash
   echo "PERPLEXITY_API_KEY=your_api_key_here" >> .env
   ```

2. **Enable Search in Config**:
   - Set `search.perplexity.enabled: true` in `config.yaml`

3. **Initialize Search Client**:
   - The system automatically initializes `PerplexitySearchClient` when enabled

### Benefits of Search Integration

1. **Real-Time Information**: Access to latest developments during debates
2. **Strategic Signaling**: Search queries reveal diplomatic priorities
3. **Theatrical Depth**: Combines hard facts with sovereignty performances
4. **Accountability**: UNMASK feature prevents empty rhetoric
5. **Dynamic Tensions**: Exposes contradictions between signals and fictions

### Troubleshooting Search

#### API Key Issues
- Verify `.env` file contains valid `PERPLEXITY_API_KEY`
- Check API key permissions and rate limits

#### Search Not Working
- Ensure `search.perplexity.enabled: true` in config
- Check network connectivity
- Verify Perplexity API status

#### No Search Results
- Try broader search terms
- Check if rate limits are exceeded
- Verify search triggers in agent messages

### Theory References

- **Costly Signals**: Fearon, J. (1997). "Signaling Foreign Policy Interests"
- **Performance Fictions**: Ezrahi, Y. (1990). "The Descent of Icarus"
- **CSET Framework**: Center for Security and Emerging Technology signal types
- **Double-Entry System**: Combines material commitments with theatrical sovereignty