"""Test to verify theoretical analyses reference specific search results"""

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

async def test_specific_analysis():
    """Test that theoretical analyses reference specific policies from search"""
    
    # Load configuration
    config = load_config()
    
    # Initialize search client
    search_client = PerplexitySearchClient(config['perplexity_api_key'])
    
    # Create US agent
    agent = TheoreticallyEnhancedAgent(
        name="US",
        personality="You are the United States representative, focused on innovation and competitiveness.",
        agent_config_key="us_agent",
        search_client=search_client
    )
    
    # Test context
    context = "The debate is about AI governance and international cooperation."
    last_message = "What specific AI initiatives has your country launched recently?"
    
    print("\n" + "="*80)
    print("TESTING SPECIFIC THEORETICAL ANALYSIS")
    print("="*80)
    
    # Generate response
    print(f"\nGenerating response for {agent.name}...")
    response = await agent.generate_response(context, last_message)
    
    # Extract just the theoretical analyses
    print("\n" + "="*80)
    print("THEORETICAL ANALYSES:")
    print("="*80)
    
    # Extract Ezrahi analysis
    if "[EZRAHI'S ANALYSIS" in response:
        start = response.find("[EZRAHI'S ANALYSIS")
        end = response.find("[FEARON'S", start) if "[FEARON'S" in response else response.find("[META-SOVEREIGNTY", start)
        if end == -1:
            end = response.find("Sources:", start)
        ezrahi = response[start:end].strip()
        print("\n" + ezrahi)
        
        # Check for specific policies
        print("\nEzrahi Specificity Check:")
        specific_indicators = ["$", "billion", "Act", "Order", "Executive", "%", "million"]
        found = [ind for ind in specific_indicators if ind in ezrahi]
        print(f"✓ Found specific indicators: {found}")
    
    # Extract Fearon analysis
    if "[FEARON'S" in response:
        start = response.find("[FEARON'S")
        end = response.find("[META-SOVEREIGNTY", start) if "[META-SOVEREIGNTY" in response else response.find("Sources:", start)
        fearon = response[start:end].strip()
        print("\n" + "-"*80)
        print(fearon)
        
        # Check for specific policies
        print("\nFearon Specificity Check:")
        specific_indicators = ["$", "billion", "CHIPS", "Act", "Order", "signal type", "cost"]
        found = [ind for ind in specific_indicators if ind in fearon]
        print(f"✓ Found specific indicators: {found}")
    
    # Extract Meta-sovereignty analysis
    if "[META-SOVEREIGNTY" in response:
        start = response.find("[META-SOVEREIGNTY")
        end = response.find("Sources:", start) if "Sources:" in response else len(response)
        meta = response[start:end].strip()
        print("\n" + "-"*80)
        print(meta)
        
        # Check for specific policies
        print("\nMeta-sovereignty Specificity Check:")
        specific_indicators = ["$", "billion", "CHIPS", "ASML", "Dutch", "Taiwan", "dependency"]
        found = [ind for ind in specific_indicators if ind in meta]
        print(f"✓ Found specific indicators: {found}")
    
    # Overall check for generic phrases that should NOT appear
    print("\n" + "="*80)
    print("CHECKING FOR FORBIDDEN GENERIC PHRASES:")
    print("="*80)
    
    forbidden_phrases = [
        "emphasis on voluntary",
        "fostering innovation",
        "commitment to ethical",
        "international cooperation",
        "democratic principles"
    ]
    
    found_forbidden = []
    for phrase in forbidden_phrases:
        if phrase.lower() in response.lower():
            found_forbidden.append(phrase)
    
    if found_forbidden:
        print(f"✗ Found forbidden generic phrases: {found_forbidden}")
    else:
        print("✓ No forbidden generic phrases found")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_specific_analysis())