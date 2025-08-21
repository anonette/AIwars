"""
Simple test for theoretical analysis format generation
"""

import asyncio
import logging
from enhanced_search_integration import TheoreticallyEnhancedAgent

# Set up logging to see what's happening
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_theory_format():
    """Test if theoretical analysis generates correct format"""
    
    print("="*60)
    print("TESTING THEORETICAL ANALYSIS FORMAT")
    print("="*60)
    
    # Create a minimal agent for testing
    agent = TheoreticallyEnhancedAgent(
        name="Test Agent",
        personality="Test personality",
        agent_config_key="openai",
        config={}
    )
    
    # Test the theoretical enhancement directly
    base_response = "We support democratic AI governance."
    theoretical_context = """
    THEORETICAL FRAMEWORK RESOURCES:
    - Yaron Ezrahi: Imagined Democracies (political_imaginaries)
      Keywords: necessary fictions, democratic legitimacy, transparency
    - Michel Foucault: Society Must Be Defended (power_analysis)
      Keywords: sovereignty, biopolitics, state apparatus
    """
    
    print("\nTesting theoretical analysis generation...")
    print("Base response:", base_response)
    
    try:
        # Call the method directly
        analysis = await agent._generate_theoretical_enhancement(
            base_response=base_response,
            theoretical_context=theoretical_context,
            topic="AI governance"
        )
        
        print("\nResult:")
        print("-"*60)
        if analysis:
            print(analysis)
            
            # Check format
            if '[THEORETICAL ANALYSIS]' in analysis:
                print("\n✅ SUCCESS: Contains [THEORETICAL ANALYSIS] marker")
                
                # Check components
                checks = {
                    'Political Imaginary': '- Political Imaginary:' in analysis,
                    'Power Dynamics': '- Power Dynamics:' in analysis,
                    'Cultural Position': '- Cultural Position:' in analysis
                }
                
                print("\nComponent checks:")
                for component, present in checks.items():
                    status = "✅" if present else "❌"
                    print(f"  {status} {component}")
                
                if all(checks.values()):
                    print("\n🎉 All components present! Theoretical analysis is working correctly.")
                else:
                    print("\n⚠️ Some components missing")
            else:
                print("\n❌ FAILED: Missing [THEORETICAL ANALYSIS] marker")
        else:
            print("❌ FAILED: Returned empty analysis")
        print("-"*60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_theory_format())