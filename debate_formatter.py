"""
Debate Formatter Module
Implements hybrid formatting with dual output support for display and logging
"""

import re
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class SignalType(Enum):
    """Signal types based on CSET framework"""
    TYING_HANDS = "TYING_HANDS"
    SUNK_COSTS = "SUNK_COSTS"
    INSTALLMENT_COSTS = "INSTALLMENT_COSTS"
    REDUCIBLE_COSTS = "REDUCIBLE_COSTS"


class DebateFormatter:
    """
    Formatter for debate responses with support for both display and log-safe output
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize formatter with optional configuration
        
        Args:
            config: Optional configuration dictionary
        """
        config = config or {}
        
        # Display configuration
        self.enable_emojis = config.get('enable_emojis', True)
        self.enable_colors = config.get('enable_colors', False)
        self.separator_width = config.get('separator_width', 80)
        self.log_safe_mode = config.get('log_safe_mode', False)
        
        # Symbol mappings
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
        
        # ASCII fallbacks for log-safe mode
        self.ascii_symbols = {
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
        
        # Country flags
        self.flags = {
            'United States': '🇺🇸',
            'People\'s Republic of China': '🇨🇳',
            'European Union': '🇪🇺'
        }
        
        # Signal type labels
        self.signal_labels = {
            SignalType.TYING_HANDS: 'BINDING COMMITMENT',
            SignalType.SUNK_COSTS: 'SUNK COST',
            SignalType.INSTALLMENT_COSTS: 'ONGOING PROGRAM',
            SignalType.REDUCIBLE_COSTS: 'FLEXIBLE POSITION'
        }
        
    def format_response(self, response_data: Dict[str, Any], for_logging: bool = False) -> str:
        """
        Format a complete debate response
        
        Args:
            response_data: Structured response data
            for_logging: Whether to format for logging (no emojis)
            
        Returns:
            Formatted response string
        """
        if for_logging or self.log_safe_mode:
            return self._format_log_safe(response_data)
        return self._format_display(response_data)
    
    def _format_display(self, response_data: Dict[str, Any]) -> str:
        """Format response for display with emojis and visual elements"""
        parts = []
        
        # Header
        parts.append(self._format_header(
            response_data.get('country', 'Unknown'),
            response_data.get('round', 0)
        ))
        
        # Search narration
        if 'search' in response_data:
            parts.append(self._format_search_narration(response_data['search']))
            parts.append("")  # Empty line
        
        # Main speech
        if 'main_speech' in response_data:
            parts.append(response_data['main_speech'])
            parts.append("")  # Empty line
        
        # Costly signal
        if 'costly_signal' in response_data:
            parts.append(self._format_costly_signal(response_data['costly_signal']))
            parts.append("")
        
        # Performance fiction
        if 'performance' in response_data:
            parts.append(self._format_performance(response_data['performance']))
            parts.append("")
        
        # Tension
        if 'tension' in response_data:
            parts.append(self._format_tension(response_data['tension']))
            parts.append("")
        
        # Poster concept
        if 'poster' in response_data:
            parts.append(self._format_poster(response_data['poster']))
            parts.append("")
        
        # UNMASK
        if 'unmask' in response_data:
            parts.append(self._format_unmask(response_data['unmask']))
            parts.append("")
        
        # Verified sources
        if 'sources' in response_data and response_data['sources']:
            parts.append(self._format_sources(response_data['sources']))
        
        return "\n".join(parts)
    
    def _format_log_safe(self, response_data: Dict[str, Any]) -> str:
        """Format response for logging without emojis"""
        # Temporarily disable emojis
        original_emoji_state = self.enable_emojis
        self.enable_emojis = False
        
        result = self._format_display(response_data)
        
        # Restore original state
        self.enable_emojis = original_emoji_state
        
        return result
    
    def _format_header(self, country: str, round_num: int) -> str:
        """Format country header with separator"""
        flag = self._get_flag(country) if self.enable_emojis else ""
        header = f"{flag} {country} (Round {round_num})".strip()
        separator = "━" * self.separator_width if self.enable_emojis else "=" * self.separator_width
        return f"{header}\n{separator}"
    
    def _format_search_narration(self, search_data: Dict[str, str]) -> str:
        """Format search narration"""
        symbol = self._get_symbol('search')
        narration = search_data.get('narration', '')
        query = search_data.get('query', '')
        
        # Format with italics (markdown style)
        return f"    {symbol} *{narration}*"
    
    def _format_costly_signal(self, signal_data: Dict[str, Any]) -> str:
        """Format costly signal with appropriate symbol"""
        signal_type = signal_data.get('type', 'REDUCIBLE_COSTS')
        content = signal_data.get('content', '')
        
        # Map signal type to symbol
        symbol_map = {
            'TYING_HANDS': 'tying_hands',
            'SUNK_COSTS': 'sunk_costs',
            'INSTALLMENT_COSTS': 'installment_costs',
            'REDUCIBLE_COSTS': 'reducible_costs'
        }
        
        symbol = self._get_symbol(symbol_map.get(signal_type, 'reducible_costs'))
        label = self.signal_labels.get(SignalType(signal_type), 'SIGNAL')
        type_label = signal_type.replace('_', ' ').title()
        
        return f"    {symbol} {label} [{type_label}]\n    └─ {self._wrap_text(content, 7)}"
    
    def _format_performance(self, performance_data: Dict[str, str]) -> str:
        """Format performance fiction"""
        symbol = self._get_symbol('performance')
        content = performance_data.get('content', '')
        
        return f"    {symbol} PERFORMANCE\n    └─ {self._wrap_text(content, 7)}"
    
    def _format_tension(self, tension: str) -> str:
        """Format signal-fiction tension"""
        symbol = self._get_symbol('tension')
        return f"    {symbol} TENSION: {self._wrap_text(tension, 14)}"
    
    def _format_poster(self, poster_data: Dict[str, str]) -> str:
        """Format poster concept"""
        symbol = self._get_symbol('poster')
        lines = [f"    {symbol} POSTER"]
        
        if 'inscriptio' in poster_data:
            lines.append(f"    ├─ INSCRIPTIO: \"{poster_data['inscriptio']}\"")
        if 'pictura' in poster_data:
            lines.append(f"    ├─ PICTURA: {poster_data['pictura']}")
        if 'subscriptio' in poster_data:
            lines.append(f"    └─ SUBSCRIPTIO: \"{poster_data['subscriptio']}\"")
        
        return "\n".join(lines)
    
    def _format_unmask(self, unmask_data: Dict[str, str]) -> str:
        """Format UNMASK challenge"""
        symbol = self._get_symbol('unmask')
        content = unmask_data.get('content', '')
        target = unmask_data.get('target', '')
        
        header = f"    {symbol} UNMASK"
        if target:
            header += f" [{target}]"
        
        return f"{header}\n    └─ {self._wrap_text(content, 7)}"
    
    def _format_sources(self, sources: List[Dict[str, str]]) -> str:
        """Format verified sources"""
        symbol = self._get_symbol('verified')
        lines = []
        
        for i, source in enumerate(sources):
            name = source.get('name', 'Unknown Source')
            timestamp = source.get('timestamp', '')
            url = source.get('url', '')
            excerpt = source.get('excerpt', '')
            
            # Format timestamp
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    timestamp_str = dt.strftime('%Y-%m-%dT%H:%M:%S')
                except:
                    timestamp_str = timestamp
            else:
                timestamp_str = 'No timestamp'
            
            lines.append(f"    {symbol} VERIFIED SOURCE")
            lines.append(f"    └─ {name} • {timestamp_str} • {url}")
            if excerpt:
                lines.append(f"       \"{excerpt}\"")
        
        return "\n".join(lines)
    
    def _get_symbol(self, symbol_type: str) -> str:
        """Get symbol with fallback for non-emoji mode"""
        if self.enable_emojis:
            return self.symbols.get(symbol_type, '')
        return self.ascii_symbols.get(symbol_type, f'[{symbol_type.upper()}]')
    
    def _get_flag(self, country: str) -> str:
        """Get country flag emoji"""
        if self.enable_emojis:
            return self.flags.get(country, '🏳️')
        return f"[{country.upper()[:2]}]"
    
    def _wrap_text(self, text: str, indent: int) -> str:
        """
        Wrap text with proper indentation for multi-line content
        
        Args:
            text: Text to wrap
            indent: Number of spaces to indent wrapped lines
            
        Returns:
            Wrapped text
        """
        # Simple wrapping - in production, use textwrap module
        if len(text) <= (self.separator_width - indent):
            return text
        
        # For now, return as-is
        # TODO: Implement proper text wrapping
        return text
    
    def export_structured_log(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Export response data in structured format for logging/analysis
        
        Args:
            response_data: Original response data
            
        Returns:
            Structured log entry
        """
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'country': response_data.get('country', 'Unknown'),
            'round': response_data.get('round', 0),
            'action_type': 'debate_response',
            'components': {}
        }
        
        # Add search info
        if 'search' in response_data:
            log_entry['components']['search'] = {
                'query': response_data['search'].get('query', ''),
                'narration': response_data['search'].get('narration', '')
            }
        
        # Add signal info
        if 'costly_signal' in response_data:
            signal = response_data['costly_signal']
            log_entry['components']['signal'] = {
                'type': signal.get('type', ''),
                'category': self._get_signal_category(signal.get('type', '')),
                'content_length': len(signal.get('content', ''))
            }
        
        # Add performance info
        if 'performance' in response_data:
            log_entry['components']['performance'] = {
                'present': True,
                'content_length': len(response_data['performance'].get('content', ''))
            }
        
        # Add tension info
        if 'tension' in response_data:
            log_entry['components']['tension'] = {
                'present': True,
                'content_length': len(response_data['tension'])
            }
        
        # Add source info
        if 'sources' in response_data:
            log_entry['components']['sources'] = {
                'count': len(response_data['sources']),
                'sources': [
                    {
                        'name': s.get('name', ''),
                        'timestamp': s.get('timestamp', '')
                    } for s in response_data['sources']
                ]
            }
        
        # Add main speech info
        if 'main_speech' in response_data:
            log_entry['components']['main_speech'] = {
                'length': len(response_data['main_speech']),
                'word_count': len(response_data['main_speech'].split())
            }
        
        return log_entry
    
    def _get_signal_category(self, signal_type: str) -> str:
        """Map signal type to category for analysis"""
        categories = {
            'TYING_HANDS': 'binding_commitment',
            'SUNK_COSTS': 'irreversible_investment',
            'INSTALLMENT_COSTS': 'ongoing_commitment',
            'REDUCIBLE_COSTS': 'flexible_position'
        }
        return categories.get(signal_type, 'unknown')


def strip_emojis(text: str) -> str:
    """
    Remove all emoji characters from text
    
    Args:
        text: Input text with potential emojis
        
    Returns:
        Text with emojis removed
    """
    # Pattern to match most emoji characters
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", 
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)


def replace_emojis(text: str, replacements: Dict[str, str]) -> str:
    """
    Replace specific emojis with text alternatives
    
    Args:
        text: Input text with emojis
        replacements: Dictionary mapping emojis to replacements
        
    Returns:
        Text with emojis replaced
    """
    for emoji, replacement in replacements.items():
        text = text.replace(emoji, replacement)
    return text


# Example usage and testing
if __name__ == "__main__":
    import sys
    import io
    
    # Set stdout to handle UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # Test data
    test_response = {
        "country": "United States",
        "round": 0,
        "search": {
            "query": "US AI companies regulatory burden 2024",
            "narration": "frantically searches for US AI companies regulatory burden 2024"
        },
        "main_speech": "The United States views AI governance through the prism of maintaining a secure and competitive technological ecosystem. Our recent regulatory efforts reflect a commitment to balancing innovation with national security.",
        "costly_signal": {
            "type": "TYING_HANDS",
            "content": "We are introducing legislation requiring all AI systems above 10^26 FLOPS to undergo mandatory federal safety certification before deployment."
        },
        "performance": {
            "content": "The President signs the AI Accountability Act as tech CEOs stand witness, their signatures binding them to a new social contract."
        },
        "tension": "The public ceremony transforms legal commitment into political theater - the constraint becomes a crown.",
        "sources": [{
            "name": "Perplexity AI",
            "timestamp": "2025-08-16T12:03:56.309408",
            "url": "https://perplexity.ai",
            "excerpt": "The US CHIPS Act allocates $52 billion for semiconductor manufacturing..."
        }]
    }
    
    try:
        # Test with emojis
        formatter = DebateFormatter()
        print("=== DISPLAY FORMAT (with emojis) ===")
        print(formatter.format_response(test_response))
    except UnicodeEncodeError:
        print("Unicode encoding error - falling back to log-safe mode")
        formatter = DebateFormatter({'enable_emojis': False})
        print(formatter.format_response(test_response))
    
    print("\n\n=== LOG-SAFE FORMAT (no emojis) ===")
    formatter_log = DebateFormatter({'enable_emojis': False})
    print(formatter_log.format_response(test_response, for_logging=True))
    
    print("\n\n=== STRUCTURED LOG ===")
    print(json.dumps(formatter.export_structured_log(test_response), indent=2))
    
    # Test emoji stripping
    print("\n\n=== EMOJI STRIPPING TEST ===")
    test_text = "🇺🇸 United States 🔍 searches for 💎 binding commitments"
    print(f"Original: {test_text}")
    print(f"Stripped: {strip_emojis(test_text)}")
    
    # Test emoji replacement
    print("\n\n=== EMOJI REPLACEMENT TEST ===")
    replacements = {
        '🇺🇸': '[US]',
        '🔍': '[SEARCH]',
        '💎': '[BINDING]'
    }
    print(f"Original: {test_text}")
    print(f"Replaced: {replace_emojis(test_text, replacements)}")