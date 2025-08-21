"""Debug test to see what's being extracted from search results"""

import asyncio
import logging
import re
from perplexity_search import PerplexitySearchClient
from config import load_config

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_extraction():
    """Test what we're extracting from search results"""
    
    # Load configuration
    config = load_config()
    
    # Initialize search client
    search_client = PerplexitySearchClient(config['perplexity_api_key'])
    
    # Perform a search
    from perplexity_search import perform_strategic_search
    
    search_results = await perform_strategic_search(
        search_client, 
        "US", 
        "AI governance",
        "US AI initiatives 2025",
        "AI governance debate"
    )
    
    print("\n" + "="*80)
    print("SEARCH RESULTS ANALYSIS")
    print("="*80)
    
    if search_results and search_results.get("results"):
        for i, result in enumerate(search_results["results"][:3]):
            print(f"\n[Result {i+1}]")
            print(f"Source: {result.source}")
            print(f"Content preview: {result.content[:200]}...")
            
            # Extract specific information
            print("\nExtracted specifics:")
            
            # Dollar amounts
            dollars = re.findall(r'\$[\d,]+(?:\.\d+)?\s*(?:billion|million|trillion)?', result.content)
            if dollars:
                print(f"  Dollar amounts: {dollars}")
            
            # Specific acts/orders
            acts = re.findall(r'(?:CHIPS Act|AI Act|Executive Order \d+|H\.R\.\s*\d+|Public Law \d+-\d+)', result.content)
            if acts:
                print(f"  Acts/Orders: {acts}")
            
            # Dates
            dates = re.findall(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}|\d{4}', result.content)
            if dates:
                print(f"  Dates: {dates[:5]}")  # Limit to 5
            
            # Specific programs/initiatives
            programs = re.findall(r'(?:AI Safety Institute|National AI Initiative|AI Research Resource|NIST.*?Framework)', result.content)
            if programs:
                print(f"  Programs: {programs}")
            
            # Percentages
            percentages = re.findall(r'\d+(?:\.\d+)?%', result.content)
            if percentages:
                print(f"  Percentages: {percentages}")

if __name__ == "__main__":
    asyncio.run(test_extraction())