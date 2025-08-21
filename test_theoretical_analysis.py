"""
Test script to verify theoretical analysis is working correctly
"""

import asyncio
import logging
from enhanced_search_integration import TheoreticallyEnhancedAgent, EnhancedDocumentStore
from perplexity_search import PerplexitySearchClient

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def test_theoretical_analysis():
    """Test the theoretical analysis generation"""
    
    # Initialize components
    document_store = EnhancedDocumentStore()
    search_client = PerplexitySearchClient()
    
    # Create test agent
    agent = TheoreticallyEnhancedAgent(
        name="United States",
        personality="Representative of US interests in AI governance",
        agent_config_key="openai",
        config={},
        document_store=document_store,
        search_client=search_client
    )
    
    # Test base response
    base_response = "The United States champions democratic AI governance through innovation and ethical frameworks."
    
    # Get theoretical context
    theoretical_context = agent._get_theoretical_context("AI governance")
    print("Theoretical Context Available:")
    print("-" * 80)
    print(theoretical_context)
    print("-" * 80)
    
    # Test theoretical enhancement
    print("\nTesting Theoretical Analysis Generation...")
    analysis = await agent._generate_theoretical_enhancement(
        base_response=base_response,
        theoretical_context=theoretical_context,
        topic="AI governance"
    )
    
    print("\nTheoretical Analysis Result:")
    print("-" * 80)
    if analysis:
        print(analysis)
        
        # Verify format
        if '[THEORETICAL ANALYSIS]' in analysis:
            print("\n✅ Theoretical analysis contains expected marker!")
            
            # Check for all three components
            has_imaginary = '- Political Imaginary:' in analysis
            has_power = '- Power Dynamics:' in analysis
            has_cultural = '- Cultural Position:' in analysis
            
            print(f"Has Political Imaginary: {has_imaginary}")
            print(f"Has Power Dynamics: {has_power}")
            print(f"Has Cultural Position: {has_cultural}")
            
            if all([has_imaginary, has_power, has_cultural]):
                print("\n✅ All theoretical components present!")
            else:
                print("\n⚠️ Some theoretical components missing")
        else:
            print("\n❌ Theoretical analysis missing expected marker")
    else:
        print("❌ Theoretical analysis returned empty")
    print("-" * 80)

async def test_full_response_with_theory():
    """Test a full response generation with theoretical analysis"""
    
    print("\n" + "="*80)
    print("TESTING FULL RESPONSE WITH THEORETICAL ANALYSIS")
    print("="*80)
    
    # Initialize components
    document_store = EnhancedDocumentStore()
    search_client = PerplexitySearchClient()
    
    # Create test agent
    agent = TheoreticallyEnhancedAgent(
        name="European Union",
        personality="Representative of EU interests in AI governance",
        agent_config_key="european_union",
        config={},
        document_store=document_store,
        search_client=search_client
    )
    
    # Test context
    context = "The debate focuses on establishing global AI governance frameworks."
    last_message = "United States: We propose innovation-led governance with minimal regulatory constraints."
    
    print("\nGenerating full response with theoretical enhancement...")
    
    try:
        response = await agent.generate_response(context, last_message)
        
        print("\nFull Response:")
        print("-" * 80)
        print(response)
        print("-" * 80)
        
        # Check if theoretical analysis was included
        if '[THEORETICAL ANALYSIS]' in response:
            print("\n✅ Response includes theoretical analysis!")
        else:
            print("\n⚠️ Response doesn't include theoretical analysis")
            
    except Exception as e:
        print(f"\n❌ Error generating response: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_theoretical_analysis())
    asyncio.run(test_full_response_with_theory())