import streamlit as st
import sys
import os

st.title("AI Wars Debate System - Test")

# Test if we can import our modules without PyTorch issues
try:
    # Add the current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Import our modules
    from perplexity_search import PerplexitySearchClient
    from search_enabled_debate_agent import SearchEnabledDebateAgent
    
    st.success("✅ Successfully imported search modules!")
    
    # Check if config loads
    import yaml
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    if config.get('search', {}).get('perplexity', {}).get('enabled', False):
        st.success("✅ Search is enabled in config!")
    else:
        st.warning("⚠️ Search is not enabled in config")
        
    # Check if API key is available
    if os.getenv("PERPLEXITY_API_KEY"):
        st.success("✅ Perplexity API key found!")
    else:
        st.error("❌ Perplexity API key not found in environment")
        
except Exception as e:
    st.error(f"Error during import: {str(e)}")
    st.exception(e)

st.info("If all checks pass, the main app should work correctly!")