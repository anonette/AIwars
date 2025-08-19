"""
Configuration to ensure agents always search for recent initiatives first
"""

def create_search_first_prompt(agent_name: str, topic: str, search_results: dict, 
                              doc_context: str, last_message: str) -> str:
    """
    Create a prompt that emphasizes using search results for recent initiatives
    and documents for official positions
    """
    
    # Format search results
    search_section = "RECENT INITIATIVES FROM SEARCH:\n"
    if search_results and search_results.get("results"):
        for i, result in enumerate(search_results["results"][:5]):
            if hasattr(result, 'content'):
                search_section += f"\n[{i+1}] {result.content[:400]}...\n"
            elif isinstance(result, dict):
                content = result.get('content', '')
                search_section += f"\n[{i+1}] {content[:400]}...\n"
    else:
        search_section += "No recent initiatives found in search.\n"
    
    # Format document context
    doc_section = "OFFICIAL POSITION FROM POLICY DOCUMENTS:\n"
    doc_section += doc_context if doc_context else "No specific policy documents available.\n"
    
    # Create comprehensive prompt
    prompt = f"""You are {agent_name} in an AI governance debate on the topic: {topic}

{search_section}

{doc_section}

Previous speaker said: {last_message}

IMPORTANT: Your response MUST:
1. Reference SPECIFIC recent initiatives from the search results above (mention programs by name, funding amounts, dates)
2. Connect these recent initiatives to your country's official policy framework from the documents
3. Show how these concrete developments advance your strategic position

Do not give generic statements. Every claim must reference either:
- A specific initiative/program/investment from the search results
- An official policy position from your documents
- Ideally both, showing how recent initiatives implement official policy

Be specific with names, numbers, and dates."""
    
    return prompt


def ensure_search_first_flow():
    """
    Documentation of the required flow:
    
    1. ALWAYS perform search first for recent initiatives
    2. THEN consult RAG documents for official positions
    3. FINALLY generate response using both sources
    
    This ensures agents are grounded in:
    - Current reality (from search)
    - Official positions (from documents)
    """
    pass