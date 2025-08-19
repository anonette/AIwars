# Debate Formatter Implementation Plan

## Overview

This document provides a detailed implementation plan for creating a `debate_formatter.py` module that will transform debate responses into the new hybrid format.

## Module Structure

### 1. Main Class: `DebateFormatter`

```python
class DebateFormatter:
    def __init__(self, config=None):
        """
        Initialize formatter with optional configuration
        
        Args:
            config (dict): Optional configuration for symbols, colors, etc.
        """
        self.symbols = {
            'search': '🔍',
            'tying_hands': '💎',
            'sunk_costs': '💰',
            'installment_costs': '🔄',
            'reducible_costs': '🎯',
            'performance': '🎭',
            'tension': '⚡',
            'verified': '✓',
            'unmask': '⚠️',
            'poster': '📊'
        }
        self.enable_colors = config.get('enable_colors', False) if config else False
        self.enable_emojis = config.get('enable_emojis', True) if config else True
        self.separator_width = config.get('separator_width', 80) if config else 80
```

### 2. Core Methods

#### `format_response(self, response_data)`
Main method that orchestrates the formatting of a complete response.

```python
def format_response(self, response_data):
    """
    Format a complete debate response
    
    Args:
        response_data (dict): Structured response data containing:
            - country: str
            - round: int
            - search: dict (query, narration)
            - main_speech: str
            - costly_signal: dict (type, content)
            - performance: dict (content)
            - tension: str
            - sources: list of dicts
            - poster: dict (optional)
            - unmask: dict (optional)
    
    Returns:
        str: Formatted response
    """
```

#### `format_header(self, country, round_num)`
Format the country header with flag and round number.

```python
def format_header(self, country, round_num):
    """
    Format country header with separator
    
    Args:
        country (str): Country name
        round_num (int): Round number
    
    Returns:
        str: Formatted header with separator line
    """
    flags = {
        'United States': '🇺🇸',
        'People\'s Republic of China': '🇨🇳',
        'European Union': '🇪🇺'
    }
```

#### `format_search_narration(self, search_data)`
Format the search action narration.

```python
def format_search_narration(self, search_data):
    """
    Format search narration with italics
    
    Args:
        search_data (dict): Contains 'query' and 'narration'
    
    Returns:
        str: Formatted search narration
    """
```

#### `format_costly_signal(self, signal_data)`
Format costly signals with appropriate symbols and structure.

```python
def format_costly_signal(self, signal_data):
    """
    Format costly signal with symbol and tree structure
    
    Args:
        signal_data (dict): Contains 'type' and 'content'
    
    Returns:
        str: Formatted costly signal
    """
    signal_labels = {
        'TYING_HANDS': 'BINDING COMMITMENT',
        'SUNK_COSTS': 'SUNK COST',
        'INSTALLMENT_COSTS': 'ONGOING PROGRAM',
        'REDUCIBLE_COSTS': 'FLEXIBLE POSITION'
    }
```

#### `format_performance(self, performance_data)`
Format performance fiction elements.

```python
def format_performance(self, performance_data):
    """
    Format performance fiction
    
    Args:
        performance_data (dict): Contains 'content'
    
    Returns:
        str: Formatted performance
    """
```

#### `format_sources(self, sources)`
Format verified sources with proper attribution.

```python
def format_sources(self, sources):
    """
    Format verified sources
    
    Args:
        sources (list): List of source dicts with 'name', 'timestamp', 'url', 'excerpt'
    
    Returns:
        str: Formatted sources
    """
```

### 3. Helper Methods

#### `wrap_text(self, text, indent_level=0, first_line_indent=None)`
Wrap text to fit within terminal width while preserving indentation.

```python
def wrap_text(self, text, indent_level=0, first_line_indent=None):
    """
    Wrap text with proper indentation
    
    Args:
        text (str): Text to wrap
        indent_level (int): Number of spaces to indent
        first_line_indent (str): Optional different indent for first line
    
    Returns:
        str: Wrapped text
    """
```

#### `get_symbol(self, symbol_type)`
Get symbol with fallback for non-emoji mode.

```python
def get_symbol(self, symbol_type):
    """
    Get symbol with fallback
    
    Args:
        symbol_type (str): Type of symbol
    
    Returns:
        str: Symbol or text fallback
    """
    text_fallbacks = {
        'search': '[SEARCH]',
        'tying_hands': '[BINDING]',
        'sunk_costs': '[SUNK]',
        'installment_costs': '[ONGOING]',
        'reducible_costs': '[FLEXIBLE]',
        'performance': '[PERFORM]',
        'tension': '[TENSION]',
        'verified': '[VERIFIED]',
        'unmask': '[UNMASK]',
        'poster': '[POSTER]'
    }
```

### 4. Integration Points

#### With `debate_manager.py`
- Modify `format_response()` method to use `DebateFormatter`
- Pass structured data instead of raw text

#### With `search_enabled_debate_agent.py`
- Ensure agent returns structured response data
- Include all meta-elements in response

#### With `debatepy.py` (Streamlit)
- Use formatter for display
- Add configuration options for format preferences

## Data Structure Example

```python
response_data = {
    "country": "United States",
    "round": 0,
    "search": {
        "query": "US AI companies regulatory burden 2024",
        "narration": "frant