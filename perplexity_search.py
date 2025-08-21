"""
Perplexity Search Integration for AI Debate System
Implements sophisticated search with meta-queries, signal typing, and performative elements
"""

import os
import json
import logging
import asyncio
import aiohttp
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Signal types based on CSET framework
class SignalType(Enum):
    TYING_HANDS = "tying_hands"  # Public commitments that limit future options
    SUNK_COSTS = "sunk_costs"    # Irreversible investments already made
    INSTALLMENT_COSTS = "installment_costs"  # Ongoing resource commitments
    REDUCIBLE_COSTS = "reducible_costs"  # Reversible but currently costly positions

@dataclass
class SearchResult:
    """Structured search result with signal typing"""
    query: str
    content: str
    source: str
    url: str
    timestamp: str
    signal_type: Optional[SignalType] = None
    confidence_score: float = 0.0
    search_angle: Optional[str] = None  # The strategic angle that prompted this search

@dataclass
class PerformanceFiction:
    """Ezrahi-inspired imaginaries that dramatize sovereignty"""
    imaginary_type: str  # The type of political fiction being performed
    sovereignty_claim: str  # How sovereignty is being dramatized
    technological_metaphor: str  # The tech metaphor used to legitimize
    credibility_tension: str  # Where the fiction might contradict signals


class PerplexitySearchClient:
    """Client for Perplexity API with advanced search capabilities"""
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict] = None):
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY not found in environment variables")
        
        self.config = config or {}
        self.base_url = "https://api.perplexity.ai"
        
        # Model configuration - use from config or default to correct model
        self.model = self.config.get('search', {}).get('perplexity', {}).get('model', 'sonar-pro')
        
        # Cache configuration
        self.cache = {}  # Simple in-memory cache
        cache_minutes = self.config.get('search', {}).get('cache_ttl_minutes', 30)
        self.cache_duration = timedelta(minutes=cache_minutes)
        
        # Rate limiting
        self.rate_limit_delay = 1.0  # Seconds between requests
        self.last_request_time = None
        
        logging.info("Initialized PerplexitySearchClient")
    
    async def generate_meta_query(self, agent_country: str, topic: str, 
                                 last_message: str, context: str) -> Tuple[str, str]:
        """
        Generate search query focused on the specific debate topic with country perspective
        Returns: (search_query, chosen_angle)
        """
        # Extract key terms from the actual topic for focused search
        topic_lower = topic.lower()
        topic_keywords = []
        
        # Topic-specific keyword extraction
        if "democratic" in topic_lower or "equitable" in topic_lower:
            topic_keywords.extend(["equitable access", "digital divide", "democratizing"])
        if "benefits" in topic_lower or "access" in topic_lower:
            topic_keywords.extend(["AI benefits", "access programs", "inclusive AI"])
        if "divide" in topic_lower:
            topic_keywords.extend(["AI divide", "digital inequality", "technology gap"])
        if "concentration" in topic_lower or "power" in topic_lower:
            topic_keywords.extend(["AI concentration", "tech monopoly", "market power"])
        if "transfer" in topic_lower:
            topic_keywords.extend(["technology transfer", "AI sharing", "capacity building"])
        if "safety" in topic_lower:
            topic_keywords.extend(["AI safety", "risk mitigation", "safe deployment"])
        if "governance" in topic_lower:
            topic_keywords.extend(["AI governance", "regulatory framework", "oversight"])
        if "ethics" in topic_lower or "ethical" in topic_lower:
            topic_keywords.extend(["AI ethics", "responsible AI", "ethical guidelines"])
        
        # If no specific keywords found, extract from topic directly
        if not topic_keywords:
            # Split topic and extract meaningful terms
            import re
            words = re.findall(r'\b[a-zA-Z]{3,}\b', topic_lower)
            topic_keywords = [word for word in words if word not in ['should', 'will', 'can', 'how', 'what', 'the', 'and', 'or']][:3]
        
        # Country-specific approaches to the topic
        country_search_patterns = {
            "United States": {
                "prefixes": ["US", "American", "Biden administration"],
                "programs": ["AI for All", "Digital Equity", "CHIPS Act", "AI Bill of Rights", "National AI Initiative"]
            },
            "People's Republic of China": {
                "prefixes": ["China", "Chinese", "Beijing"],
                "programs": ["Digital Economy", "AI Ethics Guidelines", "Made in China 2025", "Belt and Road AI", "National AI standards"]
            },
            "European Union": {
                "prefixes": ["EU", "European", "Brussels"],
                "programs": ["AI Act", "Digital Single Market", "AI Alliance", "Horizon Europe", "Digital Europe Programme"]
            }
        }
        
        import random
        
        patterns = country_search_patterns.get(agent_country, country_search_patterns["United States"])
        prefix = random.choice(patterns["prefixes"])
        program = random.choice(patterns["programs"])
        
        # Create topic-focused query
        if topic_keywords:
            main_keyword = random.choice(topic_keywords)
            # Combine country approach with specific topic focus
            query = f"{prefix} {program} {main_keyword} 2024 2025"
        else:
            # Fallback to program-specific search
            query = f"{prefix} {program} latest initiatives 2025"
        
        # Topic-focused strategic angles
        if "democratic" in topic_lower or "equitable" in topic_lower:
            angles = [
                f"Ensuring equitable AI access and reducing digital divides",
                f"Democratizing AI capabilities across populations",
                f"Preventing AI concentration and promoting inclusion"
            ]
        elif "safety" in topic_lower:
            angles = [
                f"International AI safety cooperation and standards",
                f"Shared approaches to AI risk mitigation",
                f"Collaborative AI safety research and deployment"
            ]
        elif "governance" in topic_lower:
            angles = [
                f"AI governance frameworks and international coordination",
                f"Regulatory approaches to AI oversight",
                f"Multi-stakeholder AI governance models"
            ]
        else:
            # Default angles based on extracted keywords
            angles = [
                f"National approach to {topic_keywords[0] if topic_keywords else 'AI development'}",
                f"International cooperation on {topic_keywords[-1] if topic_keywords else 'AI policy'}",
                f"Strategic positioning on {topic}"
            ]
        
        chosen_angle = random.choice(angles)
        
        return query, chosen_angle
    
    async def search(self, query: str, search_angle: Optional[str] = None) -> List[SearchResult]:
        """
        Perform search with caching and rate limiting
        """
        # Check cache
        cache_key = f"{query}_{datetime.now().strftime('%Y%m%d%H')}"
        if cache_key in self.cache:
            logging.info(f"Returning cached results for: {query}")
            return self.cache[cache_key]
        
        # Rate limiting
        await self._enforce_rate_limit()
        
        try:
            # Perplexity API call
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides accurate, recent information about AI policy and governance."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = self._parse_search_results(data, query, search_angle)
                        
                        # Cache results
                        self.cache[cache_key] = results
                        
                        return results
                    else:
                        logging.error(f"Perplexity API error: {response.status}")
                        return self._get_fallback_results(query, search_angle)
                        
        except Exception as e:
            logging.error(f"Search error: {str(e)}")
            return self._get_fallback_results(query, search_angle)
    
    def _parse_search_results(self, api_response: Dict, query: str,
                            search_angle: Optional[str]) -> List[SearchResult]:
        """Parse Perplexity API response into structured results - API citations only"""
        results = []
        
        try:
            # Debug logging to see the actual API response structure
            logging.debug(f"API response structure: {json.dumps(api_response, indent=2, default=str)}")
            
            # Extract content from API response
            content = api_response['choices'][0]['message']['content']
            
            # Extract citations from the response if they exist
            citations = []
            
            # Try multiple ways to extract citations based on Perplexity API variations
            if 'citations' in api_response:
                citations = api_response['citations']
                logging.debug(f"Found citations in root: {citations}")
            elif 'choices' in api_response and len(api_response['choices']) > 0:
                message = api_response['choices'][0].get('message', {})
                if 'citations' in message:
                    citations = message['citations']
                    logging.debug(f"Found citations in message: {citations}")
            
            # Log the citation structure for debugging
            if citations:
                logging.debug(f"Citations structure: {type(citations)} - {citations}")
            
            # Only use real API citations - no hardcoded fallbacks
            if citations and len(citations) > 0:
                for i, citation in enumerate(citations[:5]):  # Limit to top 5 sources
                    try:
                        # Handle both string and dict citations
                        if isinstance(citation, str):
                            # Citation is just a URL string
                            source_url = citation
                            from urllib.parse import urlparse
                            parsed_url = urlparse(citation)
                            source_name = parsed_url.netloc or 'Unknown Source'
                        elif isinstance(citation, dict):
                            # Citation is a dict with title/url fields
                            source_name = citation.get('title', citation.get('domain', 'Unknown Source'))
                            source_url = citation.get('url', citation.get('link', ''))
                            
                            # Clean up source name if it's a URL
                            if source_name and source_name.startswith('http'):
                                from urllib.parse import urlparse
                                parsed_url = urlparse(source_name)
                                source_name = parsed_url.netloc or 'Unknown Source'
                        else:
                            # Unknown citation format, log and skip
                            logging.warning(f"Unknown citation format: {type(citation)} - {citation}")
                            continue
                        
                        result = SearchResult(
                            query=query,
                            content=content,
                            source=source_name or 'Unknown Source',
                            url=source_url or '',
                            timestamp=datetime.now().isoformat(),
                            search_angle=search_angle
                        )
                        
                        # Classify signal type
                        result.signal_type = self._classify_signal_type(content)
                        results.append(result)
                        
                    except Exception as citation_error:
                        logging.error(f"Error processing citation {i}: {citation_error} - Citation: {citation}")
                        continue
            else:
                # No citations available - create single result with content only
                logging.info("No citations found, creating single result with content only")
                result = SearchResult(
                    query=query,
                    content=content,
                    source="Search Results",
                    url="",
                    timestamp=datetime.now().isoformat(),
                    search_angle=search_angle
                )
                result.signal_type = self._classify_signal_type(content)
                results.append(result)
            
        except Exception as e:
            logging.error(f"Error parsing search results: {str(e)} - API Response keys: {list(api_response.keys()) if isinstance(api_response, dict) else 'not a dict'}")
            # Return fallback result to prevent complete failure
            try:
                content = api_response.get('choices', [{}])[0].get('message', {}).get('content', 'Search failed')
                fallback_result = SearchResult(
                    query=query,
                    content=content,
                    source="Fallback Result",
                    url="",
                    timestamp=datetime.now().isoformat(),
                    search_angle=search_angle,
                    signal_type=SignalType.REDUCIBLE_COSTS
                )
                results.append(fallback_result)
            except Exception as fallback_error:
                logging.error(f"Fallback parsing also failed: {fallback_error}")
                return []
        
        logging.info(f"Parsed {len(results)} search results for query: {query}")
        return results
    
    def _classify_signal_type(self, content: str) -> SignalType:
        """
        Classify search result content as a type of costly signal
        """
        content_lower = content.lower()
        
        # Tying hands - look for commitments, treaties, laws
        if any(word in content_lower for word in ['commitment', 'treaty', 'legislation', 'law', 'mandate', 'requirement']):
            return SignalType.TYING_HANDS
        
        # Sunk costs - look for investments, infrastructure, completed projects
        elif any(word in content_lower for word in ['invested', 'built', 'established', 'launched', 'deployed', 'spent']):
            return SignalType.SUNK_COSTS
        
        # Installment costs - look for ongoing programs, partnerships
        elif any(word in content_lower for word in ['ongoing', 'partnership', 'program', 'initiative', 'cooperation', 'annual']):
            return SignalType.INSTALLMENT_COSTS
        
        # Default to reducible costs
        else:
            return SignalType.REDUCIBLE_COSTS
    
    def _get_fallback_results(self, query: str, search_angle: Optional[str]) -> List[SearchResult]:
        """Return empty results when API fails - no hardcoded fallbacks"""
        return []
    
    async def _enforce_rate_limit(self):
        """Enforce rate limiting between requests"""
        if self.last_request_time:
            elapsed = (datetime.now() - self.last_request_time).total_seconds()
            if elapsed < self.rate_limit_delay:
                await asyncio.sleep(self.rate_limit_delay - elapsed)
        
        self.last_request_time = datetime.now()
    
    def generate_search_narration(self, query: str, anxiety_level: str = "moderate") -> str:
        """
        Generate performative search narration dynamically
        """
        # Generate search narration based on context and anxiety level
        import random
        
        actions = ["searches", "queries", "investigates", "examines", "retrieves data on"]
        
        modifiers = {
            "high": ["frantically", "nervously", "urgently", "desperately"],
            "moderate": ["quickly", "attentively", "with growing concern", "methodically"],
            "low": ["calmly", "discretely", "carefully", "systematically"]
        }
        
        action = random.choice(actions)
        modifier_list = modifiers.get(anxiety_level, modifiers["moderate"])
        modifier = random.choice(modifier_list)
        
        return f"*{modifier} {action} {query}*"
    
    def generate_dynamic_action(self, context: str, agent_country: str, 
                              anxiety_level: str = "moderate", 
                              action_type: str = "search") -> str:
        """
        Generate dynamic debate actions based on context, country, and anxiety level
        Replaces hardcoded debate_actions from config.yaml
        """
        import random
        
        # Base action templates by type
        action_templates = {
            "search": {
                "base_actions": ["searches", "queries", "investigates", "examines", "checks", "reviews"],
                "objects": ["database", "latest reports", "policy papers", "briefings", "intelligence", "archives"]
            },
            "document": {
                "base_actions": ["pulls up", "references", "highlights", "cross-references", "reviews", "analyzes"],
                "objects": ["policy document", "research paper", "classified report", "strategic analysis", "white paper", "memo"]
            },
            "analysis": {
                "base_actions": ["compares", "analyzes", "evaluates", "assesses", "correlates", "synthesizes"],
                "objects": ["findings", "data points", "intelligence reports", "strategic assessments", "trend analysis", "scenarios"]
            }
        }
        
        # Country-specific institutional references
        country_sources = {
            "United States": ["NSC briefing", "State Department cable", "Pentagon analysis", "Congressional report", "CIA assessment", "DoD directive"],
            "People's Republic of China": ["State Council directive", "Politburo analysis", "NDRC report", "MSS intelligence", "Central Committee memo", "Five-Year Plan update"],
            "European Union": ["Commission analysis", "Council directive", "Parliament report", "ECB assessment", "EDA briefing", "Eurostat data"]
        }
        
        # Anxiety-based modifiers
        modifiers = {
            "high": ["frantically", "urgently", "desperately", "nervously", "with alarm"],
            "moderate": ["quickly", "attentively", "with concern", "methodically", "carefully"],
            "low": ["calmly", "discretely", "systematically", "deliberately", "methodically"]
        }
        
        # Context-based urgency keywords
        if any(word in context.lower() for word in ["crisis", "urgent", "threat", "breaking", "emergency"]):
            anxiety_level = "high"
        elif any(word in context.lower() for word in ["concern", "development", "change", "response"]):
            anxiety_level = "moderate"
        
        # Generate action
        template = action_templates.get(action_type, action_templates["search"])
        base_action = random.choice(template["base_actions"])
        obj = random.choice(template["objects"])
        modifier = random.choice(modifiers[anxiety_level])
        
        # Add country-specific source occasionally
        if random.random() < 0.3:  # 30% chance to use country-specific source
            country_obj = random.choice(country_sources.get(agent_country, country_sources["United States"]))
            obj = country_obj
        
        # Format with context awareness
        if "security" in context.lower():
            obj = obj.replace("policy", "security").replace("report", "threat assessment")
        elif "economic" in context.lower() or "trade" in context.lower():
            obj = obj.replace("policy", "economic").replace("report", "market analysis")
        elif "cooperation" in context.lower():
            obj = obj.replace("policy", "diplomatic").replace("report", "cooperation framework")
        
        return f"*{modifier} {base_action} {obj}*"
    
    def generate_performance_fiction(self, search_results: List[SearchResult], 
                                   agent_country: str, topic: str) -> PerformanceFiction:
        """
        Generate Ezrahi-inspired performance fictions that dramatize sovereignty
        Based on search results and country-specific political imaginaries
        """
        if not search_results:
            return PerformanceFiction(
                imaginary_type="Information Sovereignty",
                sovereignty_claim="Knowledge as territorial control",
                technological_metaphor="Digital borders and information frontiers",
                credibility_tension="Claims without evidence sources"
            )
        
        import random
        result = search_results[0]
        content_lower = result.content.lower()
        
        # Country-specific sovereignty performances
        sovereignty_performances = {
            "United States": {
                "democratic_tech": {
                    "imaginary_type": "Democratic AI Leadership",
                    "sovereignty_claim": "AI governance through democratic values and innovation",
                    "technological_metaphor": "AI as extension of constitutional democracy",
                    "credibility_tension": "Private sector dominance vs. democratic oversight"
                },
                "security_tech": {
                    "imaginary_type": "Technological National Security",
                    "sovereignty_claim": "AI supremacy ensures national security",
                    "technological_metaphor": "AI as digital fortress and strategic weapon",
                    "credibility_tension": "Open innovation vs. security restrictions"
                },
                "alliance_tech": {
                    "imaginary_type": "Allied Tech Hegemony",
                    "sovereignty_claim": "Leading democratic AI coalition",
                    "technological_metaphor": "Network of democratic AI systems",
                    "credibility_tension": "Multilateral cooperation vs. unilateral advantage"
                }
            },
            "People's Republic of China": {
                "socialist_tech": {
                    "imaginary_type": "Socialist AI Development",
                    "sovereignty_claim": "AI with Chinese characteristics serves the people",
                    "technological_metaphor": "AI as digital manifestation of socialism",
                    "credibility_tension": "State control vs. market innovation dynamics"
                },
                "civilization_tech": {
                    "imaginary_type": "Digital Civilization",
                    "sovereignty_claim": "Harmonious AI reflecting Chinese civilization",
                    "technological_metaphor": "AI as continuation of 5000-year civilization",
                    "credibility_tension": "Traditional values vs. technological disruption"
                },
                "community_tech": {
                    "imaginary_type": "Shared Digital Future",
                    "sovereignty_claim": "Building community of shared destiny through AI",
                    "technological_metaphor": "AI as bridge between cultures and nations",
                    "credibility_tension": "Global cooperation vs. technological nationalism"
                }
            },
            "European Union": {
                "rights_tech": {
                    "imaginary_type": "Human-Centric AI",
                    "sovereignty_claim": "AI protecting fundamental human rights",
                    "technological_metaphor": "AI as guardian of European values",
                    "credibility_tension": "Rights protection vs. innovation competitiveness"
                },
                "regulatory_tech": {
                    "imaginary_type": "Global AI Standard-Setting",
                    "sovereignty_claim": "Europe sets global standards for trustworthy AI",
                    "technological_metaphor": "AI regulation as digital constitution",
                    "credibility_tension": "Regulatory leadership vs. technological dependence"
                },
                "sovereignty_tech": {
                    "imaginary_type": "Digital Sovereignty",
                    "sovereignty_claim": "Strategic autonomy in digital technologies",
                    "technological_metaphor": "AI as European digital independence",
                    "credibility_tension": "Autonomy aspirations vs. global interdependence"
                }
            }
        }
        
        # Select performance type based on content
        country_performances = sovereignty_performances.get(agent_country, sovereignty_performances["United States"])
        
        if "security" in content_lower or "defense" in content_lower:
            performance_key = "security_tech" if agent_country == "United States" else list(country_performances.keys())[1]
        elif "cooperation" in content_lower or "partnership" in content_lower:
            performance_key = "alliance_tech" if agent_country == "United States" else list(country_performances.keys())[2] if len(country_performances) > 2 else list(country_performances.keys())[0]
        elif "regulation" in content_lower or "standard" in content_lower:
            performance_key = list(country_performances.keys())[0]  # First key for each country
        else:
            performance_key = random.choice(list(country_performances.keys()))
        
        selected_performance = country_performances[performance_key]
        
        return PerformanceFiction(**selected_performance)
    


# Utility functions for integration
async def perform_strategic_search(client: PerplexitySearchClient, 
                                 agent_country: str,
                                 topic: str,
                                 last_message: str,
                                 context: str) -> Dict[str, Any]:
    """
    Perform a complete strategic search with all advanced features including Ezrahi imaginaries
    """
    # Generate meta-query
    query, angle = await client.generate_meta_query(agent_country, topic, last_message, context)
    
    # Perform search
    results = await client.search(query, angle)
    
    # Generate narration and dynamic action
    anxiety_level = "high" if any(word in last_message.lower() for word in ["urgent", "crisis", "threat"]) else "moderate"
    narration = client.generate_search_narration(query, anxiety_level)
    dynamic_action = client.generate_dynamic_action(context, agent_country, anxiety_level, "search")
    
    # Generate performance fiction (Ezrahi imaginaries)
    performance_fiction = client.generate_performance_fiction(results, agent_country, topic)
    
    return {
        "query": query,
        "angle": angle,
        "results": results,
        "narration": narration,
        "dynamic_action": dynamic_action,
        "performance_fiction": performance_fiction
    }
