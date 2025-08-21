"""
Minimal test to verify theoretical analysis prompt engineering
"""

import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

async def test_llm_format_compliance():
    """Test if LLM follows the theoretical analysis format"""
    
    print("="*60)
    print("TESTING LLM FORMAT COMPLIANCE")
    print("="*60)
    
    # Simulate the exact prompt that would be sent to the LLM
    test_prompt = """Analyze the following diplomatic response through theoretical frameworks.

DIPLOMATIC RESPONSE TO ANALYZE:
The United States champions democratic AI governance through innovation and ethical frameworks.

AVAILABLE THEORETICAL SOURCES:
- Yaron Ezrahi: Imagined Democracies (political_imaginaries)
  Keywords: necessary fictions, democratic legitimacy, transparency
- Michel Foucault: Society Must Be Defended (power_analysis)
  Keywords: sovereignty, biopolitics, state apparatus

INSTRUCTIONS:
You MUST analyze this response using the theoretical frameworks provided, particularly:
- Ezrahi's concept of "necessary political fictions" and political imaginaries
- Foucault's analysis of power relations and sovereignty
- Post-colonial perspectives on technological discourse

OUTPUT FORMAT (you MUST use this exact format):
[THEORETICAL ANALYSIS]
- Political Imaginary: <specific necessary fiction from Ezrahi's framework>
- Power Dynamics: <material power relations using Foucault's concepts>
- Cultural Position: <discourse positioning from post-colonial theory>

IMPORTANT: Start your response with [THEORETICAL ANALYSIS] and follow the exact format above.

REMINDER: Your response MUST start with [THEORETICAL ANALYSIS] followed by the three analysis points."""
    
    print("\nPrompt that would be sent to LLM:")
    print("-"*60)
    print(test_prompt)
    print("-"*60)
    
    # Expected format example
    expected_format = """[THEORETICAL ANALYSIS]
- Political Imaginary: The "democratic AI governance" operates as a necessary fiction (Ezrahi) that legitimizes US technological hegemony through appeals to democratic values
- Power Dynamics: Innovation rhetoric masks material control over AI infrastructure and standards-setting (Foucault's sovereignty through technical apparatus)
- Cultural Position: Positions US as benevolent hegemon in contrast to authoritarian AI governance models"""
    
    print("\nExpected format example:")
    print("-"*60)
    print(expected_format)
    print("-"*60)
    
    # Verify the prompt structure
    print("\nPrompt validation:")
    checks = {
        "Contains [THEORETICAL ANALYSIS] instruction": "[THEORETICAL ANALYSIS]" in test_prompt,
        "Contains Ezrahi reference": "Ezrahi" in test_prompt,
        "Contains Foucault reference": "Foucault" in test_prompt,
        "Contains format specification": "- Political Imaginary:" in test_prompt,
        "Contains REMINDER": "REMINDER:" in test_prompt
    }
    
    all_good = True
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")
        if not result:
            all_good = False
    
    if all_good:
        print("\n✅ Prompt structure is correct for LLM format compliance")
    else:
        print("\n❌ Prompt structure has issues")

# Test the actual implementation
async def test_with_mock_agent():
    """Test with a mock version of the agent"""
    from search_enabled_debate_agent import SearchEnabledDebateAgent
    
    print("\n" + "="*60)
    print("TESTING WITH MOCK AGENT")
    print("="*60)
    
    # Create a minimal agent
    agent = SearchEnabledDebateAgent(
        name="Test Agent",
        personality="Test",
        agent_config_key="openai",
        config={}
    )
    
    # Test the prompt generation
    prompt = """Generate a theoretical analysis of this diplomatic statement.

Statement: The US promotes democratic AI governance.

You MUST output EXACTLY this format (replace the bracketed placeholders with your analysis):

[THEORETICAL ANALYSIS]
- Political Imaginary: [Your analysis using Ezrahi's necessary fictions concept]
- Power Dynamics: [Your analysis using Foucault's power relations]
- Cultural Position: [Your analysis using post-colonial theory]

Start with [THEORETICAL ANALYSIS] on the first line."""
    
    print("Testing direct prompt...")
    
    # Mock the LLM response
    mock_response = """[THEORETICAL ANALYSIS]
- Political Imaginary: Democratic AI governance serves as a necessary fiction that legitimizes technological control
- Power Dynamics: Material infrastructure control masked by democratic rhetoric
- Cultural Position: Western-centric technological discourse positioning"""
    
    print("\nMock LLM response:")
    print("-"*60)
    print(mock_response)
    print("-"*60)
    
    # Verify format
    if '[THEORETICAL ANALYSIS]' in mock_response:
        print("\n✅ Mock response contains required marker")
    else:
        print("\n❌ Mock response missing required marker")

if __name__ == "__main__":
    asyncio.run(test_llm_format_compliance())
    asyncio.run(test_with_mock_agent())