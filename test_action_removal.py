"""
Test that action phrases are properly removed from all responses
"""

import asyncio
import logging
import yaml
from enhanced_search_integration import TheoreticallyEnhancedAgent, EnhancedDocumentStore

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def test_action_removal():
    """Test that action phrases are removed"""
    
    print("Testing Action Phrase Removal")
    print("=" * 80)
    
    # Load config
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Create enhanced document store
    store = EnhancedDocumentStore()
    
    # Create test agent
    test_agent = TheoreticallyEnhancedAgent(
        name="United States",
        personality="US representative focused on innovation and democratic values",
        agent_config_key="openai",
        config=config,
        document_store=store
    )
    
    # Test the _strip_action_phrases method directly
    test_texts = [
        "*straightens tie confidently*\n\nThe United States believes in democratic AI governance.",
        "*reviews notes briefly*\n\nWe must ensure transparency.",
        "No action here, just content.",
        "*adjusts spectacles thoughtfully*\n\nThis is a test.\n\n*nods decisively*\n\nMore content here."
    ]
    
    print("Testing _strip_action_phrases method:")
    print("-" * 40)
    
    for i, text in enumerate(test_texts):
        print(f"\nTest {i+1}:")
        print(f"BEFORE: {repr(text)}")
        cleaned = test_agent._strip_action_phrases(text)
        print(f"AFTER:  {repr(cleaned)}")
    
    print("\n" + "=" * 80)
    
    # Test full response generation
    context = "Round 1 of 5: The topic is AI governance and international cooperation."
    last_message = "European Union: We need strong regulatory frameworks for AI safety."
    
    print("\nGenerating full response (should have no action phrases):")
    print("-" * 80)
    
    response = await test_agent.generate_response(context, last_message)
    
    print(response)
    
    # Check if any action phrases remain
    if '*' in response:
        print("\n⚠️  WARNING: Response still contains asterisks, may have action phrases!")
    else:
        print("\n✓ Success: No action phrases detected in response")

if __name__ == "__main__":
    asyncio.run(test_action_removal())