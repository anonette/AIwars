"""
Enhanced Search Integration with Full Theoretical Resource Access
Integrates TEXTS/ resources with agent-specific documents for deep analysis
"""

import os
import logging
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path
import json
import hashlib
import asyncio
import re
from dataclasses import dataclass
from document_integration import DocumentEnabledDebateAgent
from document_retrieval import DocumentStore
from search_enabled_debate_agent import SearchEnabledDebateAgent

@dataclass
class TheoreticalResource:
    """Enhanced document representation for theoretical resources"""
    path: str
    title: str
    author: str
    category: str  # 'political_theory', 'ai_governance', 'strategic_analysis', etc.
    priority: int  # Higher number = higher priority for theoretical analysis
    content_preview: str
    keywords: List[str]

class EnhancedDocumentStore(DocumentStore):
    """Extended document store that includes theoretical resources from TEXTS/"""
    
    def __init__(self, base_path: str = "agent_documents", texts_path: str = "TEXTS"):
        super().__init__(base_path)
        self.texts_path = Path(texts_path)
        self.theoretical_resources: List[TheoreticalResource] = []
        self.resource_index = {}
        
        # Load theoretical resources
        self._load_theoretical_resources()
        logging.info(f"Enhanced document store initialized with {len(self.theoretical_resources)} theoretical resources")
    
    def _load_theoretical_resources(self):
        """Load and index theoretical resources from TEXTS/"""
        if not self.texts_path.exists():
            logging.warning(f"TEXTS path {self.texts_path} does not exist")
            return
        
        # Priority theoretical works
        priority_resources = {
            "Yaron Ezrahi - Imagined Democracies": {
                "author": "Yaron Ezrahi",
                "category": "political_imaginaries",
                "priority": 100,
                "keywords": ["political imaginaries", "necessary fictions", "democratic legitimacy", "transparency"]
            },
            "James Fearon - Rationalist Explanations for War": {
                "author": "James Fearon",
                "category": "costly_signaling",
                "priority": 100,
                "keywords": ["costly signals", "credible commitments", "audience costs", "sunk costs", "tying hands", "installment costs"]
            },
            "James Fearon - Signaling Foreign Policy Interests": {
                "author": "James Fearon",
                "category": "costly_signaling",
                "priority": 95,
                "keywords": ["audience costs", "domestic political costs", "reputation costs", "signaling resolve"]
            },
            "Michel Foucault - Society Must Be Defended": {
                "author": "Michel Foucault",
                "category": "power_analysis",
                "priority": 95,
                "keywords": ["power dynamics", "sovereignty", "biopolitics", "state apparatus"]
            },
            "Mark Coeckelbergh - The Political Philosophy of AI": {
                "author": "Mark Coeckelbergh",
                "category": "ai_political_theory",
                "priority": 90,
                "keywords": ["AI governance", "political philosophy", "technology politics"]
            },
            "Mathias Risse - Political Theory of the Digital Age": {
                "author": "Mathias Risse",
                "category": "digital_politics",
                "priority": 90,
                "keywords": ["digital governance", "algorithmic authority", "digital sovereignty"]
            },
            "Homi K. Bhabha - The Location of Culture": {
                "author": "Homi K. Bhabha",
                "category": "cultural_theory",
                "priority": 85,
                "keywords": ["cultural positioning", "mimicry", "hybridity", "colonial discourse"]
            }
        }
        
        # Scan TEXTS directory
        for file_path in self.texts_path.iterdir():
            if file_path.suffix.lower() in ['.pdf', '.txt', '.md', '.json']:
                resource_info = self._extract_resource_info(file_path, priority_resources)
                if resource_info:
                    self.theoretical_resources.append(resource_info)
                    # Create searchable index
                    self.resource_index[file_path.stem] = resource_info
    
    def _extract_resource_info(self, file_path: Path, priority_map: Dict) -> Optional[TheoreticalResource]:
        """Extract metadata for theoretical resources"""
        filename = file_path.name
        
        # Match against priority resources
        matched_resource = None
        for key, info in priority_map.items():
            if any(part.lower() in filename.lower() for part in key.split(" - ")):
                matched_resource = info
                break
        
        # Default classification for unmatched resources
        if not matched_resource:
            if "cset" in filename.lower() or "analysis" in filename.lower():
                matched_resource = {"author": "Unknown", "category": "strategic_analysis", "priority": 70, "keywords": ["analysis"]}
            elif any(term in filename.lower() for term in ["ai", "governance", "policy"]):
                matched_resource = {"author": "Unknown", "category": "ai_governance", "priority": 75, "keywords": ["AI governance"]}
            elif filename.endswith('.json'):
                matched_resource = {"author": "Data", "category": "structured_data", "priority": 60, "keywords": ["data"]}
            else:
                matched_resource = {"author": "Unknown", "category": "general", "priority": 50, "keywords": []}
        
        # Generate content preview (placeholder - would need actual file reading)
        preview = f"Theoretical resource: {filename}"
        
        return TheoreticalResource(
            path=str(file_path),
            title=filename,
            author=matched_resource["author"],
            category=matched_resource["category"],
            priority=matched_resource["priority"],
            content_preview=preview,
            keywords=matched_resource["keywords"]
        )
    
    def search_theoretical_resources(self, query: str, category: str = None, 
                                   max_results: int = 5) -> List[TheoreticalResource]:
        """Search theoretical resources by query and category"""
        query_lower = query.lower()
        matches = []
        
        for resource in self.theoretical_resources:
            score = 0
            
            # Category match bonus
            if category and resource.category == category:
                score += 50
            elif category:
                continue  # Skip if specific category requested but doesn't match
            
            # Title match
            if query_lower in resource.title.lower():
                score += 30
            
            # Keyword match
            for keyword in resource.keywords:
                if keyword.lower() in query_lower:
                    score += 20
            
            # Author match
            if query_lower in resource.author.lower():
                score += 15
            
            if score > 0:
                matches.append((resource, score))
        
        # Sort by score descending, then by priority
        matches.sort(key=lambda x: (x[1], x[0].priority), reverse=True)
        
        return [match[0] for match in matches[:max_results]]
    
    def get_high_priority_resources(self, category: str = None) -> List[TheoreticalResource]:
        """Get highest priority theoretical resources"""
        resources = [r for r in self.theoretical_resources if r.priority >= 80]
        if category:
            resources = [r for r in resources if r.category == category]
        
        return sorted(resources, key=lambda x: x.priority, reverse=True)

class TheoreticallyEnhancedAgent(SearchEnabledDebateAgent):
    """
    Search-enabled agent with full access to theoretical resources
    Provides deep analysis using primary sources like Ezrahi's actual work
    """
    
    def __init__(self, name: str, personality: str, agent_config_key: str,
                 config: dict = None, document_store: Optional[DocumentStore] = None,
                 search_client = None):
        """Initialize with enhanced document store"""
        
        # Use enhanced document store if none provided
        if document_store is None:
            document_store = EnhancedDocumentStore()
        
        super().__init__(name, personality, agent_config_key, config, document_store, search_client)
        
        # Track theoretical resources used
        self.last_used_theoretical_resources = []
        
        logging.info(f"Initialized theoretically enhanced agent {name} with {len(self.document_store.theoretical_resources)} theoretical resources")
    
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
    
    async def generate_response(self, context: str, last_message: str,
                              debate_prompt: str = None) -> str:
        """Generate response with theoretical resource integration"""
        try:
            # Extract topic
            topic = self._extract_topic(context)
            
            # Get theoretical resources for the topic
            theoretical_context = self._get_theoretical_context(topic, context)
            
            # Call parent's generate_response which now always uses both search and documents
            response = await super().generate_response(context, last_message, debate_prompt)
            
            # Strip action phrases from the base response
            response = self._strip_action_phrases(response)
            
            # Get search results if available from parent class
            search_results = getattr(self, '_last_search_results', None)
            
            # Enhance with theoretical analysis if we have search results or theoretical resources
            if search_results or self.last_used_theoretical_resources:
                # Generate Ezrahi analysis
                ezrahi_analysis = await self._generate_ezrahi_analysis(
                    response, theoretical_context, topic, search_results
                )
                
                # Generate Fearon costly signal analysis
                fearon_analysis = await self._generate_fearon_analysis(
                    response, search_results
                )
                
                # Generate meta-sovereignty analysis
                meta_sovereignty_analysis = await self._generate_meta_sovereignty_analysis(
                    response, ezrahi_analysis, fearon_analysis, search_results
                )
                
                # Combine all analyses
                if ezrahi_analysis:
                    response = f"{response}\n\n{ezrahi_analysis}"
                if fearon_analysis:
                    response = f"{response}\n\n{fearon_analysis}"
                if meta_sovereignty_analysis:
                    response = f"{response}\n\n{meta_sovereignty_analysis}"
                
                # Don't add citations here - parent class handles it
            
            return response
            
        except Exception as e:
            logging.error(f"Error in theoretically enhanced response: {str(e)}")
            return await super().generate_response(context, last_message, debate_prompt)
    
    def _get_theoretical_context(self, topic: str, context: str) -> str:
        """Retrieve relevant theoretical resources for the topic"""
        theoretical_context = ""
        self.last_used_theoretical_resources = []
        
        if not isinstance(self.document_store, EnhancedDocumentStore):
            return theoretical_context
        
        # Search for relevant theoretical resources
        relevant_resources = self.document_store.search_theoretical_resources(
            query=topic, max_results=3
        )
        
        # Always include high-priority political imaginaries resources
        political_resources = self.document_store.get_high_priority_resources(
            category="political_imaginaries"
        )
        
        # Combine and deduplicate
        all_resources = list({r.path: r for r in (relevant_resources + political_resources[:2])}.values())
        
        if all_resources:
            theoretical_context += "THEORETICAL FRAMEWORK RESOURCES:\n"
            for resource in all_resources[:4]:  # Limit to top 4
                theoretical_context += f"- {resource.author}: {resource.title} ({resource.category})\n"
                theoretical_context += f"  Keywords: {', '.join(resource.keywords[:3])}\n"
                self.last_used_theoretical_resources.append(resource.title)
        
        return theoretical_context
    
    async def _generate_ezrahi_analysis(self, base_response: str,
                                       theoretical_context: str, topic: str,
                                       search_results: Optional[Dict] = None) -> str:
        """Generate Ezrahi's political fiction analysis"""
        
        # Extract search results content if available
        search_content = ""
        specific_policies = []
        if search_results and search_results.get("results"):
            search_content = "\n\nSEARCH RESULTS ON AI POLICY:\n"
            search_content += "=" * 50 + "\n"
            for i, result in enumerate(search_results["results"][:5]):  # Show up to 5 results
                search_content += f"\n[{i+1}] SOURCE: {result.source}\n"
                search_content += f"    CONTENT: {result.content[:400]}...\n"
                search_content += "-" * 50 + "\n"
                
                # Extract specific policies with dollar amounts
                import re
                dollars = re.findall(r'\$[\d,]+(?:\.\d+)?\s*(?:billion|million|trillion)?', result.content)
                acts = re.findall(r'(?:CHIPS Act|AI Act|Executive Order \d+|H\.R\.\s*\d+)', result.content)
                dates = re.findall(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}|\d{4}', result.content)
                
                for dollar in dollars:
                    specific_policies.append(f"FUNDING: {dollar}")
                for act in acts:
                    specific_policies.append(f"POLICY: {act}")
                for date in dates:
                    specific_policies.append(f"DATE: {date}")
        
        # Add extracted specifics
        if specific_policies:
            search_content += "\n\nEXTRACTED SPECIFIC POLICIES:\n"
            for policy in specific_policies[:10]:  # Limit to 10
                search_content += f"• {policy}\n"
        
        ezrahi_prompt = f"""You are Yaron Ezrahi, the political theorist who wrote "Imagined Democracies: Necessary Political Fictions."

STATEMENT TO ANALYZE: "{base_response}"
{search_content}

MANDATORY REQUIREMENT: You MUST extract and analyze AT LEAST 3 specific policies/initiatives from the search results above. For EACH one:

1. NAME THE SPECIFIC POLICY: Quote the exact program name, dollar amount, or initiative as it appears in the search results (e.g., "$52 billion CHIPS Act", "EU AI Act", "National AI Initiative")

2. IDENTIFY ITS POLITICAL FICTION: What specific fiction does THIS PARTICULAR policy require? (e.g., "The CHIPS Act's $52 billion requires belief that domestic semiconductor production equals technological sovereignty")

3. EXPOSE THE CONTRADICTION: How does THIS SPECIFIC policy contradict the rhetoric? Use exact quotes and numbers from the search.

4. REVEAL THE MATERIAL REALITY: What does THIS SPECIFIC investment/regulation actually do versus what it claims?

FORBIDDEN: Generic statements like "emphasis on voluntary standards" or "fostering innovation"
REQUIRED: Specific references like "the Biden administration's Executive Order 14110 allocating $140 million to AI institutes"

Start your analysis by listing the 3+ specific policies you found in the search, then analyze each one."""
        
        try:
            # Use LLM to generate theoretical analysis as Ezrahi
            original_personality = self.personality
            self.personality = """You are Yaron Ezrahi, author of "Imagined Democracies: Necessary Political Fictions." You analyze how modern democracies create legitimacy through political imaginaries and performances. You reveal how policy statements deploy necessary fictions to make complex technical governance appear democratic and transparent. Focus on analytical content without physical actions or gestures."""
            
            # Generate with higher temperature for creative analysis
            analysis = await self._generate_creative_analysis(ezrahi_prompt)
            
            self.personality = original_personality
            
            if analysis:
                # Strip action phrases
                analysis = self._strip_action_phrases(analysis)
                logging.info(f"Ezrahi-style theoretical analysis generated for {self.name}")
                return f"[EZRAHI'S ANALYSIS OF POLITICAL FICTIONS]\n{analysis}"
            else:
                logging.warning("Ezrahi analysis returned empty")
                return ""
                
        except Exception as e:
            logging.error(f"Error generating Ezrahi analysis: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())
            return ""
    
    async def _generate_fearon_analysis(self, base_response: str,
                                       search_results: Optional[Dict] = None) -> str:
        """Generate Fearon's costly signal analysis"""
        
        # Extract search results for signal identification
        search_content = ""
        specific_signals = []
        if search_results and search_results.get("results"):
            search_content = "\n\nSEARCH RESULTS REVEALING ACTUAL POLICIES:\n"
            search_content += "=" * 50 + "\n"
            for i, result in enumerate(search_results["results"][:5]):  # Show up to 5 results
                search_content += f"\n[{i+1}] SOURCE: {result.source}\n"
                search_content += f"    CONTENT: {result.content[:400]}...\n"
                search_content += "-" * 50 + "\n"
                
                # Extract specific signals
                import re
                dollars = re.findall(r'\$[\d,]+(?:\.\d+)?\s*(?:billion|million|trillion)?', result.content)
                acts = re.findall(r'(?:CHIPS Act|AI Act|Executive Order \d+|H\.R\.\s*\d+)', result.content)
                
                for dollar in dollars:
                    specific_signals.append(f"SIGNAL: {dollar}")
                for act in acts:
                    specific_signals.append(f"POLICY: {act}")
        
        # Add extracted signals
        if specific_signals:
            search_content += "\n\nEXTRACTED COSTLY SIGNALS:\n"
            for signal in specific_signals[:10]:
                search_content += f"• {signal}\n"
        
        fearon_prompt = f"""You are James Fearon analyzing AI policy through your costly signaling framework from "Rationalist Explanations for War" (1995).

STATEMENT TO ANALYZE: "{base_response}"
{search_content}

MANDATORY TASK: Extract and analyze AT LEAST 3 specific policies from the search results above.

STEP 1 - IDENTIFY POLICIES: List the specific policies you found in the search results with their exact names and details as they appear (e.g., "CHIPS Act - $52 billion", "EU AI Act", "Executive Order 14110").

STEP 2 - ANALYZE EACH AS A COSTLY SIGNAL:

For EACH policy you identified, provide this analysis:

**[EXACT POLICY NAME AS IT APPEARS IN SEARCH]**
- SIGNAL TYPE: [sunk cost, tying hands, or audience cost]
- COST STRUCTURE:
  * Monetary: $[exact amount from search]
  * Political: [specific groups that oppose]
  * Reversibility: [what makes it hard to undo]
- SEPARATING MECHANISM: Only type θ > [threshold] sends this signal because [specific reason]
- BELIEF UPDATE: P(resolved|signal) = [X] vs prior P(resolved) = [Y]

FORBIDDEN PHRASES:
- "emphasis on voluntary standards"
- "fostering innovation"
- "commitment to ethical AI"
- Any generic statement not tied to a specific policy from the search

REQUIRED:
- Exact policy names from search results
- Specific dollar amounts
- Concrete mechanisms
- Numerical thresholds

Start by listing the 3+ policies you're analyzing from the search results."""
        
        try:
            # Use LLM to generate Fearon analysis
            original_personality = self.personality
            self.personality = """You are James Fearon, author of "Rationalist Explanations for War" (1995) and "Signaling Foreign Policy Interests" (1997). You developed the formal theory of costly signaling in international relations, showing how states can credibly communicate private information through actions that are too costly for unresolved types to mimic. You distinguish between different types of costly signals: sunk costs, tying hands, audience costs, and installment costs. Your work explains how these signals solve information asymmetry problems in international politics. Focus on analytical content without physical actions or gestures."""
            
            # Generate with higher temperature for creative analysis
            analysis = await self._generate_creative_analysis(fearon_prompt)
            
            self.personality = original_personality
            
            if analysis:
                # Strip action phrases
                analysis = self._strip_action_phrases(analysis)
                logging.info(f"Fearon-style costly signal analysis generated for {self.name}")
                return f"[FEARON'S COSTLY SIGNAL ANALYSIS]\n{analysis}"
            else:
                logging.warning("Fearon analysis returned empty")
                return ""
                
        except Exception as e:
            logging.error(f"Error generating Fearon analysis: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())
            return ""
    
    async def _generate_meta_sovereignty_analysis(self, base_response: str,
                                                 ezrahi_analysis: str,
                                                 fearon_analysis: str,
                                                 search_results: Optional[Dict] = None) -> str:
        """Generate meta-sovereignty analysis based on the thesis"""
        
        meta_sovereignty_prompt = f"""You are a political theorist analyzing AI governance through the lens of meta-sovereignty infrastructures -  technical, legal, and organizational systems that exceed national borders, fragment jurisdiction, and entangle states in global dependencies. They are neither fully material nor purely symbolic: they operate simultaneously as costly signals of capability and as imaginaries that project coherence, legitimacy, and agency.

STATEMENT: "{base_response}"

EZRAHI'S POLITICAL FICTION ANALYSIS:
{ezrahi_analysis}

FEARON'S COSTLY SIGNAL ANALYSIS:
{fearon_analysis}

MANDATORY TASK: Using the SPECIFIC POLICIES identified in the analyses above, reveal meta-sovereign strategies.

For EACH specific policy mentioned above (e.g., CHIPS Act, EU AI Act, Executive Orders), analyze:

1. INFRASTRUCTURAL IMAGINARY:
   - Policy: [exact name and amount]
   - Imaginary: What future does this $X billion investment imagine?
   - Reality: What dependencies does it actually reveal?

2. SOVEREIGNTY AS PERFORMANCE:
   - How does [specific policy] perform authority it cannot possess?
   - Example: "CHIPS Act's $52B performs semiconductor independence while depending on ASML's Dutch EUV monopoly"

3. CONCRETE ENTANGLEMENTS:
   - [Policy X] depends on [specific foreign technology/expertise]
   - [Investment Y] requires [specific international partnership]
   - [Regulation Z] cannot function without [specific global infrastructure]

4. GOVERNANCE WITHOUT POSSESSION:
   - How does [specific policy] create authority through standards/partnerships rather than control?
   - What new governance mechanism does [specific initiative] introduce?

FORBIDDEN: Generic statements about "fostering innovation" or "international cooperation"
REQUIRED: Every claim must reference a specific policy with its exact name, budget, and dependencies

Example format:
"The CHIPS Act's $52 billion reveals meta-sovereignty in action: it performs semiconductor independence through massive investment while simultaneously exposing dependence on ASML's lithography (100% Dutch monopoly), Tokyo Electron's deposition tools (Japanese), and TSMC's process knowledge (Taiwanese). The Act governs not through possession but through subsidy conditions that shape global supply chains."

Start by listing the specific policies you're analyzing from the previous sections."""
        
        try:
            # Use LLM to generate meta-sovereignty analysis
            original_personality = self.personality
            self.personality = """You are a political theorist specializing in sovereignty studies and infrastructure politics. You analyze how states perform sovereignty through technological imaginaries and costly signals in an era where control over AI systems remains fundamentally contested and entangled. Focus on analytical content without physical actions or gestures."""
            
            # Generate with higher temperature for creative analysis
            analysis = await self._generate_creative_analysis(meta_sovereignty_prompt)
            
            self.personality = original_personality
            
            if analysis:
                # Strip action phrases
                analysis = self._strip_action_phrases(analysis)
                logging.info(f"Meta-sovereignty analysis generated for {self.name}")
                return f"[META-SOVEREIGNTY ANALYSIS: SIGNALS AND IMAGINARIES]\n{analysis}"
            else:
                logging.warning("Meta-sovereignty analysis returned empty")
                return ""
                
        except Exception as e:
            logging.error(f"Error generating meta-sovereignty analysis: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())
            return ""
    
    def _format_theoretical_citations(self) -> str:
        """Format citations for theoretical resources used"""
        if not self.last_used_theoretical_resources:
            return ""
        
        citations = ["\n\nTHEORETICAL SOURCES:"]
        for i, resource in enumerate(self.last_used_theoretical_resources):
            citations.append(f"[T{i+1}] {resource}")
        
        return "\n".join(citations)
    
    def _format_search_citations(self, search_results: Optional[Dict]) -> str:
        """Format search result citations"""
        if not search_results or not search_results.get("results"):
            return ""
        
        citations = ["CURRENT SOURCES:"]
        for i, result in enumerate(search_results["results"][:5]):
            # Handle both object and dict formats
            if hasattr(result, 'source') and hasattr(result, 'url'):
                citations.append(f"[{i+1}] {result.source} - {result.url}")
            elif isinstance(result, dict):
                source = result.get('source', 'Unknown')
                url = result.get('url', '')
                citations.append(f"[{i+1}] {source} - {url}")
        
        return "\n".join(citations)
    
    async def _generate_creative_analysis(self, prompt: str) -> str:
        """Generate analysis with higher temperature for creativity"""
        try:
            import requests
            import os
            
            # Get API key from environment
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                logging.error("OPENROUTER_API_KEY not found")
                return ""
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Use the agent's model or default
            model = getattr(self, 'model', 'openai/gpt-4o')
            
            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a theoretical analyst providing creative and insightful analysis."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000,
                "temperature": 0.9  # High temperature for creative analysis
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                response_data = response.json()
                return response_data["choices"][0]["message"]["content"].strip()
            else:
                logging.error(f"API error in creative analysis: {response.status_code}, {response.text}")
                return ""
                
        except Exception as e:
            logging.error(f"Error in creative analysis generation: {str(e)}")
            return ""

def create_enhanced_agents(config: dict) -> Dict[str, TheoreticallyEnhancedAgent]:
    """Create theoretically enhanced agents for all nations"""
    
    # Initialize enhanced document store
    enhanced_store = EnhancedDocumentStore()
    
    agents = {}
    
    # Map actual config keys from config.yaml structure
    agent_configs = {
        "United States": "openai",        # matches config.yaml structure
        "People's Republic of China": "deepseek", 
        "European Union": "european_union"
    }
    
    agents_section = config.get('agents', {})
    
    for display_name, config_key in agent_configs.items():
        if config_key in agents_section:
            agent_config = agents_section[config_key]
            personality = agent_config.get('personality', f'{display_name} representative')
            
            agents[display_name] = TheoreticallyEnhancedAgent(
                name=display_name,
                personality=personality,
                agent_config_key=config_key,
                config=config,
                document_store=enhanced_store
            )
            
            logging.info(f"Created enhanced agent: {display_name} using config key: {config_key}")
        else:
            logging.warning(f"Config key {config_key} not found in agents section")
    
    return agents

# Example usage and testing
async def test_theoretical_integration():
    """Test the theoretical resource integration"""
    
    # Create enhanced document store
    store = EnhancedDocumentStore()
    
    print(f"Loaded {len(store.theoretical_resources)} theoretical resources")
    
    # Test searches
    political_resources = store.search_theoretical_resources("political imaginaries")
    print(f"Found {len(political_resources)} resources for 'political imaginaries'")
    
    ai_resources = store.search_theoretical_resources("AI governance")  
    print(f"Found {len(ai_resources)} resources for 'AI governance'")
    
    high_priority = store.get_high_priority_resources()
    print(f"High priority resources: {len(high_priority)}")
    for resource in high_priority[:3]:
        print(f"  - {resource.author}: {resource.title} (Priority: {resource.priority})")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_theoretical_integration())
