"""
Integration module to connect the debate formatter with existing debate system
"""

import re
import json
from typing import Dict, List, Optional, Any, Tuple
from debate_formatter import DebateFormatter, SignalType
import logging


class DebateResponseParser:
    """Parse existing debate responses into structured format for the formatter"""
    
    def __init__(self):
        self.patterns = {
            'search_narration': r'\*(.*?searches.*?)\*',
            'costly_signal': r'\[COSTLY SIGNAL - ([A-Z_]+)\]:\s*(.+?)(?=\n\[|\n\n|$)',
            'performance_fiction': r'\[PERFORMANCE FICTION\]:\s*(.+?)(?=\n\[|\n\n|$)',
            'tension': r'\[SIGNAL-FICTION TENSION\]:\s*(.+?)(?=\n\[|\n\n|$)',
            'poster': r'\[POSTER CONCEPT\]:\s*INSCRIPTIO:\s*(.+?)\s*PICTURA:\s*(.+?)\s*SUBSCRIPTIO:\s*(.+?)(?=\n\[|\n\n|$)',
            'unmask': r'\[UNMASK\]\s*(.+?)(?=\n\n|$)',
            'citations': r'\[(\d+)\]\s*(.+?):\s*(VERIFIED FACT|STRATEGIC POSITION|ESTABLISHED POLICY)\s*-\s*(.+?)(?=\n|$)'
        }
    
    def parse_response(self, agent_name: str, response: str, round_num: int) -> Dict[str, Any]:
        """
        Parse a debate response into structured components
        
        Args:
            agent_name: Name of the agent
            response: Raw response text
            round_num: Current round number
            
        Returns:
            Structured response data for formatter
        """
        # Initialize result structure
        result = {
            'country': agent_name,
            'round': round_num,
            'sources': []
        }
        
        # Extract search narration
        search_match = re.search(self.patterns['search_narration'], response, re.DOTALL)
        if search_match:
            narration = search_match.group(1)
            # Try to extract query from narration
            query_match = re.search(r'searches for["\s]+(.+?)["\s]*(?:briefly|$)', narration)
            query = query_match.group(1) if query_match else "unknown query"
            result['search'] = {
                'narration': narration,
                'query': query
            }
        
        # Extract main speech (everything before the first meta-element)
        main_speech_end = response.find('[COSTLY SIGNAL')
        if main_speech_end == -1:
            main_speech_end = response.find('[PERFORMANCE FICTION')
        if main_speech_end == -1:
            main_speech_end = response.find('[UNMASK')
        
        if main_speech_end > 0:
            main_speech = response[:main_speech_end].strip()
            # Remove search narration from main speech
            if search_match:
                main_speech = main_speech.replace(search_match.group(0), '').strip()
            result['main_speech'] = main_speech
        else:
            # No meta-elements found, entire response is main speech
            result['main_speech'] = response.strip()
        
        # Extract costly signal
        signal_match = re.search(self.patterns['costly_signal'], response, re.DOTALL)
        if signal_match:
            signal_type = signal_match.group(1)
            signal_content = signal_match.group(2).strip()
            result['costly_signal'] = {
                'type': signal_type,
                'content': signal_content
            }
        
        # Extract performance fiction
        fiction_match = re.search(self.patterns['performance_fiction'], response, re.DOTALL)
        if fiction_match:
            result['performance'] = {
                'content': fiction_match.group(1).strip()
            }
        
        # Extract tension
        tension_match = re.search(self.patterns['tension'], response, re.DOTALL)
        if tension_match:
            result['tension'] = tension_match.group(1).strip()
        
        # Extract poster
        poster_match = re.search(self.patterns['poster'], response, re.DOTALL)
        if poster_match:
            result['poster'] = {
                'inscriptio': poster_match.group(1).strip(),
                'pictura': poster_match.group(2).strip(),
                'subscriptio': poster_match.group(3).strip()
            }
        
        # Extract UNMASK
        unmask_match = re.search(self.patterns['unmask'], response, re.DOTALL)
        if unmask_match:
            result['unmask'] = {
                'content': unmask_match.group(1).strip()
            }
        
        # Extract citations and convert to sources
        citations = re.findall(self.patterns['citations'], response, re.MULTILINE)
        for citation in citations:
            num, source_info, fact_type, url = citation
            # Parse timestamp if present
            timestamp_match = re.search(r'\((\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}[^)]*)\)', source_info)
            if timestamp_match:
                timestamp = timestamp_match.group(1)
                source_name = source_info[:timestamp_match.start()].strip()
            else:
                timestamp = ""
                source_name = source_info
            
            result['sources'].append({
                'name': source_name,
                'timestamp': timestamp,
                'url': url.strip(),
                'excerpt': f"{fact_type}: {url.strip()}"
            })
        
        return result


class FormattedDebateManager:
    """Extension of DebateManager that uses the new formatter"""
    
    def __init__(self, original_manager, formatter_config: Optional[Dict] = None):
        """
        Initialize with reference to original manager
        
        Args:
            original_manager: The existing DebateManager instance
            formatter_config: Optional configuration for formatter
        """
        self.manager = original_manager
        self.formatter = DebateFormatter(formatter_config)
        self.parser = DebateResponseParser()
        self.formatter_config = formatter_config or {}
        
    def format_response(self, agent_name: str, response: str, round_num: int, 
                       for_logging: bool = False) -> str:
        """
        Format a debate response using the new formatter
        
        Args:
            agent_name: Name of the agent
            response: Raw response text
            round_num: Current round number
            for_logging: Whether to format for logging (no emojis)
            
        Returns:
            Formatted response
        """
        try:
            # Parse the response
            structured_data = self.parser.parse_response(agent_name, response, round_num)
            
            # Format using the new formatter
            formatted = self.formatter.format_response(structured_data, for_logging)
            
            return formatted
        except Exception as e:
            logging.error(f"Error formatting response: {e}")
            # Fallback to original response
            return response
    
    def get_structured_log_entry(self, agent_name: str, response: str, 
                                round_num: int) -> Dict[str, Any]:
        """
        Get structured log entry for a response
        
        Args:
            agent_name: Name of the agent
            response: Raw response text
            round_num: Current round number
            
        Returns:
            Structured log entry
        """
        try:
            structured_data = self.parser.parse_response(agent_name, response, round_num)
            return self.formatter.export_structured_log(structured_data)
        except Exception as e:
            logging.error(f"Error creating structured log: {e}")
            return {
                'error': str(e),
                'agent': agent_name,
                'round': round_num
            }


def integrate_formatter_with_manager(debate_manager, formatter_config: Optional[Dict] = None):
    """
    Monkey-patch the existing DebateManager to use the new formatter
    
    Args:
        debate_manager: Existing DebateManager instance
        formatter_config: Optional formatter configuration
    """
    # Create formatter wrapper
    formatter_wrapper = FormattedDebateManager(debate_manager, formatter_config)
    
    # Store original methods
    debate_manager._original_start_debate = debate_manager.start_debate
    debate_manager._original_next_turn = debate_manager.next_turn
    
    # Store original log_debate_turn if it exists
    if hasattr(debate_manager, 'logger') and hasattr(debate_manager.logger, 'log_debate_turn'):
        debate_manager.logger._original_log_debate_turn = debate_manager.logger.log_debate_turn
        
        # Create enhanced log_debate_turn that logs both formats
        def enhanced_log_debate_turn(agent_name: str, message: str):
            # Log original message
            debate_manager.logger._original_log_debate_turn(agent_name, message)
            
            # Also log structured format
            try:
                # Get current round from conversation history
                round_num = len(debate_manager.conversation_history)
                
                # Create log-safe formatted version
                structured_data = formatter_wrapper.parser.parse_response(agent_name, message, round_num)
                log_safe_formatted = formatter_wrapper.formatter.format_response(structured_data, for_logging=True)
                
                # Log the formatted version
                debate_manager.logger.logger.info(f"[FORMATTED LOG-SAFE VERSION]\n{log_safe_formatted}\n{'-'*50}")
                
                # Log structured data as JSON
                structured_log = formatter_wrapper.get_structured_log_entry(agent_name, message, round_num)
                debate_manager.logger.logger.info(f"[STRUCTURED DATA]\n{json.dumps(structured_log, indent=2)}\n{'-'*50}")
                
            except Exception as e:
                debate_manager.logger.logger.error(f"Error creating formatted log: {str(e)}")
        
        # Replace the log_debate_turn method
        debate_manager.logger.log_debate_turn = enhanced_log_debate_turn
    
    # Create new methods that use formatter
    async def formatted_start_debate(debate_prompt: str = None):
        # Get original response
        response = await debate_manager._original_start_debate(debate_prompt)
        
        # Format the response
        if response and debate_manager.conversation_history:
            last_entry = debate_manager.conversation_history[-1]
            agent_name = last_entry['agent']
            round_num = last_entry.get('round', 1)
            
            # Format for display
            formatted_response = formatter_wrapper.format_response(
                agent_name, response, round_num, for_logging=False
            )
            
            # Log structured version
            log_entry = formatter_wrapper.get_structured_log_entry(
                agent_name, response, round_num
            )
            logging.info(f"Structured log: {log_entry}")
            
            return formatted_response
        
        return response
    
    async def formatted_next_turn(debate_prompt: str = None):
        # Get original response
        response = await debate_manager._original_next_turn(debate_prompt)
        
        # Format the response
        if response and debate_manager.conversation_history:
            last_entry = debate_manager.conversation_history[-1]
            agent_name = last_entry['agent']
            round_num = last_entry.get('round', 1)
            
            # Format for display
            formatted_response = formatter_wrapper.format_response(
                agent_name, response, round_num, for_logging=False
            )
            
            # Log structured version
            log_entry = formatter_wrapper.get_structured_log_entry(
                agent_name, response, round_num
            )
            logging.info(f"Structured log: {log_entry}")
            
            return formatted_response
        
        return response
    
    # Replace methods
    debate_manager.start_debate = formatted_start_debate
    debate_manager.next_turn = formatted_next_turn
    
    # Add formatter reference
    debate_manager.formatter = formatter_wrapper
    
    return debate_manager


# Example usage
if __name__ == "__main__":
    # Test the parser
    test_response = """*frantically searches for US AI companies regulatory burden 2024*

The United States views AI governance through the prism of maintaining a secure and competitive technological ecosystem.

[COSTLY SIGNAL - TYING_HANDS]: We are introducing legislation requiring all AI systems above 10^26 FLOPS to undergo mandatory federal safety certification.

[PERFORMANCE FICTION]: The President signs the AI Accountability Act as tech CEOs stand witness.

[SIGNAL-FICTION TENSION]: The public ceremony transforms legal commitment into political theater.

[1] Perplexity AI (2025-08-16T12:03:56): VERIFIED FACT - https://perplexity.ai"""

    parser = DebateResponseParser()
    parsed = parser.parse_response("United States", test_response, 0)
    
    print("=== PARSED DATA ===")
    import json
    print(json.dumps(parsed, indent=2))
    
    print("\n=== FORMATTED OUTPUT ===")
    formatter = DebateFormatter()
    print(formatter.format_response(parsed))
