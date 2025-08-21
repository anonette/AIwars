import asyncio
import os
from dotenv import load_dotenv
from perplexity_search import PerplexitySearchClient
import yaml
import sys

async def test_perplexity():
    # Load environment variables
    load_dotenv()
    
    # Load config
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Check API key
    api_key = os.getenv("PERPLEXITY_API_KEY")
    print(f"API Key present: {bool(api_key)}")
    print(f"API Key (first 10 chars): {api_key[:10] if api_key else 'None'}")
    
    # Initialize client
    try:
        client = PerplexitySearchClient(config=config)
        print("Client initialized successfully")
        
        # Test search
        results = await client.search("latest AI governance news 2024")
        print(f"\nSearch results: {len(results)}")
        
        for i, result in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"  Source: {result.source}")
            print(f"  URL: {result.url}")
            print(f"  Content preview: {result.content[:100]}...")
            
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Windows-specific event loop policy to avoid the RuntimeError
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Run the async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(test_perplexity())
    finally:
        loop.close()
