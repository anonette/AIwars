"""
Verify that Perplexity is working with the config
"""

import asyncio
from perplexity_search import PerplexitySearchClient
import yaml

async def test_with_config():
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Create client with config
    client = PerplexitySearchClient(config=config)
    
    print(f"Using model: {client.model}")
    
    # Test search
    results = await client.search("latest AI policy news")
    
    if results:
        print(f"✓ Search successful! Got {len(results)} results")
        for i, result in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"  Source: {result.source}")
            print(f"  Signal Type: {result.signal_type.value}")
            print(f"  Content: {result.content[:100]}...")
    else:
        print("✗ No results returned")

if __name__ == "__main__":
    asyncio.run(test_with_config())