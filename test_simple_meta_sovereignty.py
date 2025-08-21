"""
Simple test for meta-sovereignty analysis
"""

import asyncio
import logging
import yaml
from enhanced_search_integration import TheoreticallyEnhancedAgent, EnhancedDocumentStore
from dataclasses import dataclass

# Configure logging to show all messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class MockSearchResult:
    """Mock search result with proper structure"""
    source: str
    content: str

async def test_simple():
    """Simple test of the analysis components"""
    
    print("Starting Meta-Sovereignty Analysis Test")
    print("=" * 80)
    
    try:
        # Load config with UTF-8 encoding
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print("✓ Config loaded successfully")
    except Exception as e:
        print(f"✗ Error loading config: {e}")
        return
    
    try:
        # Create enhanced document store
        store = EnhancedDocumentStore()
        print(f"✓ Enhanced document store created with {len(store.theoretical_resources)} resources")
    except Exception as e:
        print(f"✗ Error creating document store: {e}")
        return
    
    try:
        # Create test agent
        test_agent = TheoreticallyEnhancedAgent(
            name="Test Agent",
            personality="Analytical test agent",
            agent_config_key="openai",
            config=config,
            document_store=store
        )
        print("✓ Test agent created successfully")
    except Exception as e:
        print(f"✗ Error creating test agent: {e}")
        return
    
    # Test statement
    test_statement = """
    The United States believes in democratic AI governance with innovation at its core.
    We support transparency and ethical frameworks while maintaining competitive advantage.
    """
    
    # Mock search results with proper structure
    mock_search_results = {
        "results": [
            MockSearchResult(
                source="Policy Update",
                content="US rebrands AI Safety Institute to Center for AI Standards and Innovation"
            ),
            MockSearchResult(
                source="Investment News", 
                content="$52 billion allocated for domestic chip manufacturing"
            )
        ]
    }
    
    print("\nTesting individual analysis components:")
    print("-" * 80)
    
    # Test Ezrahi analysis
    try:
        print("\n1. Generating Ezrahi Analysis...")
        ezrahi = await test_agent._generate_ezrahi_analysis(
            test_statement, "", "AI governance", mock_search_results
        )
        if ezrahi:
            print("✓ Ezrahi analysis generated")
            print(f"Preview: {ezrahi[:200]}...")
        else:
            print("✗ Ezrahi analysis empty")
    except Exception as e:
        print(f"✗ Error in Ezrahi analysis: {e}")
        import traceback
        traceback.print_exc()
        ezrahi = ""
    
    # Test Fearon analysis
    try:
        print("\n2. Generating Fearon Analysis...")
        fearon = await test_agent._generate_fearon_analysis(
            test_statement, mock_search_results
        )
        if fearon:
            print("✓ Fearon analysis generated")
            print(f"Preview: {fearon[:200]}...")
        else:
            print("✗ Fearon analysis empty")
    except Exception as e:
        print(f"✗ Error in Fearon analysis: {e}")
        import traceback
        traceback.print_exc()
        fearon = ""
    
    # Test Meta-sovereignty analysis
    try:
        print("\n3. Generating Meta-Sovereignty Analysis...")
        meta_sov = await test_agent._generate_meta_sovereignty_analysis(
            test_statement, ezrahi, fearon, mock_search_results
        )
        if meta_sov:
            print("✓ Meta-sovereignty analysis generated")
            print(f"Preview: {meta_sov[:200]}...")
        else:
            print("✗ Meta-sovereignty analysis empty")
    except Exception as e:
        print(f"✗ Error in Meta-sovereignty analysis: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("Test completed!")

if __name__ == "__main__":
    asyncio.run(test_simple())