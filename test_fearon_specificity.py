"""
Test the enhanced Fearon analysis with specific signal types
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

async def test_fearon_specificity():
    """Test Fearon's specific signal type analysis"""
    
    print("Testing Enhanced Fearon Analysis with Specific Signal Types")
    print("=" * 80)
    
    # Load config
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Create enhanced document store
    store = EnhancedDocumentStore()
    
    # Check if Fearon resources were loaded
    fearon_resources = [r for r in store.theoretical_resources if "Fearon" in r.author]
    print(f"\nLoaded {len(fearon_resources)} Fearon theoretical resources:")
    for resource in fearon_resources:
        print(f"  - {resource.title} (Priority: {resource.priority})")
        print(f"    Keywords: {', '.join(resource.keywords)}")
    
    # Create test agent
    test_agent = TheoreticallyEnhancedAgent(
        name="United States",
        personality="US representative focused on technological leadership",
        agent_config_key="openai",
        config=config,
        document_store=store
    )
    
    # Test statement
    test_statement = """
    The United States is committed to maintaining AI leadership through strategic investments
    and partnerships with democratic allies while ensuring responsible development.
    """
    
    # Rich mock search results with various signal types
    mock_search_results = {
        "results": [
            MockSearchResult(
                source="Congressional CHIPS and Science Act 2022",
                content="Congress authorized $280 billion total, with $52.7 billion in direct semiconductor subsidies, $39 billion for manufacturing incentives, $13.2 billion for R&D. Intel receives $8.5 billion for new fabs in Ohio and Arizona. Construction has begun, creating 10,000 jobs. Funds cannot be clawed back once construction starts."
            ),
            MockSearchResult(
                source="White House AI Executive Order Oct 2023",
                content="President Biden signed sweeping AI executive order requiring safety assessments for models above 10^26 FLOPS. Order establishes AI Safety Institute, mandates federal agencies adopt AI, creates Chief AI Officers. Reversal would require new president to publicly abandon AI safety, facing backlash from tech industry and allies."
            ),
            MockSearchResult(
                source="State Department AUKUS AI Cooperation 2024",
                content="US-UK-Australia announce AI military cooperation under AUKUS Pillar 2. Includes sharing of AI algorithms for submarine detection, $2 billion joint research fund, reciprocal access to compute facilities. Treaty ratified by Senate 67-33, withdrawal requires 2/3 vote."
            ),
            MockSearchResult(
                source="Commerce Department AI Chip Export Controls",
                content="New export controls ban AI chips above certain thresholds to China. Nvidia stock dropped 7%, US semiconductor industry lobbied against. Administration proceeded despite $10 billion estimated annual revenue loss to US companies. Controls expanded three times despite industry opposition."
            ),
            MockSearchResult(
                source="NSF National AI Research Resource 2024",
                content="Congress funds National AI Research Resource with $2.6 billion over 5 years. Provides compute access to universities, with sustained annual appropriations. 127 universities enrolled, 10,000 researchers registered. Program has bipartisan support, embedded in multiple appropriations bills."
            )
        ]
    }
    
    print("\nGenerating Fearon Analysis with Specific Signal Types...")
    print("-" * 80)
    
    # Test Fearon analysis
    fearon = await test_agent._generate_fearon_analysis(
        test_statement, mock_search_results
    )
    
    if fearon:
        print(fearon)
        
        # Check if specific signal types are mentioned
        signal_types = ["SUNK COST", "TYING HANDS", "AUDIENCE COST", "INSTALLMENT COST", "OPPORTUNITY COST"]
        print("\n" + "-" * 80)
        print("Signal Type Coverage:")
        for signal_type in signal_types:
            if signal_type in fearon:
                print(f"  ✓ {signal_type} - Found in analysis")
            else:
                print(f"  ✗ {signal_type} - Not identified")
    else:
        print("No Fearon analysis generated")
    
    print("\n" + "=" * 80)
    print("Analysis should now identify specific Fearon signal types with theoretical grounding")

if __name__ == "__main__":
    asyncio.run(test_fearon_specificity())