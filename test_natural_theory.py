"""
Test the natural theoretical analysis approach
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

async def test_natural_theoretical_analysis():
    """Test the new natural approach to theoretical analysis"""
    
    print("="*60)
    print("TESTING NATURAL THEORETICAL ANALYSIS")
    print("="*60)
    
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
    
    # Test scenarios
    test_cases = [
        {
            "context": "The debate is about AI governance frameworks.",
            "last_message": "China: We propose state-led AI development with strong oversight.",
            "description": "Response to state-led governance"
        },
        {
            "context": "Discussion on AI safety and innovation balance.",
            "last_message": "EU: We must prioritize human rights in AI development.",
            "description": "Response to rights-based approach"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n{'='*60}")
        print(f"Test Case {i+1}: {test_case['description']}")
        print(f"{'='*60}")
        
        print(f"Context: {test_case['context']}")
        print(f"Last Message: {test_case['last_message']}")
        
        try:
            # Generate response
            response = await agent.generate_response(
                context=test_case['context'],
                last_message=test_case['last_message']
            )
            
            print(f"\nGenerated Response:")
            print("-"*60)
            print(response)
            print("-"*60)
            
            # Check if theoretical analysis was included
            if '[THEORETICAL ANALYSIS]' in response:
                print("\n✅ Response includes theoretical analysis!")
                
                # Extract and display just the theoretical part
                theory_start = response.find('[THEORETICAL ANALYSIS]')
                theory_section = response[theory_start:]
                
                print("\nTheoretical Analysis Section:")
                print("-"*40)
                print(theory_section)
                print("-"*40)
                
                # Check for theorist references
                theorists = ['Ezrahi', 'Foucault', 'Bhabha', 'necessary fiction', 'power', 'sovereignty', 'cultural']
                found_concepts = [t for t in theorists if t.lower() in theory_section.lower()]
                
                if found_concepts:
                    print(f"\n✅ Found theoretical concepts: {', '.join(found_concepts)}")
                else:
                    print("\n⚠️ No specific theoretical concepts found")
            else:
                print("\n⚠️ No theoretical analysis section found")
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

async def test_direct_theoretical_generation():
    """Test the theoretical enhancement method directly"""
    
    print("\n" + "="*60)
    print("TESTING DIRECT THEORETICAL GENERATION")
    print("="*60)
    
    # Create minimal agent
    agent = TheoreticallyEnhancedAgent(
        name="Test Agent",
        personality="Test",
        agent_config_key="openai",
        config={}
    )
    
    # Test the theoretical enhancement directly
    base_response = "The United States champions democratic AI governance through innovation and ethical frameworks."
    theoretical_context = """
- Yaron Ezrahi: Imagined Democracies (political_imaginaries)
  Keywords: necessary fictions, democratic legitimacy, transparency
- Michel Foucault: Society Must Be Defended (power_analysis)
  Keywords: sovereignty, biopolitics, state apparatus
- Homi Bhabha: The Location of Culture (cultural_theory)
  Keywords: cultural positioning, mimicry, hybridity
"""
    
    print("Testing direct theoretical enhancement...")
    print(f"Base response: {base_response}")
    
    try:
        analysis = await agent._generate_theoretical_enhancement(
            base_response=base_response,
            theoretical_context=theoretical_context,
            topic="AI governance"
        )
        
        print("\nTheoretical Analysis:")
        print("-"*60)
        if analysis:
            print(analysis)
            
            # Check quality
            if len(analysis) > 200:
                print(f"\n✅ Generated substantial analysis ({len(analysis)} characters)")
            else:
                print(f"\n⚠️ Analysis seems brief ({len(analysis)} characters)")
                
            # Check for theoretical content
            theorists = ['Ezrahi', 'Foucault', 'Bhabha', 'necessary fiction', 'power', 'sovereignty', 
                        'imaginar', 'cultural', 'discourse', 'legitimacy']
            found = [t for t in theorists if t.lower() in analysis.lower()]
            
            if found:
                print(f"✅ Found theoretical concepts: {', '.join(found)}")
            else:
                print("⚠️ Missing expected theoretical concepts")
        else:
            print("❌ No analysis generated")
        print("-"*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run both tests
    asyncio.run(test_direct_theoretical_generation())
    asyncio.run(test_natural_theoretical_analysis())