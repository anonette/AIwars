"""Test script to verify search-first workflow for geopolitical agents"""

import asyncio
import logging
from datetime import datetime
from enhanced_search_integration import TheoreticallyEnhancedAgent
from perplexity_search import PerplexitySearchClient
from config import load_config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_search_first_workflow():
    """Test that agents search for recent initiatives before consulting documents"""
    
    # Load configuration
    config = load_config()
    
    # Initialize search client
    search_client = PerplexitySearchClient(config['perplexity_api_key'])
    
    # Create test agent (EU)
    agent = TheoreticallyEnhancedAgent(
        name="EU",
        personality="You are the European Union representative, focused on ethical AI and regulatory frameworks.",
        agent_config_key="eu_agent",
        search_client=search_client,
        document_store=None  # Will be mocked
    )
    
    # Test context
    context = "The debate is about AI governance and regulation frameworks."
    last_message = "How is your country approaching AI safety and regulation?"
    
    print("\n" + "="*80)
    print("TESTING SEARCH-FIRST WORKFLOW")
    print("="*80)
    
    # Generate response
    print(f"\nGenerating response for {agent.name}...")
    response = await agent.generate_response(context, last_message)
    
    # Check if response contains references to recent initiatives
    print(f"\n{agent.name} Response:")
    print("-" * 40)
    print(response[:500] + "..." if len(response) > 500 else response)
    
    # Verify search was performed
    print("\n" + "-"*40)
    print("VERIFICATION:")
    print("-" * 40)
    
    # Check for search result indicators
    search_indicators = [
        "2024", "2025", "recent", "initiative", "launched", "announced",
        "AI Act", "regulation", "framework", "investment"
    ]
    
    found_indicators = [ind for ind in search_indicators if ind.lower() in response.lower()]
    print(f"✓ Found search indicators: {found_indicators}")
    
    # Check for document references
    doc_indicators = [
        "policy", "position", "framework", "approach", "strategy"
    ]
    
    found_doc_indicators = [ind for ind in doc_indicators if ind.lower() in response.lower()]
    print(f"✓ Found document indicators: {found_doc_indicators}")
    
    # Check for sources section
    if "Sources:" in response:
        print("✓ Sources section found")
        sources_start = response.find("Sources:")
        sources_section = response[sources_start:sources_start+200]
        print(f"  Preview: {sources_section}...")
    else:
        print("✗ No sources section found")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)

async def test_multiple_agents():
    """Test search-first workflow for multiple agents"""
    
    # Load configuration
    config = load_config()
    
    # Initialize search client
    search_client = PerplexitySearchClient(config['perplexity_api_key'])
    
    # Create agents
    agents = [
        TheoreticallyEnhancedAgent(
            name="US",
            personality="You are the United States representative, focused on innovation and competitiveness.",
            agent_config_key="us_agent",
            search_client=search_client
        ),
        TheoreticallyEnhancedAgent(
            name="China",
            personality="You are the China representative, focused on technological sovereignty.",
            agent_config_key="china_agent",
            search_client=search_client
        ),
        TheoreticallyEnhancedAgent(
            name="EU",
            personality="You are the European Union representative, focused on ethical AI and regulation.",
            agent_config_key="eu_agent",
            search_client=search_client
        )
    ]
    
    context = "The debate is about AI governance and international cooperation."
    last_message = "What recent AI initiatives has your country launched?"
    
    print("\n" + "="*80)
    print("TESTING MULTIPLE AGENTS - SEARCH-FIRST WORKFLOW")
    print("="*80)
    
    for agent in agents:
        print(f"\n\n{'='*40}")
        print(f"Testing {agent.name}")
        print('='*40)
        
        response = await agent.generate_response(context, last_message)
        
        # Show first 300 chars
        print(f"\nResponse preview:")
        print(response[:300] + "...")
        
        # Check for recent dates
        recent_dates = ["2024", "2025"]
        found_dates = [d for d in recent_dates if d in response]
        print(f"\n✓ Found recent dates: {found_dates}")
        
        # Check for sources
        has_sources = "Sources:" in response
        print(f"✓ Has sources section: {has_sources}")
        
        await asyncio.sleep(1)  # Rate limiting

if __name__ == "__main__":
    # Run single agent test
    asyncio.run(test_search_first_workflow())
    
    # Run multiple agents test
    asyncio.run(test_multiple_agents())