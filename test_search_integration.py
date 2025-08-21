"""
Test script for the complete RAG + Search + Signal integration
Tests document retrieval, search capabilities, costly signals, and UNMASK features
"""

import asyncio
import logging
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from document_retrieval import DocumentStore
from perplexity_search import PerplexitySearchClient, perform_strategic_search
from search_enabled_debate_agent import SearchEnabledDebateAgent
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_search_integration():
    """Test the complete search integration system"""
    
    print("=" * 80)
    print("TESTING SEARCH-ENABLED AI DEBATE SYSTEM")
    print("=" * 80)
    
    # Load configuration
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize components
    print("\n1. Initializing components...")
    
    # Document store
    document_store = DocumentStore()
    print(f"   ✓ Document store initialized with {len(document_store.document_index)} documents")
    
    # Search client
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key:
        print("   ✗ ERROR: PERPLEXITY_API_KEY not found in .env file")
        print("   Please add: PERPLEXITY_API_KEY=your_key_here")
        return
    
    search_client = PerplexitySearchClient(api_key=api_key)
    print("   ✓ Perplexity search client initialized")
    
    # Create test agents
    print("\n2. Creating search-enabled agents...")
    
    agents = {}
    for agent_name in ["United States", "People's Republic of China", "European Union"]:
        agent_key = agent_name.lower().replace(" ", "_").replace("'", "")
        agents[agent_name] = SearchEnabledDebateAgent(
            name=agent_name,
            personality=config['agents']['openai']['personality'],
            agent_config_key='openai',
            config=config,
            document_store=document_store,
            search_client=search_client
        )
        print(f"   ✓ Created {agent_name} agent")
    
    # Test scenarios
    print("\n3. Running test scenarios...")
    
    # Scenario 1: Test document retrieval
    print("\n   Scenario 1: Document Retrieval")
    print("   " + "-" * 40)
    
    us_agent = agents["United States"]
    context = "The topic is AI governance and semiconductor policy"
    last_message = "China: We believe in sovereign control over AI development"
    
    # Test document search
    doc_context, used_docs = us_agent._get_document_context_with_tracking(
        "United States", last_message, "AI governance semiconductor"
    )
    
    if doc_context:
        print(f"   ✓ Found {len(used_docs)} relevant documents")
        print(f"   Documents: {', '.join(used_docs[:3])}...")
    else:
        print("   ⚠ No documents found (this is okay if documents aren't loaded)")
    
    # Scenario 2: Test search functionality
    print("\n   Scenario 2: Search Functionality")
    print("   " + "-" * 40)
    
    try:
        search_results = await perform_strategic_search(
            search_client,
            "United States",
            "AI semiconductor export controls",
            "China is developing indigenous AI chips",
            context
        )
        
        if search_results:
            print(f"   ✓ Search completed successfully")
            print(f"   Meta-queries generated: {len(search_results.get('meta_queries', []))}")
            print(f"   Results found: {len(search_results.get('results', []))}")
            print(f"   Signal type: {search_results['results'][0].signal_type.value if search_results.get('results') else 'N/A'}")
            
            # Show search narration
            print(f"\n   Search Narration Preview:")
            print(f"   {search_results['narration'][:200]}...")
        else:
            print("   ✗ Search failed or returned no results")
    except Exception as e:
        print(f"   ✗ Search error: {str(e)}")
        print("   (This may be due to API key issues or rate limits)")
    
    # Scenario 3: Test full response generation
    print("\n   Scenario 3: Full Response Generation")
    print("   " + "-" * 40)
    
    try:
        # Generate a response with search and documents
        response = await us_agent.generate_response(
            context="Round 1: Discuss AI governance and semiconductor policy",
            last_message="China: We are investing heavily in domestic AI chip production to ensure technological sovereignty.",
            debate_prompt="Respond to China's position on AI sovereignty"
        )
        
        print("   ✓ Response generated successfully")
        
        # Check for key components
        components = {
            "Search narration": "*searches" in response,
            "Costly signal": "[COSTLY SIGNAL" in response,
            "Performance fiction": "[PERFORMANCE FICTION]" in response,
            "Signal-fiction tension": "[SIGNAL-FICTION TENSION]" in response,
            "Citations": "Sources" in response or "[1]" in response
        }
        
        print("\n   Response components:")
        for component, present in components.items():
            status = "✓" if present else "✗"
            print(f"   {status} {component}")
        
        # Show response preview
        print(f"\n   Response Preview:")
        print("   " + "-" * 40)
        print(f"   {response[:500]}...")
        
    except Exception as e:
        print(f"   ✗ Response generation error: {str(e)}")
        logging.error(f"Full error: {e}", exc_info=True)
    
    # Scenario 4: Test UNMASK feature
    print("\n\n   Scenario 4: UNMASK Feature")
    print("   " + "-" * 40)
    
    # Update round tracking to enable UNMASK
    us_agent.rounds_since_last_unmask = 2
    
    try:
        # Generate response to a claim that should trigger UNMASK
        theatrical_message = "European Union: We guarantee complete AI safety through our comprehensive regulatory framework that will ensure all AI systems are fully aligned with human values."
        
        response = await us_agent.generate_response(
            context="Round 2: Discussing AI safety guarantees",
            last_message=theatrical_message,
            debate_prompt="Respond to EU's guarantee claims"
        )
        
        if "[UNMASK]" in response:
            print("   ✓ UNMASK feature activated")
            unmask_start = response.find("[UNMASK]")
            unmask_end = response.find("\n", unmask_start + 200)
            print(f"\n   UNMASK Preview:")
            print(f"   {response[unmask_start:unmask_end]}...")
        else:
            print("   ⚠ UNMASK not triggered (may need more theatrical language)")
            
    except Exception as e:
        print(f"   ✗ UNMASK test error: {str(e)}")
    
    # Scenario 5: Test poster generation in high-tension moment
    print("\n   Scenario 5: Poster Generation (High Tension)")
    print("   " + "-" * 40)
    
    try:
        crisis_response = await agents["People's Republic of China"].generate_response(
            context="Round 3: URGENT - Crisis over semiconductor export controls",
            last_message="United States: Immediate ban on all AI chip exports to China effective today.",
            debate_prompt="Respond to US semiconductor ban"
        )
        
        if "[POSTER CONCEPT]" in crisis_response:
            print("   ✓ Poster concept generated for high-tension moment")
            poster_start = crisis_response.find("[POSTER CONCEPT]")
            poster_end = crisis_response.find("\n\n", poster_start + 200)
            print(f"\n   Poster Preview:")
            print(f"   {crisis_response[poster_start:poster_end]}...")
        else:
            print("   ⚠ No poster generated (may need more tension indicators)")
            
    except Exception as e:
        print(f"   ✗ Poster generation error: {str(e)}")
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    print("\nThe search integration system includes:")
    print("✓ Document retrieval from knowledge base")
    print("✓ Real-time search via Perplexity API")
    print("✓ Meta-query generation for strategic angles")
    print("✓ Costly signal generation (Fearon)")
    print("✓ Performance fiction creation (Ezrahi)")
    print("✓ Signal-fiction tension analysis")
    print("✓ UNMASK capability for denaturalizing claims")
    print("✓ Multi-format citations (hard facts vs performative)")
    print("✓ Poster concept generation for high-tension moments")
    
    print("\nTo run a full debate with search integration:")
    print("1. Ensure PERPLEXITY_API_KEY is set in .env")
    print("2. Run: python debatepy.py")
    print("3. Select a topic and watch agents search, signal, and perform!")

if __name__ == "__main__":
    # Run the async test
    asyncio.run(test_search_integration())