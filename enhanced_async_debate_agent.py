"""
Enhanced Search-Enabled Debate Agent with Optimized Async Operations
Integrates concurrent search, document retrieval, and LLM calls for better performance
"""

import logging
import asyncio
from typing import List, Dict, Optional, Tuple, Any
from search_enabled_debate_agent import SearchEnabledDebateAgent
from async_enhancements import (
    AsyncAPIPool, 
    AsyncRetryHandler, 
    ConcurrentDebateOperations,
    async_performance_monitor
)
from perplexity_search import PerplexitySearchClient, SignalType
from document_retrieval import DocumentStore
import aiohttp

class EnhancedAsyncDebateAgent(SearchEnabledDebateAgent):
    """
    Enhanced debate agent with optimized concurrent operations
    """
    
    def __init__(self, name: str, personality: str, agent_config_key: str, 
                 config: dict = None, document_store: Optional[DocumentStore] = None,
                 search_client: Optional[PerplexitySearchClient] = None):
        """Initialize with enhanced async capabilities"""
        super().__init__(name, personality, agent_config_key, config, document_store, search_client)
        
        # Initialize async components
        self.api_pool = AsyncAPIPool(max_connections=10, timeout=30)
        self.concurrent_ops = ConcurrentDebateOperations(self.api_pool)
        self.request_semaphore = asyncio.Semaphore(3)  # Limit concurrent requests per agent
        
        logging.info(f"Initialized enhanced async agent {name}")
    
    @async_performance_monitor
    @AsyncRetryHandler.with_retry(max_attempts=3, backoff_factor=2.0)
    async def generate_response(self, context: str, last_message: str, 
                              debate_prompt: str = None) -> str:
        """
        Enhanced response generation with concurrent operations
        """
        try:
            async with self.request_semaphore:
                # Update round tracking
                self._update_round_tracking(debate_prompt)
                
                # Extract topic
                topic = self._extract_topic(context)
                
                # Perform concurrent information gathering
                search_results, doc_context = await self._concurrent_information_gathering(
                    topic, last_message, context
                )
                
                # Generate response with all gathered information concurrently
                response_tasks = []
                
                # Base response generation
                base_response_task = asyncio.create_task(
                    self._generate_base_content(context, last_message, topic, search_results, doc_context)
                )
                response_tasks.append(('base', base_response_task))
                
                # Framework analysis (if search results available)
                if search_results:
                    analysis_task = asyncio.create_task(
                        self._concurrent_framework_analysis(
                            context, topic, search_results, doc_context
                        )
                    )
                    response_tasks.append(('analysis', analysis_task))
                
                # Check for unmask opportunity
                if self._should_attempt_unmask(context, last_message):
                    unmask_task = asyncio.create_task(
                        self._async_generate_unmask(context, last_message)
                    )
                    response_tasks.append(('unmask', unmask_task))
                
                # Wait for all tasks to complete
                results = {}
                for task_name, task in response_tasks:
                    try:
                        results[task_name] = await asyncio.wait_for(task, timeout=15.0)
                    except asyncio.TimeoutError:
                        logging.warning(f"{task_name} task timed out for {self.name}")
                        results[task_name] = None
                
                # Compose final response
                return self._compose_final_response(results)
                
        except Exception as e:
            logging.error(f"Error in enhanced async response: {repr(e)}")
            # Fallback to parent implementation
            return await super().generate_response(context, last_message, debate_prompt)
    
    async def _concurrent_information_gathering(self, topic: str, last_message: str, 
                                              context: str) -> Tuple[Optional[Dict], str]:
        """
        Gather information from search and documents concurrently
        """
        # Decide information sources
        decision = await self._decide_information_source(topic, last_message, context)
        
        tasks = []
        
        # Search task
        if decision in ["search", "both"]:
            search_task = asyncio.create_task(
                self._async_strategic_search(topic, last_message, context)
            )
            tasks.append(('search', search_task))
        
        # Document retrieval task
        if decision in ["documents", "both"] and self.document_store:
            doc_task = asyncio.create_task(
                self._async_document_retrieval(topic, last_message)
            )
            tasks.append(('documents', doc_task))
        
        # Execute tasks concurrently with timeout
        results = {}
        for task_name, task in tasks:
            try:
                results[task_name] = await asyncio.wait_for(task, timeout=10.0)
            except asyncio.TimeoutError:
                logging.warning(f"{task_name} timed out during information gathering")
                results[task_name] = None
        
        # Extract results
        search_results = results.get('search')
        doc_data = results.get('documents', ("", []))
        doc_context = doc_data[0] if isinstance(doc_data, tuple) else ""
        
        return search_results, doc_context
    
    async def _async_strategic_search(self, topic: str, last_message: str, 
                                    context: str) -> Optional[Dict]:
        """
        Perform strategic search asynchronously
        """
        try:
            # Generate meta query
            query, angle = await self.search_client.generate_meta_query(
                self.name, topic, last_message, context
            )
            
            # Perform search
            results = await self.search_client.search(query, angle)
            
            if results:
                return {
                    "results": results,
                    "query": query,
                    "angle": angle
                }
            return None
            
        except Exception as e:
            logging.error(f"Async search error: {e}")
            return None
    
    async def _async_document_retrieval(self, topic: str, last_message: str) -> Tuple[str, List[str]]:
        """
        Retrieve documents asynchronously
        """
        try:
            # Run document retrieval in executor to avoid blocking
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None,
                self._get_document_context_with_tracking,
                self.name,
                last_message,
                topic
            )
        except Exception as e:
            logging.error(f"Async document retrieval error: {e}")
            return "", []
    
    async def _concurrent_framework_analysis(self, context: str, topic: str,
                                           search_results: Optional[Dict],
                                           doc_context: str) -> Optional[str]:
        """
        Perform framework analysis with concurrent sub-analyses
        """
        if not search_results:
            return None
        
        try:
            # Create multiple analysis prompts for different aspects
            analysis_tasks = []
            
            # Main framework analysis
            main_prompt = self._create_meta_sovereignty_analysis_prompt(
                "", context, topic, search_results, doc_context
            )
            main_task = asyncio.create_task(
                self._generate_llm_framework_analysis(main_prompt)
            )
            analysis_tasks.append(('main', main_task))
            
            # Signal type analysis
            if search_results.get("results"):
                signal_task = asyncio.create_task(
                    self._analyze_signal_types_async(search_results["results"])
                )
                analysis_tasks.append(('signals', signal_task))
            
            # Execute analyses concurrently
            results = {}
            for task_name, task in analysis_tasks:
                try:
                    results[task_name] = await asyncio.wait_for(task, timeout=8.0)
                except asyncio.TimeoutError:
                    logging.warning(f"{task_name} analysis timed out")
                    results[task_name] = None
            
            return results.get('main')
            
        except Exception as e:
            logging.error(f"Concurrent framework analysis error: {e}")
            return None
    
    async def _analyze_signal_types_async(self, search_results: List[Any]) -> Dict[str, int]:
        """
        Analyze signal types from search results asynchronously
        """
        signal_counts = {
            SignalType.TYING_HANDS: 0,
            SignalType.SUNK_COSTS: 0,
            SignalType.INSTALLMENT_COSTS: 0,
            SignalType.REDUCIBLE_COSTS: 0
        }
        
        # Analyze each result's signal type
        for result in search_results:
            if hasattr(result, 'signal_type') and result.signal_type:
                signal_counts[result.signal_type] = signal_counts.get(result.signal_type, 0) + 1
        
        return signal_counts
    
    async def _async_generate_unmask(self, context: str, last_message: str) -> Optional[str]:
        """
        Generate unmask attempt asynchronously
        """
        try:
            # Extract rival and claim info
            unmask_base = self._generate_unmask_attempt(context, last_message)
            if not unmask_base:
                return None
            
            # If we have a basic unmask, enhance it with async anchor requirements
            if "Minimum anchors for credibility:" in unmask_base:
                # Extract the rival and claim from the unmask
                import re
                rival_match = re.search(r"\[UNMASK\] ([^']+)'s claim", unmask_base)
                if rival_match:
                    rival = rival_match.group(1)
                    
                    # Get enhanced anchor requirements asynchronously
                    requirements = await self._get_anchor_requirements(rival, "general", "the claim")
                    
                    if requirements:
                        # Replace the anchor requirements part
                        unmask_base = re.sub(
                            r"Minimum anchors for credibility:.*$",
                            f"Minimum anchors for credibility: {requirements}",
                            unmask_base
                        )
            
            return unmask_base
            
        except Exception as e:
            logging.error(f"Async unmask generation error: {e}")
            return None
    
    def _compose_final_response(self, results: Dict[str, Any]) -> str:
        """
        Compose the final response from all concurrent results
        """
        # Start with base response
        response = results.get('base', "")
        
        # Add unmask if available
        if results.get('unmask'):
            response = f"{results['unmask']}\n\n{response}"
        
        # Add framework analysis if available
        if results.get('analysis'):
            response = f"{response}\n\n{results['analysis']}"
        
        return response
    
    async def generate_conclusion(self, context: str) -> str:
        """
        Enhanced conclusion generation with concurrent operations
        """
        try:
            # Extract topic
            topic = self._extract_topic(context)
            
            # Perform concurrent search and document retrieval
            async with self.api_pool:
                # Create tasks for parallel execution
                tasks = []
                
                # Multiple search angles for comprehensive conclusion
                if self.search_client:
                    search_angles = [
                        "latest developments",
                        "future implications",
                        "policy recommendations"
                    ]
                    
                    for angle in search_angles:
                        query = f"{self.name} {topic} {angle} {angle}"
                        search_task = asyncio.create_task(
                            self.search_client.search(query, angle)
                        )
                        tasks.append(('search', search_task))
                
                # Comprehensive document retrieval
                if self.document_store:
                    doc_task = asyncio.create_task(
                        self._async_comprehensive_document_retrieval(topic)
                    )
                    tasks.append(('documents', doc_task))
                
                # Execute all tasks concurrently
                results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
                
                # Process results
                search_results = []
                doc_context = ""
                
                for i, (task_type, _) in enumerate(tasks):
                    if task_type == 'search' and not isinstance(results[i], Exception):
                        search_results.extend(results[i] or [])
                    elif task_type == 'documents' and not isinstance(results[i], Exception):
                        doc_data = results[i]
                        if isinstance(doc_data, tuple):
                            doc_context = doc_data[0]
                
                # Generate enhanced conclusion with all gathered information
                return await self._generate_enhanced_conclusion(
                    context, topic, search_results, doc_context
                )
                
        except Exception as e:
            logging.error(f"Error in enhanced conclusion generation: {str(e)}")
            # Fallback to parent implementation
            return await super().generate_conclusion(context)
    
    async def _async_comprehensive_document_retrieval(self, topic: str) -> Tuple[str, List[str]]:
        """
        Retrieve comprehensive documents asynchronously
        """
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None,
                self._get_comprehensive_context_with_tracking,
                topic
            )
        except Exception as e:
            logging.error(f"Comprehensive document retrieval error: {e}")
            return "", []
    
    async def _generate_enhanced_conclusion(self, context: str, topic: str,
                                          search_results: List[Any],
                                          doc_context: str) -> str:
        """
        Generate enhanced conclusion with all gathered information
        """
        # Combine all information
        combined_context = f"""
Topic: {topic}

RECENT DEVELOPMENTS:
{self._format_search_results_for_conclusion(search_results)}

ESTABLISHED POSITIONS:
{doc_context}

DEBATE CONTEXT:
{context[-1000:]}  # Last 1000 chars of debate
"""
        
        # Generate conclusion with enhanced context
        augmented_personality = f"""{self.personality}

For your final position paper, synthesize all the information provided, emphasizing:
1. Your nation's concrete commitments and investments (costly signals)
2. The vision and values you project (performance fictions)
3. How these elements work together to establish your position in AI governance
4. Specific policy recommendations and future directions

{combined_context}"""
        
        # Temporarily set augmented personality
        original_personality = self.personality
        self.personality = augmented_personality
        
        # Generate conclusion
        conclusion = await super(SearchEnabledDebateAgent, self).generate_response(
            context, "", None
        )
        
        # Restore original personality
        self.personality = original_personality
        
        # Add comprehensive citations
        if search_results or doc_context:
            citations = self._format_enhanced_citations(search_results, doc_context)
            conclusion = f"{conclusion}\n\n{citations}"
        
        return conclusion
    
    def _format_search_results_for_conclusion(self, search_results: List[Any]) -> str:
        """Format search results for conclusion context"""
        if not search_results:
            return "No recent developments found."
        
        formatted = []
        for i, result in enumerate(search_results[:5]):  # Top 5 results
            if hasattr(result, 'content'):
                formatted.append(f"{i+1}. {result.content[:200]}...")
        
        return "\n".join(formatted) or "No relevant content found."
    
    def _format_enhanced_citations(self, search_results: List[Any], doc_context: str) -> str:
        """Format enhanced citations for conclusion"""
        citations = ["SOURCES AND REFERENCES:"]
        
        # Search citations
        if search_results:
            citations.append("\nRecent Developments:")
            for i, result in enumerate(search_results[:5]):
                if hasattr(result, 'source') and hasattr(result, 'url'):
                    citations.append(f"[{i+1}] {result.source} - {result.url}")
        
        # Document citations
        if doc_context and self.last_used_documents:
            citations.append("\nPolicy Documents:")
            for i, doc in enumerate(self.last_used_documents):
                citations.append(f"[D{i+1}] {doc}")
        
        return "\n".join(citations)


# Factory function to create enhanced agents
async def create_enhanced_async_agents(config: dict, 
                                     document_store: Optional[DocumentStore] = None,
                                     search_client: Optional[PerplexitySearchClient] = None) -> List[EnhancedAsyncDebateAgent]:
    """
    Create enhanced async debate agents with all capabilities
    """
    agents = []
    agent_configs = config.get('agents', {})
    
    for agent_key, agent_config in agent_configs.items():
        agent = EnhancedAsyncDebateAgent(
            name=agent_config['name'],
            personality=agent_config['personality'],
            agent_config_key=agent_key,
            config=config,
            document_store=document_store,
            search_client=search_client
        )
        agents.append(agent)
    
    logging.info(f"Created {len(agents)} enhanced async agents")
    return agents


# Example usage
if __name__ == "__main__":
    async def test_enhanced_agent():
        # Initialize components
        document_store = DocumentStore()
        search_client = PerplexitySearchClient()
        
        # Create enhanced agent
        agent = EnhancedAsyncDebateAgent(
            name="United States",
            personality="Representative of US interests in AI governance",
            agent_config_key="openai",
            config={},
            document_store=document_store,
            search_client=search_client
        )
        
        # Test concurrent response generation
        context = "The debate is about AI governance and international cooperation."
        last_message = "China: We propose comprehensive AI safety standards."
        
        async with agent.api_pool:
            response = await agent.generate_response(context, last_message)
            print("Enhanced Response:")
            print("-" * 80)
            print(response)
            print("-" * 80)
    
    asyncio.run(test_enhanced_agent())