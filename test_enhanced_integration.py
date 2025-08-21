"""
Test Enhanced Theoretical Integration
"""

import asyncio
import logging
from enhanced_search_integration import (
    EnhancedDocumentStore, 
    TheoreticallyEnhancedAgent,
    test_theoretical_integration
)
import yaml

async def test_enhanced_system():
    """Test the enhanced system with real theoretical resources"""
    
    print("=== TESTING ENHANCED THEORETICAL INTEGRATION ===\n")
    
    # Test 1: Enhanced Document Store
    print("1. Testing Enhanced Document Store...")
    await test_theoretical_integration()
    print()
    
    # Test 2: Create Enhanced Agent
    print("2. Testing TheoreticallyEnhancedAgent...")
    
    # Load config
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except:
        config = {'US_config': {'personality': 'US representative'}}
    
    # Create enhanced agent
    agent = TheoreticallyEnhancedAgent(
        name="United_States",
        personality="US representative focused on technological leadership and democratic values",
        agent_config_key="US_config",
        config=config
    )
    
    print(f"Created agent with access to {len(agent.document_store.theoretical_resources)} theoretical resources")
    
    # Test 3: Generate Response with Theoretical Analysis
    print("\n3. Testing Response Generation with Theoretical Enhancement...")
    
    test_context = """
    AI governance debate on technological sovereignty. Topic: Democratic oversight of AI systems.
    Previous round discussed the need for transparent AI governance frameworks.
    """
    
    test_message = "European_Union: We propose mandatory algorithmic auditing to ensure democratic accountability in AI systems."
    
    # This should now include theoretical analysis using Ezrahi's framework
    response = await agent.generate_response(test_context, test_message)
    
    print("GENERATED RESPONSE:")
    print("-" * 50)
    print(response)
    print("-" * 50)
    
    # Check if theoretical analysis was included
    if "[THEORETICAL ANALYSIS]" in response:
        print("✅ SUCCESS: Theoretical analysis included in response")
    else:
        print("⚠️  Note: No theoretical analysis markers found (may still contain enhanced content)")
    
    print(f"\n📚 Theoretical resources used: {agent.last_used_theoretical_resources}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_enhanced_system())
