"""
Test Ezrahi-style analysis of political fictions in AI policy
"""

import asyncio
import logging
from enhanced_search_integration import TheoreticallyEnhancedAgent, EnhancedDocumentStore
from perplexity_search import PerplexitySearchClient, SearchResult, SignalType

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def test_ezrahi_political_fictions():
    """Test Ezrahi's analysis of political fictions in AI policy"""
    
    print("="*60)
    print("TESTING EZRAHI'S ANALYSIS OF POLITICAL FICTIONS")
    print("="*60)
    
    # Create minimal agent
    agent = TheoreticallyEnhancedAgent(
        name="Test Agent",
        personality="Test",
        agent_config_key="openai",
        config={}
    )
    
    # Test cases with different AI policy statements
    test_cases = [
        {
            "statement": "The United States champions democratic AI governance through innovation and ethical frameworks.",
            "search_results": {
                "results": [
                    SearchResult(
                        query="US AI policy",
                        content="The US AI Safety Institute has been rebranded as the Center for AI Standards and Innovation, shifting focus from safety to innovation and competitiveness.",
                        source="TechPolicy News",
                        url="https://example.com/1",
                        timestamp="2024-01-15",
                        signal_type=SignalType.TYING_HANDS
                    ),
                    SearchResult(
                        query="US AI policy",
                        content="Executive orders accelerate federal permitting for large-scale data centers, prioritizing infrastructure over environmental reviews.",
                        source="Government Executive",
                        url="https://example.com/2",
                        timestamp="2024-01-16",
                        signal_type=SignalType.SUNK_COSTS
                    )
                ]
            },
            "description": "US democratic AI governance claim"
        },
        {
            "statement": "We ensure transparent and accountable AI development for all citizens.",
            "search_results": {
                "results": [
                    SearchResult(
                        query="AI transparency",
                        content="New AI systems deployed without public disclosure, citing national security concerns. Transparency requirements waived for defense applications.",
                        source="AI Watch",
                        url="https://example.com/3",
                        timestamp="2024-01-17",
                        signal_type=SignalType.REDUCIBLE_COSTS
                    )
                ]
            },
            "description": "Transparency claim"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n{'='*60}")
        print(f"Test Case {i+1}: {test_case['description']}")
        print(f"{'='*60}")
        
        print(f"Policy Statement: \"{test_case['statement']}\"")
        print("\nSearch Results:")
        for j, result in enumerate(test_case['search_results']['results']):
            print(f"{j+1}. {result.source}: {result.content[:100]}...")
        
        try:
            # Generate Ezrahi analysis
            theoretical_context = """
- Yaron Ezrahi: Imagined Democracies (political_imaginaries)
  Keywords: necessary fictions, democratic legitimacy, transparency, performance
"""
            
            analysis = await agent._generate_theoretical_enhancement(
                base_response=test_case['statement'],
                theoretical_context=theoretical_context,
                topic="AI governance",
                search_results=test_case['search_results']
            )
            
            print(f"\nEzrahi's Analysis:")
            print("-"*60)
            if analysis:
                print(analysis)
                
                # Check for key Ezrahi concepts
                ezrahi_concepts = [
                    'political fiction', 'necessary fiction', 'imaginary', 'imaginaries',
                    'performance', 'legitimacy', 'transparency', 'democratic', 
                    'myth', 'theater', 'theatrical', 'spectacle'
                ]
                
                found_concepts = [c for c in ezrahi_concepts if c.lower() in analysis.lower()]
                
                if found_concepts:
                    print(f"\n✅ Found Ezrahi concepts: {', '.join(found_concepts)}")
                else:
                    print("\n⚠️ No specific Ezrahi concepts found")
                    
                # Check if it analyzes the search results
                if any(result.source in analysis for result in test_case['search_results']['results']):
                    print("✅ Analysis references search results")
                else:
                    print("⚠️ Analysis doesn't reference search results")
                    
            else:
                print("❌ No analysis generated")
            print("-"*60)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

async def test_direct_ezrahi_prompt():
    """Test the Ezrahi prompt directly"""
    
    print("\n" + "="*60)
    print("TESTING DIRECT EZRAHI PROMPT")
    print("="*60)
    
    # Create the exact prompt that would be sent
    prompt = """You are Yaron Ezrahi, the political theorist who wrote "Imagined Democracies: Necessary Political Fictions." You are analyzing AI policy statements and search results to identify the political fictions at work.

DIPLOMATIC STATEMENT: "The United States champions democratic AI governance through innovation and ethical frameworks."

SEARCH RESULTS ON AI POLICY:

1. From TechPolicy News: The US AI Safety Institute has been rebranded as the Center for AI Standards and Innovation, shifting focus from safety to innovation and competitiveness...
2. From Government Executive: Executive orders accelerate federal permitting for large-scale data centers, prioritizing infrastructure over environmental reviews...

As Ezrahi, you understand that modern democracies rely on "necessary political fictions" - shared imaginaries that make democratic governance possible. These fictions include:
- The myth of transparent governance
- The performance of democratic deliberation
- The fiction of citizen control over technology
- The imaginary of rational policy-making

Analyze the above AI policy statement and search results. Identify:
1. What political fictions are being deployed to legitimize AI governance?
2. How do these fictions mask the actual power relations and technical complexities?
3. What performances of democracy are being enacted through these policy statements?

Write as Ezrahi would - revealing how political imaginaries operate in AI governance discourse."""
    
    print("Prompt that positions LLM as Ezrahi:")
    print("-"*60)
    print(prompt)
    print("-"*60)
    
    print("\nExpected type of response:")
    print("- Identifies specific political fictions (e.g., 'democratic AI governance')")
    print("- Analyzes how search results contradict the stated fictions")
    print("- Reveals the performance aspects of policy statements")
    print("- Uses Ezrahi's theoretical framework naturally")

if __name__ == "__main__":
    asyncio.run(test_ezrahi_political_fictions())
    asyncio.run(test_direct_ezrahi_prompt())