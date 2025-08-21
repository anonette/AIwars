"""
Test the meta-sovereignty analysis implementation
"""

import asyncio
import logging
import yaml
from enhanced_search_integration import TheoreticallyEnhancedAgent, EnhancedDocumentStore
from perplexity_search import PerplexitySearchClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def test_meta_sovereignty_analysis():
    """Test the complete theoretical analysis pipeline"""
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Create enhanced document store
    store = EnhancedDocumentStore()
    
    # Create search client
    search_client = PerplexitySearchClient(api_key=config.get('perplexity_api_key'))
    
    # Create US agent with enhanced capabilities
    us_agent = TheoreticallyEnhancedAgent(
        name="United States",
        personality=config['agents']['openai']['personality'],
        agent_config_key="openai",
        config=config,
        document_store=store,
        search_client=search_client
    )
    
    # Test context
    context = """
    The debate topic is: AI Governance and Global Cooperation
    
    Previous discussion has focused on the balance between innovation and safety in AI development.
    """
    
    last_message = "The European Union emphasizes the need for democratic AI governance with strong ethical frameworks."
    
    print("Generating US response with full theoretical analysis...")
    print("=" * 80)
    
    # Generate response
    response = await us_agent.generate_response(context, last_message)
    
    print(response)
    print("=" * 80)
    
    # Verify all three analyses are present
    analyses_present = {
        "Ezrahi": "[EZRAHI'S ANALYSIS OF POLITICAL FICTIONS]" in response,
        "Fearon": "[FEARON'S COSTLY SIGNAL ANALYSIS]" in response,
        "Meta-Sovereignty": "[META-SOVEREIGNTY ANALYSIS: SIGNALS AND IMAGINARIES]" in response
    }
    
    print("\nAnalysis Components Present:")
    for analysis, present in analyses_present.items():
        print(f"  {analysis}: {'✓' if present else '✗'}")
    
    return all(analyses_present.values())

async def test_individual_analyses():
    """Test each analysis component individually"""
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Create enhanced document store
    store = EnhancedDocumentStore()
    
    # Create test agent
    test_agent = TheoreticallyEnhancedAgent(
        name="Test Agent",
        personality="Analytical test agent",
        agent_config_key="openai",
        config=config,
        document_store=store
    )
    
    # Test diplomatic statement
    test_statement = """
    Ladies and gentlemen, as we stand at the forefront of the AI era, the United States 
    believes in a future where AI development is both democratic and innovative. While we 
    understand the need to bridge the AI divide, we emphasize that equitable access should 
    not come at the expense of stifling innovation or compromising security.
    """
    
    # Mock search results
    mock_search_results = {
        "results": [
            {
                "source": "US AI Policy Update",
                "content": "The U.S. AI Safety Institute has been rebranded to the Center for AI Standards and Innovation, signaling a shift from safety-first to innovation-focused approach."
            },
            {
                "source": "CHIPS Act Implementation",
                "content": "The US has allocated $52 billion for domestic semiconductor manufacturing, aiming to reduce dependence on foreign chip supplies."
            },
            {
                "source": "AI Executive Order Analysis",
                "content": "New executive order emphasizes voluntary industry standards over mandatory regulations, prioritizing market-driven solutions."
            }
        ]
    }
    
    print("\n1. Testing Ezrahi Analysis...")
    print("-" * 40)
    ezrahi = await test_agent._generate_ezrahi_analysis(
        test_statement, "", "AI governance", mock_search_results
    )
    print(ezrahi[:500] + "..." if len(ezrahi) > 500 else ezrahi)
    
    print("\n2. Testing Fearon Analysis...")
    print("-" * 40)
    fearon = await test_agent._generate_fearon_analysis(
        test_statement, mock_search_results
    )
    print(fearon[:500] + "..." if len(fearon) > 500 else fearon)
    
    print("\n3. Testing Meta-Sovereignty Analysis...")
    print("-" * 40)
    meta_sov = await test_agent._generate_meta_sovereignty_analysis(
        test_statement, ezrahi, fearon, mock_search_results
    )
    print(meta_sov[:500] + "..." if len(meta_sov) > 500 else meta_sov)

async def main():
    """Run all tests"""
    print("Testing Meta-Sovereignty Implementation")
    print("=" * 80)
    
    # Test individual components
    await test_individual_analyses()
    
    print("\n" + "=" * 80)
    print("Testing Full Integration")
    print("=" * 80)
    
    # Test full integration
    success = await test_meta_sovereignty_analysis()
    
    if success:
        print("\n✓ All tests passed! Meta-sovereignty analysis is working correctly.")
    else:
        print("\n✗ Some analyses are missing. Check the implementation.")

if __name__ == "__main__":
    asyncio.run(main())