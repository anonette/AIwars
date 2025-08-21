"""Simple test to verify search-first workflow"""

import asyncio
import logging
from search_enabled_debate_agent import SearchEnabledDebateAgent
from perplexity_search import PerplexitySearchClient
from config import load_config

logging.basicConfig(level=logging.INFO)

async def test_simple_workflow():
    """Test that base agent always uses both search and documents"""
    
    config = load_config()
    search_client = PerplexitySearchClient(config['perplexity_api_key'])
    
    # Create a simple search-enabled agent
    agent = SearchEnabledDebateAgent(
        name="TestAgent",
        personality="You are a test agent.",
        agent_config_key="test_agent",
        search_client=search_client
    )
    
    # Test the decision method
    decision = await agent._decide_information_source("AI governance", "test message", "test context")
    print(f"Decision method returns: {decision}")
    assert decision == "both", f"Expected 'both', got '{decision}'"
    
    # Test response generation
    context = "Discussion about AI safety"
    last_message = "What are your country's recent AI initiatives?"
    
    print("\nGenerating response...")
    response = await agent.generate_response(context, last_message)
    
    print("\nResponse preview:")
    print(response[:500] + "..." if len(response) > 500 else response)
    
    # Check for indicators
    if "recent" in response.lower() or "initiative" in response.lower():
        print("\n✓ Response mentions recent initiatives")
    
    if "Sources:" in response:
        print("✓ Response includes sources")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_simple_workflow())