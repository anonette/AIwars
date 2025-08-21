"""Test the AI Safety topic with search-first workflow"""

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

async def test_ai_safety_topic():
    """Test AI Safety topic debate"""
    
    # Load configuration
    config = load_config()
    
    # Initialize search client
    search_client = PerplexitySearchClient(config['perplexity_api_key'])
    
    # Create agents
    agents = {
        "US": TheoreticallyEnhancedAgent(
            name="US",
            personality="You are the United States representative, focused on innovation and competitiveness while balancing safety concerns.",
            agent_config_key="us_agent",
            search_client=search_client
        ),
        "China": TheoreticallyEnhancedAgent(
            name="China",
            personality="You are the China representative, focused on technological sovereignty and development.",
            agent_config_key="china_agent",
            search_client=search_client
        ),
        "EU": TheoreticallyEnhancedAgent(
            name="EU",
            personality="You are the European Union representative, focused on ethical AI and regulatory frameworks.",
            agent_config_key="eu_agent",
            search_client=search_client
        )
    }
    
    # AI Safety topic context
    context = "The debate topic is: AI Safety vs Innovation - How do we balance rapid AI advancement with necessary safety measures?"
    
    print("\n" + "="*80)
    print("AI SAFETY TOPIC TEST")
    print("="*80)
    print(f"\nContext: {context}")
    
    # Test each agent
    for name, agent in agents.items():
        print(f"\n\n{'='*40}")
        print(f"Testing {name} on AI Safety")
        print('='*40)
        
        last_message = "What specific AI safety initiatives has your country implemented recently, and how do they balance innovation with safety?"
        
        response = await agent.generate_response(context, last_message)
        
        # Show first 500 chars of response
        print(f"\nResponse preview:")
        print(response[:500] + "..." if len(response) > 500 else response)
        
        # Check for key indicators
        print(f"\n✓ Checks:")
        
        # Check for recent dates
        recent_dates = ["2024", "2025"]
        found_dates = [d for d in recent_dates if d in response]
        print(f"  - Recent dates: {found_dates}")
        
        # Check for safety-related terms
        safety_terms = ["safety", "risk", "alignment", "testing", "evaluation", "framework"]
        found_safety = [t for t in safety_terms if t.lower() in response.lower()]
        print(f"  - Safety terms: {found_safety}")
        
        # Check for sources
        has_sources = "Sources:" in response
        print(f"  - Has sources: {has_sources}")
        
        await asyncio.sleep(1)  # Rate limiting

async def test_sustainability_topic():
    """Test the new sustainability and minerals topic"""
    
    # Load configuration
    config = load_config()
    
    # Initialize search client
    search_client = PerplexitySearchClient(config['perplexity_api_key'])
    
    # Create EU agent for sustainability test
    agent = TheoreticallyEnhancedAgent(
        name="EU",
        personality="You are the European Union representative, concerned about environmental sustainability and resource dependencies.",
        agent_config_key="eu_agent",
        search_client=search_client
    )
    
    context = "The debate topic is: AI Infrastructure and Sustainability - How do we address the environmental impact of AI, including energy consumption and rare earth mineral dependencies?"
    
    print("\n\n" + "="*80)
    print("SUSTAINABILITY TOPIC TEST")
    print("="*80)
    print(f"\nContext: {context}")
    
    last_message = "How is your region addressing the environmental impact of AI data centers and the dependency on rare earth minerals?"
    
    response = await agent.generate_response(context, last_message)
    
    print(f"\nEU Response preview:")
    print(response[:600] + "..." if len(response) > 600 else response)
    
    # Check for sustainability indicators
    print(f"\n✓ Sustainability Checks:")
    
    sustainability_terms = ["energy", "carbon", "renewable", "sustainable", "environmental"]
    found_sustainability = [t for t in sustainability_terms if t.lower() in response.lower()]
    print(f"  - Sustainability terms: {found_sustainability}")
    
    mineral_terms = ["mineral", "lithium", "cobalt", "rare earth", "supply chain"]
    found_minerals = [t for t in mineral_terms if t.lower() in response.lower()]
    print(f"  - Mineral/resource terms: {found_minerals}")
    
    has_sources = "Sources:" in response
    print(f"  - Has sources: {has_sources}")

if __name__ == "__main__":
    print("Testing AI Safety topic...")
    asyncio.run(test_ai_safety_topic())
    
    print("\n\nTesting Sustainability topic...")
    asyncio.run(test_sustainability_topic())