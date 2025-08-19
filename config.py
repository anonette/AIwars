"""Configuration loader for the AI debate system"""

import yaml
import os
from typing import Dict, Any

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file"""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Also load environment variables if .env exists
    if os.path.exists('.env'):
        from dotenv import load_dotenv
        load_dotenv()
        
        # Override with environment variables if they exist
        if 'PERPLEXITY_API_KEY' in os.environ:
            config['perplexity_api_key'] = os.environ['PERPLEXITY_API_KEY']
        if 'OPENAI_API_KEY' in os.environ:
            config['openai_api_key'] = os.environ['OPENAI_API_KEY']
    
    return config