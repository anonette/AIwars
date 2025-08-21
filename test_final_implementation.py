"""Final comprehensive test of the search-first workflow with all features"""

import asyncio
import logging
from enhanced_search_integration import TheoreticallyEnhancedAgent
from perplexity_search import PerplexitySearchClient
from config import load_config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_final_implementation():
    """Test the complete implementation with all features"""
    
    # Load configuration
    config = load_config()
    
    # Initialize search client
    search_client = PerplexitySearchClient(config['perplexity_api_key'])
    
    # Create EU agent
    agent = TheoreticallyEnhancedAgent(
        name="EU",
        personality="You are the European Union representative, focused on ethical AI and regulatory frameworks.",
        agent_config_key="eu_agent",
        search_client=search_client
    )
    
    # Test context
    context = "The debate is about AI governance and international cooperation."
    last_message = "How is your country implementing AI safety measures and what recent initiatives have you launched?"
    
    print("\n" + "="*80)
    print("FINAL IMPLEMENTATION TEST")
    print("="*80)
    
    # Generate response
    print(f"\nGenerating response for {agent.name}...")
    response = await agent.generate_response(context, last_message)
    
    print(f"\n{agent.name} Response:")
    print("-" * 80)
    print(response)
    print("-" * 80)
    
    # Verification checks
    print("\nVERIFICATION:")
    print("-" * 40)
    
    # Check for recent dates
    recent_dates = ["2024", "2025"]
    found_dates = [d for d in recent_dates if d in response]
    print(f"✓ Found recent dates: {found_dates}")
    
    # Check for specific initiatives
    initiatives = ["AI Act", "Digital", "regulation", "framework", "initiative"]
    found_initiatives = [i for i in initiatives if i.lower() in response.lower()]
    print(f"✓ Found initiatives/policies: {found_initiatives}")
    
    # Check for sources section
    has_sources = "Sources:" in response
    print(f"✓ Has sources section: {has_sources}")
    
    # Check for theoretical analysis
    has_ezrahi = "political fiction" in response.lower() or "necessary fiction" in response.lower()
    print(f"✓ Has Ezrahi analysis: {has_ezrahi}")
    
    has_fearon = "costly signal" in response.lower() or "credible commitment" in response.lower()
    print(f"✓ Has Fearon analysis: {has_fearon}")
    
    has_meta_sovereignty = "meta-sovereignty" in response.lower() or "sovereignty" in response.lower()
    print(f"✓ Has meta-sovereignty analysis: {has_meta_sovereignty}")
    
    # Check for action phrases (should be none)
    action_phrases = ["*adjusts", "*straightens", "*nods", "*clears"]
    found_actions = [a for a in action_phrases if a in response]
    if found_actions:
        print(f"✗ Found action phrases that should be stripped: {found_actions}")
    else:
        print("✓ No action phrases found (correctly stripped)")
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY:")
    print("="*80)
    
    all_checks = [
        ("Recent dates", bool(found_dates)),
        ("Initiatives/policies", bool(found_initiatives)),
        ("Sources section", has_sources),
        ("Ezrahi analysis", has_ezrahi),
        ("Fearon analysis", has_fearon),
        ("Meta-sovereignty", has_meta_sovereignty),
        ("Action phrases stripped", not bool(found_actions))
    ]
    
    passed = sum(1 for _, result in all_checks if result)
    total = len(all_checks)
    
    print(f"Passed: {passed}/{total} checks")
    
    for check_name, result in all_checks:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {check_name}")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_final_implementation())