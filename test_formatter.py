"""
Unit tests for debate formatter and emoji handling
"""

import unittest
import json
from debate_formatter import DebateFormatter, SignalType, strip_emojis, replace_emojis
from debate_formatter_integration import DebateResponseParser


class TestEmojiHandling(unittest.TestCase):
    """Test emoji stripping and replacement functions"""
    
    def test_strip_emojis(self):
        """Test emoji stripping functionality"""
        test_cases = [
            ("🇺🇸 United States 🔍 searches", " United States  searches"),
            ("💎 BINDING COMMITMENT", " BINDING COMMITMENT"),
            ("No emojis here", "No emojis here"),
            ("Mixed 🎭 text with 💰 emojis", "Mixed  text with  emojis"),
            ("🔍🔍🔍", ""),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input=input_text):
                result = strip_emojis(input_text)
                self.assertEqual(result, expected)
    
    def test_replace_emojis(self):
        """Test emoji replacement functionality"""
        replacements = {
            '🇺🇸': '[US]',
            '🔍': '[SEARCH]',
            '💎': '[BINDING]'
        }
        
        test_cases = [
            ("🇺🇸 United States", "[US] United States"),
            ("🔍 searching for info", "[SEARCH] searching for info"),
            ("💎 binding commitment", "[BINDING] binding commitment"),
            ("🇺🇸 🔍 💎", "[US] [SEARCH] [BINDING]"),
            ("No emojis", "No emojis"),
            ("Unknown emoji 🎭", "Unknown emoji 🎭"),  # Unspecified emoji unchanged
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input=input_text):
                result = replace_emojis(input_text, replacements)
                self.assertEqual(result, expected)


class TestDebateFormatter(unittest.TestCase):
    """Test the main debate formatter functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.formatter_with_emojis = DebateFormatter({'enable_emojis': True})
        self.formatter_no_emojis = DebateFormatter({'enable_emojis': False})
        
        self.test_response = {
            "country": "United States",
            "round": 1,
            "search": {
                "query": "AI regulation 2024",
                "narration": "frantically searches for AI regulation 2024"
            },
            "main_speech": "The United States believes in balanced AI governance.",
            "costly_signal": {
                "type": "TYING_HANDS",
                "content": "We are introducing new legislation."
            },
            "performance": {
                "content": "The President signs the act."
            },
            "tension": "Legal commitment becomes political theater.",
            "sources": [{
                "name": "Test Source",
                "timestamp": "2024-01-01T12:00:00",
                "url": "https://example.com",
                "excerpt": "Test excerpt"
            }]
        }
    
    def test_format_with_emojis(self):
        """Test formatting with emojis enabled"""
        result = self.formatter_with_emojis.format_response(self.test_response)
        
        # Check for emoji presence
        self.assertIn('🇺🇸', result)
        self.assertIn('🔍', result)
        self.assertIn('💎', result)
        self.assertIn('🎭', result)
        self.assertIn('⚡', result)
        self.assertIn('✓', result)
    
    def test_format_without_emojis(self):
        """Test formatting with emojis disabled"""
        result = self.formatter_no_emojis.format_response(self.test_response)
        
        # Check for ASCII replacements
        self.assertIn('[SEARCH]', result)
        self.assertIn('[BINDING]', result)
        self.assertIn('[PERFORM]', result)
        self.assertIn('[TENSION]', result)
        self.assertIn('[VERIFIED]', result)
        
        # Ensure no emojis present
        self.assertNotIn('🇺🇸', result)
        self.assertNotIn('🔍', result)
    
    def test_log_safe_format(self):
        """Test log-safe formatting"""
        result = self.formatter_with_emojis.format_response(self.test_response, for_logging=True)
        
        # Should not contain emojis even if formatter has emojis enabled
        self.assertNotIn('🇺🇸', result)
        self.assertNotIn('🔍', result)
        
        # Should contain ASCII replacements
        self.assertIn('[SEARCH]', result)
        self.assertIn('[BINDING]', result)
    
    def test_structured_log_export(self):
        """Test structured log export"""
        log_entry = self.formatter_with_emojis.export_structured_log(self.test_response)
        
        # Check structure
        self.assertIn('timestamp', log_entry)
        self.assertIn('country', log_entry)
        self.assertIn('round', log_entry)
        self.assertIn('components', log_entry)
        
        # Check components
        components = log_entry['components']
        self.assertIn('search', components)
        self.assertIn('signal', components)
        self.assertIn('performance', components)
        self.assertIn('tension', components)
        self.assertIn('sources', components)
        
        # Verify signal classification
        self.assertEqual(components['signal']['type'], 'TYING_HANDS')
        self.assertEqual(components['signal']['category'], 'binding_commitment')
    
    def test_signal_type_formatting(self):
        """Test different signal types format correctly"""
        signal_types = [
            ("TYING_HANDS", "💎", "BINDING COMMITMENT"),
            ("SUNK_COSTS", "💰", "SUNK COST"),
            ("INSTALLMENT_COSTS", "🔄", "ONGOING PROGRAM"),
            ("REDUCIBLE_COSTS", "🎯", "FLEXIBLE POSITION")
        ]
        
        for signal_type, emoji, label in signal_types:
            with self.subTest(signal_type=signal_type):
                test_data = self.test_response.copy()
                test_data['costly_signal']['type'] = signal_type
                
                result = self.formatter_with_emojis.format_response(test_data)
                self.assertIn(emoji, result)
                self.assertIn(label, result)


class TestResponseParser(unittest.TestCase):
    """Test the response parser functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = DebateResponseParser()
        
        self.test_raw_response = """*frantically searches for AI regulation updates*

The United States maintains its position on balanced governance.

[COSTLY SIGNAL - TYING_HANDS]: We are introducing comprehensive legislation.

[PERFORMANCE FICTION]: The President signs the AI Act with industry leaders present.

[SIGNAL-FICTION TENSION]: The ceremony transforms policy into theater.

[1] Reuters (2024-01-01T12:00:00): VERIFIED FACT - https://reuters.com"""
    
    def test_parse_basic_response(self):
        """Test parsing a basic response"""
        result = self.parser.parse_response("United States", self.test_raw_response, 1)
        
        # Check basic fields
        self.assertEqual(result['country'], "United States")
        self.assertEqual(result['round'], 1)
        
        # Check search extraction
        self.assertIn('search', result)
        self.assertIn('frantically searches', result['search']['narration'])
        
        # Check signal extraction
        self.assertIn('costly_signal', result)
        self.assertEqual(result['costly_signal']['type'], 'TYING_HANDS')
        
        # Check performance extraction
        self.assertIn('performance', result)
        self.assertIn('President signs', result['performance']['content'])
        
        # Check tension extraction
        self.assertIn('tension', result)
        self.assertIn('ceremony transforms', result['tension'])
        
        # Check source extraction
        self.assertEqual(len(result['sources']), 1)
        self.assertEqual(result['sources'][0]['name'], 'Reuters')
    
    def test_parse_response_with_unmask(self):
        """Test parsing response with UNMASK"""
        response_with_unmask = self.test_raw_response + "\n\n[UNMASK] China's claims lack material evidence."
        
        result = self.parser.parse_response("United States", response_with_unmask, 1)
        
        self.assertIn('unmask', result)
        self.assertIn("China's claims", result['unmask']['content'])
    
    def test_parse_response_with_poster(self):
        """Test parsing response with poster concept"""
        response_with_poster = self.test_raw_response + """

[POSTER CONCEPT]:
INSCRIPTIO: Freedom Through Innovation
PICTURA: Eagle soaring over silicon chips
SUBSCRIPTIO: Technology serves democracy"""
        
        result = self.parser.parse_response("United States", response_with_poster, 1)
        
        self.assertIn('poster', result)
        self.assertEqual(result['poster']['inscriptio'], 'Freedom Through Innovation')
        self.assertEqual(result['poster']['pictura'], 'Eagle soaring over silicon chips')
        self.assertEqual(result['poster']['subscriptio'], 'Technology serves democracy')


class TestFormatterIntegration(unittest.TestCase):
    """Test the integration of parser and formatter"""
    
    def test_round_trip_formatting(self):
        """Test parsing and reformatting maintains information"""
        parser = DebateResponseParser()
        formatter = DebateFormatter({'enable_emojis': False})  # Use ASCII for comparison
        
        original = """*searches for latest AI developments*

The EU champions responsible innovation.

[COSTLY SIGNAL - SUNK_COSTS]: We have invested €10 billion in AI infrastructure.

[PERFORMANCE FICTION]: Brussels becomes the global AI ethics capital.

[SIGNAL-FICTION TENSION]: Infrastructure meets ideals.

[1] EU Commission (2024-01-01): VERIFIED FACT - https://ec.europa.eu"""
        
        # Parse
        parsed = parser.parse_response("European Union", original, 2)
        
        # Format
        formatted = formatter.format_response(parsed)
        
        # Check key elements preserved
        self.assertIn("searches for latest AI developments", formatted)
        self.assertIn("The EU champions responsible innovation", formatted)
        self.assertIn("€10 billion", formatted)
        self.assertIn("Brussels becomes", formatted)
        self.assertIn("Infrastructure meets ideals", formatted)
        self.assertIn("EU Commission", formatted)


if __name__ == '__main__':
    # Run tests with verbosity
    unittest.main(verbosity=2)