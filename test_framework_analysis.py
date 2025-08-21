"""
Test script to verify the LLM framework analysis is working correctly
"""

import asyncio
import logging
from search_enabled_debate_agent import SearchEnabledDebateAgent
from perplexity_search import PerplexitySearchClient
from document_retrieval import DocumentStore

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def test_framework_analysis():
    """Test the framework analysis with improved prompts"""
    
    # Initialize components
    document_store = DocumentStore()
    search_client = PerplexitySearchClient()
    
    # Create test agent
    agent = SearchEnabledDebateAgent(
        name="United States",
        personality="Representative of US interests in AI governance",
        agent_config_key="openai",
        config={},
        document_store=document_store,
        search_client=search_client
    )
    
    # Test context
    context = "The debate is about AI governance and international cooperation."
    last_message = "China: We commit to establishing comprehensive AI safety standards."
    topic = "AI Governance"
    
    # Mock search results with proper SearchResult objects
    from perplexity_search import SearchResult, SignalType
    mock_search_results = {
        "results": [SearchResult(
            query="test query",
            content="The US has announced a $500 million investment in AI safety research through NIST.",
            source="Reuters",
            url="https://example.com",
            timestamp="2024-01-15",
            signal_type=SignalType.SUNK_COSTS
        )]
    }
    
    # Test the meta-sovereignty analysis prompt creation
    base_response = "The United States remains committed to democratic AI governance."
    
    prompt = agent._create_meta_sovereignty_analysis_prompt(
        base_response=base_response,
        context=context,
        topic=topic,
        search_results=mock_search_results,
        doc_context=""
    )
    
    print("Generated Analysis Prompt:")
    print("-" * 80)
    print(prompt)
    print("-" * 80)
    
    # Test the framework analysis
    print("\nTesting Framework Analysis...")
    analysis = await agent._generate_llm_framework_analysis(prompt)
    
    print("\nAnalysis Result:")
    print("-" * 80)
    print(analysis)
    print("-" * 80)
    
    # Check if analysis contains required markers
    if analysis:
        has_signal = '[COSTLY SIGNAL' in analysis
        has_fiction = '[PERFORMANCE FICTION' in analysis
        has_tension = '[SIGNAL-FICTION' in analysis
        
        print(f"\nValidation Results:")
        print(f"Has Costly Signal: {has_signal}")
        print(f"Has Performance Fiction: {has_fiction}")
        print(f"Has Signal-Fiction Tension: {has_tension}")
        
        if has_signal and has_fiction and has_tension:
            print("\n✅ Framework analysis generated successfully!")
        else:
            print("\n❌ Framework analysis missing required components")
    else:
        print("\n❌ Framework analysis returned empty")

if __name__ == "__main__":
    asyncio.run(test_framework_analysis())