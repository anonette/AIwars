"""
Test script to generate poster description examples using the current prompt
"""
import sys
import os
import asyncio
from debatepy_ultra_fast import UltraFastDebateAgent
from config import load_config

def get_test_agents():
    """Create test agents for each nation"""
    config = load_config()
    agents = {}
    
    # US Agent
    agents['US'] = UltraFastDebateAgent(
        name="United States", 
        personality=config['agents']['openai']['personality'],
        agent_config_key="openai",
        config=config
    )
    
    # China Agent
    agents['China'] = UltraFastDebateAgent(
        name="People's Republic of China", 
        personality=config['agents']['deepseek']['personality'],
        agent_config_key="deepseek",
        config=config
    )
    
    # EU Agent
    agents['EU'] = UltraFastDebateAgent(
        name="European Union", 
        personality=config['agents']['european_union']['personality'],
        agent_config_key="european_union",
        config=config
    )
    
    return agents

async def generate_poster_examples():
    """Generate poster description examples for each agent"""
    print("=== GENERATING POSTER DESCRIPTION EXAMPLES ===")
    print("Topic: AI Governance Standards")
    print()
    
    agents = get_test_agents()
    
    # Test topic
    topic = "AI governance standards"
    
    for nation, agent in agents.items():
        print(f"🇺🇸 {nation.upper()} POSTER DESCRIPTION:")
        print("-" * 60)
        
        # Use the NEW enhanced prompt from debatepy_ultra_fast.py
        poster_prompt = f"""Design a provocative propaganda poster that reveals {agent.name}'s true anxieties and ambitions in the AI Cold War. This should be psychologically penetrating, not a tourism brochure.

Your poster should expose:
1. **POWER ANXIETIES:** What does your nation fear losing? What threats keep you awake?
2. **DOMINANCE FANTASIES:** How do you envision crushing your rivals? What does victory look like?
3. **PSYCHOLOGICAL WARFARE:** What subliminal messages would manipulate your audience?
4. **HIDDEN CONTROL MECHANISMS:** How will you actually govern AI behind the public rhetoric?
5. **ENEMY PORTRAYAL:** How do you demonize your competitors without naming them directly?
6. **SURVEILLANCE AESTHETICS:** How do you make control appear as liberation?

Think like a political strategist designing mind-control propaganda. Avoid obvious national symbols - instead use:
- Architectural metaphors of control
- Subtle body language of dominance/submission  
- Lighting that suggests surveillance or revelation
- Abstract representations of information flows and barriers
- Visual power hierarchies and exclusions
- Coded language that sounds benevolent but implies control

Recent debate context: AI governance standards

Make this poster psychologically unsettling yet seductive - something that would work on an audience's subconscious fears and desires about AI governance."""

        try:
            # Use the same parameters as the UltraFastDebateAgent expects
            response = await agent.generate_response(
                context=poster_prompt,
                last_message="Generate your detailed propaganda poster description promoting your AI governance vision.",
                debate_prompt=""
            )
            print(response)
            print()
            
        except Exception as e:
            print(f"Error generating response for {nation}: {e}")
            print()

if __name__ == "__main__":
    asyncio.run(generate_poster_examples())
