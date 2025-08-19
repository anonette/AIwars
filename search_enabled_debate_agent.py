"""
Search-Enabled Debate Agent with Costly Signals and Performance Fictions
Implements the double-entry system of credibility (Fearon) and dramaturgy (Ezrahi)
"""

import logging
import asyncio
from typing import List, Dict, Optional, Tuple
from document_integration import DocumentEnabledDebateAgent
from perplexity_search import (
    PerplexitySearchClient,
    perform_strategic_search,
    SignalType
)
from document_retrieval import DocumentStore
import re
import random

class SearchEnabledDebateAgent(DocumentEnabledDebateAgent):
    """
    Extended debate agent with search capabilities and double-entry system:
    - Costly signals (Fearon's credibility ledger)
    - Performance fictions (Ezrahi's dramaturgy)
    - Unmasking capabilities to denaturalize rivals' claims
    """
    
    def __init__(self, name: str, personality: str, agent_config_key: str, 
                 config: dict = None, document_store: Optional[DocumentStore] = None,
                 search_client: Optional[PerplexitySearchClient] = None):
        """Initialize with both document and search capabilities"""
        super().__init__(name, personality, agent_config_key, config, document_store)
        
        # Initialize search client
        self.search_client = search_client or PerplexitySearchClient()
        
        # Track signals and performances
        self.last_costly_signal = None
        self.last_performance_fiction = None
        self.unmasking_attempts = []
        
        # Round tracking for special actions
        self.current_round = 0
        self.rounds_since_last_unmask = 0
        
        logging.info(f"Initialized search-enabled agent {name} with double-entry system")
    
    async def generate_response(self, context: str, last_message: str, 
                              debate_prompt: str = None) -> str:
        """
        Generate response with integrated search, documents, and double-entry analysis
        """
        try:
            # Update round tracking
            self._update_round_tracking(debate_prompt)
            
            # Extract topic and analyze context
            topic = self._extract_topic(context)
            
            # Decision: Search, documents, or both?
            decision = await self._decide_information_source(topic, last_message, context)
            
            # Gather information based on decision
            search_results = None
            doc_context = ""
            
            if decision in ["search", "both"]:
                search_results = await perform_strategic_search(
                    self.search_client, self.name, topic, last_message, context
                )
                # Store search results for theoretical analysis
                self._last_search_results = search_results
            
            if decision in ["documents", "both"]:
                doc_context, used_docs = self._get_document_context_with_tracking(
                    self.name, last_message, topic
                )
                self.last_used_documents = used_docs
            
            # Generate the double-entry response with dynamic content
            response = await self._generate_dynamic_double_entry_response(
                context, last_message, topic, search_results, doc_context
            )
            
            # UNMASK: Occasionally attempt to denaturalize a rival's claim
            if self._should_attempt_unmask(context, last_message):
                unmask_attempt = self._generate_unmask_attempt(context, last_message)
                if unmask_attempt:
                    response = f"{unmask_attempt}\n\n{response}"
                    self.rounds_since_last_unmask = 0
            
            # Add citations if we have search results or documents
            if (search_results and search_results.get("results")) or self.last_used_documents:
                citations = self._format_comprehensive_citations(search_results, self.last_used_documents)
                if citations:
                    response = f"{response}\n\n{citations}"
            
            return response
            
        except Exception as e:
            logging.error(f"Error in search-enabled response: {repr(e)}")
            import traceback
            logging.error(traceback.format_exc())
            return await super().generate_response(context, last_message, debate_prompt)
    
    def _should_attempt_unmask(self, context: str, last_message: str) -> bool:
        """Determine if we should attempt unmasking this round"""
        # Once per round rule
        if self.rounds_since_last_unmask < 1:
            return False
        
        # Look for stagecraft indicators in rival's message
        stagecraft_indicators = [
            "commits to", "promises", "guarantees", "ensures", "vows",
            "will establish", "will create", "will build", "pledges",
            "demonstrates", "shows leadership", "leads the way"
        ]
        
        message_lower = last_message.lower()
        return any(indicator in message_lower for indicator in stagecraft_indicators)
    
    def _generate_unmask_attempt(self, context: str, last_message: str) -> Optional[str]:
        """
        UNMASK: Identify pure stagecraft and propose minimum anchor for credibility
        """
        # Extract the speaker from last message
        speaker_match = re.match(r"^([^:]+):", last_message)
        rival = speaker_match.group(1) if speaker_match else "The previous speaker"
        
        # Patterns that indicate unanchored claims
        unanchored_patterns = [
            (r"(?:commits to|promises) (\w+(?:\s+\w+){0,3})", "commitment"),
            (r"(?:will ensure|guarantees) (\w+(?:\s+\w+){0,3})", "guarantee"),
            (r"(?:will establish|will create) (\w+(?:\s+\w+){0,3})", "creation"),
            (r"(?:leads the way in|demonstrates leadership in) (\w+(?:\s+\w+){0,3})", "leadership claim"),
            (r"(?:our|we have) (?:sovereignty|supremacy|dominance) in (\w+(?:\s+\w+){0,3})", "sovereignty claim")
        ]
        
        for pattern, claim_type in unanchored_patterns:
            match = re.search(pattern, last_message, re.IGNORECASE)
            if match:
                claim = match.group(1)
                full_claim = match.group(0)
                
                # Generate specific anchoring requirements based on rival and claim type
                anchor_requirements = self._get_anchor_requirements(rival, claim_type, claim)
                
                unmask = f"[UNMASK] {rival}'s claim to '{full_claim}' operates as pure stagecraft - "
                unmask += f"a performance without material substrate. "
                unmask += f"Minimum anchors for credibility: {anchor_requirements}"
                
                return unmask
        
        # If no specific pattern, look for general theatrical language
        theatrical_words = ["revolutionary", "unprecedented", "transformative", "historic", "groundbreaking"]
        for word in theatrical_words:
            if word in last_message.lower():
                # Skip hardcoded unmask generation - let LLM handle it naturally
                return None
        
        return None
    
    async def _get_anchor_requirements(self, rival: str, claim_type: str, claim: str) -> str:
        """
        Generate specific anchor requirements using LLM analysis of the rival's governance system
        """
        prompt = f"""
        A political analyst is examining {rival}'s claim about "{claim}" (claim type: {claim_type}). 
        
        What specific, verifiable anchors would be needed to move this claim from political theater to credible commitment? 
        Consider {rival}'s governmental structure, accountability mechanisms, and policy-making processes.
        
        Provide exactly 4 concrete requirements in format: (1) [requirement], (2) [requirement], (3) [requirement], (4) [requirement]
        
        Focus on institutional mechanisms, budget allocations, legal frameworks, or oversight structures that would make this claim costly to reverse.
        """
        
        try:
            # Use LLM to generate contextual anchor requirements
            original_personality = self.personality
            self.personality = "You are a political analyst specializing in governmental accountability mechanisms and credible commitment theory."
            
            requirements = await super().generate_response(prompt, "", None)
            self.personality = original_personality
            
            return requirements.strip()
        except Exception as e:
            logging.error(f"Error generating anchor requirements: {e}")
            return ""  # Return empty instead of hardcoded fallback
    
    async def _decide_information_source(self, topic: str, last_message: str,
                                       context: str) -> str:
        """
        ALWAYS use both search and documents to ensure comprehensive responses
        
        1. Search provides recent initiatives and current developments
        2. Documents provide official positions and policy frameworks
        """
        # Always return "both" to ensure agents:
        # 1. Search for recent AI initiatives from their country
        # 2. Consult RAG documents for official positions
        # 3. Generate responses grounded in both sources
        return "both"
    
    async def _generate_dynamic_double_entry_response(self, context: str, last_message: str,
                                                    topic: str, search_results: Optional[Dict],
                                                    doc_context: str) -> str:
        """
        Generate response through LLM analysis of meta-sovereignty framework
        """
        # Generate base response first
        base_content = await self._generate_base_content(
            context, last_message, topic, search_results, doc_context
        )
        
        # Strip action phrases from base content
        base_content = self._strip_action_phrases(base_content)
        
        # Now ask the LLM to analyze search results for theoretical frameworks
        analysis_prompt = self._create_meta_sovereignty_analysis_prompt(
            base_content, context, topic, search_results, doc_context
        )
        
        # Get LLM analysis of costly signals, performance fictions, and tensions
        analysis = await self._generate_llm_framework_analysis(analysis_prompt)
        
        # Only add analysis if it contains the expected framework elements
        if analysis and any(marker in analysis for marker in ['[COSTLY SIGNAL', '[PERFORMANCE FICTION', '[SIGNAL-FICTION']):
            return f"{base_content}\n\n{analysis}"
        else:
            # If analysis failed, just return base content with simple citation
            citations = self._format_simple_citations(search_results)
            return f"{base_content}{citations}"
    
    def _create_meta_sovereignty_analysis_prompt(self, base_response: str, context: str,
                                               topic: str, search_results: Optional[Dict],
                                               doc_context: str) -> str:
        """
        Create a prompt for LLM to analyze the response through meta-sovereignty lens using real search data
        """
        # Extract comprehensive search information
        search_evidence = ""
        if search_results and search_results.get("results"):
            search_evidence = "REAL-WORLD EVIDENCE FROM SEARCH:\n"
            for i, result in enumerate(search_results["results"][:3]):
                search_evidence += f"Source {i+1} ({result.source}): {result.content[:400]}...\n\n"
        
        doc_info = ""
        if doc_context:
            doc_info = f"POLICY DOCUMENT CONTEXT:\n{doc_context[:400]}...\n\n"
        
        # Create a clearer, more structured prompt
        analysis_prompt = f"""TASK: Analyze the following content through the lens of costly signals (material commitments) and performance fictions (symbolic rhetoric).

{search_evidence}

RESPONSE TO ANALYZE:
"{base_response}"

{doc_info}

INSTRUCTIONS:
1. Identify ONE specific policy, regulation, investment, or commitment (this is the costly signal)
2. Identify ONE piece of rhetoric, symbolic language, or ceremonial framing (this is the performance fiction)
3. Analyze how these material and symbolic elements interact or create tension

OUTPUT REQUIREMENTS:
- You MUST output EXACTLY three lines
- Each line MUST start with the exact bracketed text shown below
- Do not add any additional text, explanations, or formatting

[COSTLY SIGNAL - POLICY_POSITION]: <your specific policy/regulation/commitment here>
[PERFORMANCE FICTION]: <your specific rhetoric/symbolic language here>
[SIGNAL-FICTION TENSION]: <your analysis of their interaction here>"""
        
        return analysis_prompt
    
    async def _generate_llm_framework_analysis(self, analysis_prompt: str) -> str:
        """
        Use LLM to analyze the response through meta-sovereignty framework
        """
        try:
            logging.info(f"Starting LLM framework analysis for {self.name}")
            
            # Simplified approach - use few-shot examples
            original_personality = self.personality
            self.personality = """You are a political theorist analyzing AI governance through Fearon's costly signals and Ezrahi's performance fictions.

EXAMPLES OF CORRECT FORMAT:
[COSTLY SIGNAL - POLICY_POSITION]: $52 billion CHIPS Act funding for semiconductor manufacturing
[PERFORMANCE FICTION]: Rhetoric of 'technological sovereignty' and 'innovation leadership'
[SIGNAL-FICTION TENSION]: Material investment contradicts free market ideology

[COSTLY SIGNAL - POLICY_POSITION]: EU AI Act regulatory framework with fines up to 7% of revenue  
[PERFORMANCE FICTION]: Language of 'human-centric AI' and 'trustworthy innovation'
[SIGNAL-FICTION TENSION]: Regulatory constraints limit proclaimed innovation leadership

You MUST follow this EXACT format. Each line starts with the bracket and colon. No other text."""
            
            # Simplified prompt focusing on examples
            simplified_prompt = f"""Analyze this content using the costly signals and performance fictions framework.

{analysis_prompt}

Output EXACTLY three lines using the format shown in my examples above. Start each line with the exact brackets."""
            
            analysis = await super().generate_response(simplified_prompt, "", None)
            self.personality = original_personality
            
            if not analysis:
                logging.info(f"LLM returned empty analysis for {self.name}, using simple citations")
                return ""
            
            # More flexible parsing - look for any theoretical content
            lines = [line.strip() for line in analysis.strip().split('\n') if line.strip()]
            
            # Check for theoretical markers (more flexible)
            theoretical_indicators = [
                '[COSTLY SIGNAL', '[PERFORMANCE FICTION', '[SIGNAL-FICTION',
                'COSTLY SIGNAL:', 'PERFORMANCE FICTION:', 'SIGNAL-FICTION:',
                'costly signal', 'performance fiction', 'signal-fiction tension'
            ]
            
            has_theoretical_content = any(
                any(indicator.lower() in line.lower() for indicator in theoretical_indicators)
                for line in lines
            )
            
            if has_theoretical_content:
                logging.info(f"LLM generated theoretical analysis for {self.name}")
                return analysis.strip()
            else:
                logging.info(f"LLM response lacks theoretical framework markers for {self.name}, using simple citations")
                return ""
            
        except Exception as e:
            logging.error(f"Error in LLM framework analysis: {str(e)}")
            return ""
    
    async def _analyze_dynamic_signal_fiction_tension(self, signal: Dict, fiction: Dict, context: str) -> str:
        """
        Generate LLM analysis of signal-fiction tension based on current context
        """
        prompt = f"""
        Analyze the tension between this costly signal and performance fiction:

        COSTLY SIGNAL: {signal.get('description', 'N/A')}
        PERFORMANCE FICTION: {fiction.get('description', 'N/A')}
        CONTEXT: {context[:200]}...

        How do the material constraints (the costly signal) and symbolic performances (the fiction) interact? 
        Do they reinforce each other, create contradictions, or reveal gaps between projection and possession?

        Provide a single sentence analysis of this signal-fiction tension, focusing on how sovereignty is performed rather than possessed.
        """

        try:
            original_personality = self.personality
            self.personality = "You are a political theorist analyzing how material commitments and symbolic performances interact in sovereignty claims."
            
            tension_analysis = await super().generate_response(prompt, "", None)
            self.personality = original_personality
            
            return tension_analysis.strip()
        except Exception as e:
            logging.error(f"Error generating tension analysis: {e}")
            return ""  # Return empty instead of hardcoded fallback
    
    
    def _format_citations(self, search_results: Optional[Dict], 
                         used_documents: List[str], 
                         signal_type: SignalType) -> str:
        """
        Create multi-format citations distinguishing hard facts from performative claims
        """
        citations = []
        
        # Format search citations based on signal type
        if search_results and search_results["results"]:
            for i, result in enumerate(search_results["results"]):
                if signal_type in [SignalType.TYING_HANDS, SignalType.SUNK_COSTS]:
                    # Hard facts format for binding commitments
                    citation = f"[{i+1}] {result.source} ({result.timestamp}): VERIFIED FACT - {result.url}"
                else:
                    # Performative claims format for flexible positions
                    citation = f"[{i+1}] {result.source} ({result.timestamp}): STRATEGIC POSITION - {result.url}"
                citations.append(citation)
        
        # Format document citations
        if used_documents:
            doc_start = len(citations) + 1
            for i, doc in enumerate(used_documents):
                citation = f"[{doc_start + i}] ESTABLISHED POLICY - {doc}"
                citations.append(citation)
        
        if not citations:
            return ""
        
        # Add framing based on signal type
        if signal_type == SignalType.TYING_HANDS:
            header = "BINDING COMMITMENTS (Verified Sources):"
        elif signal_type == SignalType.SUNK_COSTS:
            header = "IRREVERSIBLE INVESTMENTS (Material Evidence):"
        elif signal_type == SignalType.INSTALLMENT_COSTS:
            header = "ONGOING COMMITMENTS (Program Documentation):"
        else:
            header = "CURRENT POSITIONS (Subject to Strategic Revision):"
        
        return f"\n{header}\n" + "\n".join(citations)
    
    
    
    
    def _estimate_signal_cost(self, signal_type: SignalType) -> str:
        """
        Estimate the cost of a signal in real terms
        """
        cost_estimates = {
            SignalType.TYING_HANDS: "High political cost - limits future flexibility",
            SignalType.SUNK_COSTS: "Irreversible financial/infrastructure investment",
            SignalType.INSTALLMENT_COSTS: "Ongoing budgetary commitment",
            SignalType.REDUCIBLE_COSTS: "Moderate cost - can be reversed with effort"
        }
        return cost_estimates.get(signal_type, "Variable cost")
    
    def _update_round_tracking(self, debate_prompt: str):
        """Update round counters"""
        if debate_prompt:
            round_match = re.search(r"round: (\d+)", debate_prompt)
            if round_match:
                new_round = int(round_match.group(1))
                if new_round > self.current_round:
                    self.current_round = new_round
                    self.rounds_since_last_unmask += 1
    
    
    async def _generate_base_content(self, context: str, last_message: str,
                                   topic: str, search_results: Optional[Dict],
                                   doc_context: str) -> str:
        """Generate the base response content using both search and documents"""
        
        # Import the search-first configuration
        from search_first_config import create_search_first_prompt
        
        # Create a comprehensive prompt that emphasizes both sources
        comprehensive_prompt = create_search_first_prompt(
            agent_name=self.name,
            topic=topic,
            search_results=search_results,
            doc_context=doc_context,
            last_message=last_message
        )
        
        # Add the debate context
        full_prompt = f"{context}\n\n{comprehensive_prompt}"
        
        # Generate response with the comprehensive prompt
        response = await super().generate_response(full_prompt, "", None)
        
        return response
    
    async def generate_conclusion(self, context: str) -> str:
        """
        Generate a conclusion that uses both documents and search
        """
        try:
            # Extract topic for search
            topic = self._extract_topic(context)
            
            # Perform strategic search for latest information
            search_results = None
            if self.search_client:
                search_results = await perform_strategic_search(
                    self.search_client, self.name, topic,
                    "Generate final position paper", context
                )
            
            # Get document context (from parent class)
            doc_context, used_documents = self._get_comprehensive_context_with_tracking(topic)
            self.last_used_documents = used_documents
            
            # Combine search and document insights
            combined_context = ""
            
            # Add search results if available
            if search_results and search_results["results"]:
                combined_context += "\nRECENT DEVELOPMENTS (from search):\n"
                for i, result in enumerate(search_results["results"][:3]):
                    combined_context += f"- {result.content[:200]}... (Source: {result.source})\n"
            
            # Add document context
            if doc_context:
                combined_context += f"\nESTABLISHED POSITIONS (from documents):\n{doc_context}"
            
            # Skip signal/fiction generation since helper methods don't exist
            
            # Augment personality with combined context
            augmented_personality = f"{self.personality}\n\nFor your final position paper, consider:\n{combined_context}"
            
            # Temporarily set augmented personality
            original_personality = self.personality
            self.personality = augmented_personality
            
            # Generate conclusion using parent's method
            conclusion = await super(DocumentEnabledDebateAgent, self).generate_conclusion(context)
            
            # Restore original personality
            self.personality = original_personality
            
            # Add comprehensive citations
            if (search_results and search_results["results"]) or self.last_used_documents:
                citations = self._format_comprehensive_citations(search_results, self.last_used_documents)
                conclusion = f"{conclusion}\n\n{citations}"
            
            return conclusion
            
        except Exception as e:
            logging.error(f"Error in search-enabled conclusion: {str(e)}")
            # Fall back to document-only conclusion
            return await super().generate_conclusion(context)
    
    def _format_simple_citations(self, search_results: Optional[Dict]) -> str:
        """Format simple citations when framework analysis fails"""
        if not search_results or not search_results.get("results"):
            return ""
        
        citations = ["\n\nCURRENT SOURCES:"]
        for i, result in enumerate(search_results["results"][:3]):
            citations.append(f"[{i+1}] {result.source} - {result.url}")
        
        return "\n".join(citations)
    
    def _format_comprehensive_citations(self, search_results: Optional[Dict],
                                      used_documents: List[str]) -> str:
        """Format citations for both search and documents"""
        citations = ["Sources:"]
        
        # Add search citations
        if search_results and search_results["results"]:
            citations.append("\nCURRENT SOURCES:")
            for i, result in enumerate(search_results["results"][:5]):
                citations.append(f"[{i+1}] {result.source} - {result.url}")
        
        # Add document citations
        if used_documents:
            citations.append("\nPOLICY DOCUMENTS:")
            start_num = len(search_results["results"]) + 1 if search_results else 1
            for i, doc in enumerate(used_documents):
                citations.append(f"[{start_num + i}] {doc}")
        
        return "\n".join(citations) if len(citations) > 1 else ""
    
    def _strip_action_phrases(self, text: str) -> str:
        """Remove action phrases from text"""
        # Common action phrase patterns to remove
        action_patterns = [
            r'\*[^*]+\*',  # Text between asterisks
            r'^(straightens|adjusts|reviews|nods|clears|takes|glances|pauses|considers|reflects|examines|studies|reorganizes|shuffles|leans|sits|stands|walks|gestures|points|raises|lowers|turns|looks|smiles|frowns|sighs|breathes|thinks|ponders|contemplates)[\s\w]*$',  # Action verbs at start of line
        ]
        
        lines = text.split('\n')
        filtered_lines = []
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                filtered_lines.append(line)
                continue
                
            # Check if entire line is an action phrase
            skip_line = False
            stripped_line = line.strip()
            
            # Check for asterisk-wrapped actions
            if stripped_line.startswith('*') and stripped_line.endswith('*'):
                skip_line = True
            
            # Check for common action phrases without asterisks
            import re
            for pattern in action_patterns[1:]:  # Skip the asterisk pattern we already checked
                if re.match(pattern, stripped_line, re.IGNORECASE):
                    skip_line = True
                    break
            
            if not skip_line:
                # Also remove inline asterisk actions from the line
                cleaned_line = re.sub(action_patterns[0], '', line)
                if cleaned_line.strip():  # Only add if there's content left
                    filtered_lines.append(cleaned_line)
        
        return '\n'.join(filtered_lines).strip()
