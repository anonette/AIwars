"""
Test the search results formatting in theoretical analysis
"""

import asyncio
import logging
import yaml
from enhanced_search_integration import TheoreticallyEnhancedAgent, EnhancedDocumentStore
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class MockSearchResult:
    """Mock search result with proper structure"""
    source: str
    content: str

async def test_search_formatting():
    """Test the search results formatting"""
    
    print("Testing Search Results Formatting in Theoretical Analysis")
    print("=" * 80)
    
    # Load config
    with open('config.yaml', 'r', encoding='utf-8') as f:
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
    
    # Test statement
    test_statement = """
    The United States commits to democratic AI governance through innovation-driven frameworks.
    We will ensure transparent development while maintaining competitive technological leadership.
    Our approach balances ethical considerations with the imperative of technological advancement.
    """
    
    # Mock search results with varied content
    mock_search_results = {
        "results": [
            MockSearchResult(
                source="White House AI Executive Order 2024",
                content="The administration announces a shift in AI policy focus from safety-first to innovation-driven approach. The AI Safety Institute has been rebranded as the Center for AI Standards and Innovation, signaling a strategic pivot toward market-led solutions and voluntary industry standards rather than mandatory regulatory frameworks."
            ),
            MockSearchResult(
                source="Congressional CHIPS Act Funding Report",
                content="$52 billion allocated for domestic semiconductor manufacturing, with $39 billion in direct subsidies to companies like Intel and TSMC. Additional $13 billion for R&D and workforce development. This represents the largest industrial policy investment in US history, aimed at reducing dependence on Asian chip suppliers."
            ),
            MockSearchResult(
                source="State Department AI Diplomacy Brief",
                content="US pursuing bilateral AI agreements with key allies while avoiding multilateral frameworks. Focus on 'friend-shoring' AI supply chains and creating exclusive technology sharing arrangements with Five Eyes partners. Emphasis on maintaining technological advantage over strategic competitors."
            ),
            MockSearchResult(
                source="NIST AI Risk Management Framework",
                content="New voluntary AI risk framework emphasizes self-assessment and industry-led standards. Unlike EU's mandatory compliance approach, US framework relies on market incentives and reputational mechanisms. Companies can choose their own risk tolerance levels within broad guidelines."
            ),
            MockSearchResult(
                source="Pentagon AI Strategy Document",
                content="Department of Defense accelerating AI integration with $1.8 billion annual investment. Focus on maintaining decision advantage through AI-enabled systems. Explicit acknowledgment that AI superiority is critical to deterrence strategy. Partnerships with tech companies prioritized over regulatory constraints."
            )
        ]
    }
    
    print("\nGenerating Ezrahi Analysis with Formatted Search Results...")
    print("-" * 80)
    
    # Test Ezrahi analysis
    ezrahi = await test_agent._generate_ezrahi_analysis(
        test_statement, "", "AI governance", mock_search_results
    )
    
    if ezrahi:
        print(ezrahi)
    else:
        print("No Ezrahi analysis generated")
    
    print("\n" + "=" * 80)
    print("Search results should now appear as a clear, formatted list")
    print("Each result shows SOURCE and CONTENT clearly separated")

if __name__ == "__main__":
    asyncio.run(test_search_formatting())