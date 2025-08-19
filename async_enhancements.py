"""
Enhanced asynchronous implementations for the AI debate system
Optimizes concurrent operations for better performance
"""

import asyncio
import aiohttp
from typing import List, Dict, Optional, Any, Callable
from contextlib import asynccontextmanager
import logging
from datetime import datetime
import time
from functools import wraps

class AsyncAPIPool:
    """Connection pool manager for API calls"""
    
    def __init__(self, max_connections: int = 10, timeout: int = 30):
        self.max_connections = max_connections
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None
        self._connector: Optional[aiohttp.TCPConnector] = None
        
    async def __aenter__(self):
        self._connector = aiohttp.TCPConnector(
            limit=self.max_connections,
            limit_per_host=5,
            ttl_dns_cache=300
        )
        self._session = aiohttp.ClientSession(
            connector=self._connector,
            timeout=self.timeout
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()
        if self._connector:
            await self._connector.close()
            
    async def request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Make an HTTP request with the connection pool"""
        if not self._session:
            raise RuntimeError("Session not initialized. Use async with statement.")
            
        async with self._session.request(method, url, **kwargs) as response:
            return {
                'status': response.status,
                'data': await response.json() if response.content_type == 'application/json' else await response.text(),
                'headers': dict(response.headers)
            }


class AsyncRetryHandler:
    """Handles retries with exponential backoff for async operations"""
    
    @staticmethod
    def with_retry(max_attempts: int = 3, backoff_factor: float = 2.0):
        """Decorator for adding retry logic to async functions"""
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                last_exception = None
                
                for attempt in range(max_attempts):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        if attempt < max_attempts - 1:
                            wait_time = backoff_factor ** attempt
                            logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                            await asyncio.sleep(wait_time)
                        else:
                            logging.error(f"All {max_attempts} attempts failed")
                            
                raise last_exception
            return wrapper
        return decorator


class ConcurrentDebateOperations:
    """Handles concurrent operations for the debate system"""
    
    def __init__(self, api_pool: AsyncAPIPool):
        self.api_pool = api_pool
        self.semaphore = asyncio.Semaphore(5)  # Limit concurrent operations
        
    async def concurrent_search_and_retrieve(self, 
                                           search_queries: List[str],
                                           document_queries: List[str],
                                           search_func: Callable,
                                           doc_func: Callable) -> Dict[str, Any]:
        """
        Perform search and document retrieval concurrently
        """
        async with self.semaphore:
            # Create tasks for all operations
            search_tasks = [search_func(query) for query in search_queries]
            doc_tasks = [doc_func(query) for query in document_queries]
            
            # Run all tasks concurrently
            all_tasks = search_tasks + doc_tasks
            results = await asyncio.gather(*all_tasks, return_exceptions=True)
            
            # Separate results
            search_results = results[:len(search_tasks)]
            doc_results = results[len(search_tasks):]
            
            # Filter out exceptions
            search_results = [r for r in search_results if not isinstance(r, Exception)]
            doc_results = [r for r in doc_results if not isinstance(r, Exception)]
            
            return {
                'search_results': search_results,
                'document_results': doc_results
            }
    
    async def parallel_agent_preparation(self, agents: List[Any], context: str) -> List[Dict[str, Any]]:
        """
        Prepare multiple agents in parallel (e.g., for conclusion generation)
        """
        async def prepare_agent(agent):
            try:
                # Each agent can search and retrieve documents concurrently
                search_task = agent.search_information(context)
                doc_task = agent.retrieve_documents(context)
                
                search_result, doc_result = await asyncio.gather(
                    search_task, doc_task, return_exceptions=True
                )
                
                return {
                    'agent': agent.name,
                    'search': search_result if not isinstance(search_result, Exception) else None,
                    'documents': doc_result if not isinstance(doc_result, Exception) else None
                }
            except Exception as e:
                logging.error(f"Error preparing agent {agent.name}: {e}")
                return {'agent': agent.name, 'error': str(e)}
        
        # Prepare all agents concurrently
        tasks = [prepare_agent(agent) for agent in agents]
        return await asyncio.gather(*tasks)


class AsyncDebateEnhancer:
    """Main class for enhancing debate system with better async patterns"""
    
    def __init__(self):
        self.api_pool = AsyncAPIPool(max_connections=20, timeout=60)
        self.operations = ConcurrentDebateOperations(self.api_pool)
        
    @AsyncRetryHandler.with_retry(max_attempts=3)
    async def enhanced_generate_response(self, agent, context: str, last_message: str) -> str:
        """
        Enhanced response generation with concurrent operations
        """
        # Prepare search queries based on context
        search_queries = self._extract_search_queries(context, last_message)
        doc_queries = self._extract_document_queries(context, last_message)
        
        # Perform concurrent operations
        results = await self.operations.concurrent_search_and_retrieve(
            search_queries=search_queries,
            document_queries=doc_queries,
            search_func=agent.search_client.search,
            doc_func=agent.document_store.search_documents
        )
        
        # Generate response with all gathered information
        response = await agent.generate_response_with_context(
            context=context,
            last_message=last_message,
            search_results=results['search_results'],
            document_results=results['document_results']
        )
        
        return response
    
    def _extract_search_queries(self, context: str, last_message: str) -> List[str]:
        """Extract relevant search queries from context"""
        # This would use NLP or keyword extraction in a real implementation
        queries = []
        
        # Extract key topics
        if "AI governance" in context.lower():
            queries.append("latest AI governance policies 2024")
        if "regulation" in last_message.lower():
            queries.append("AI regulation updates")
        if "cooperation" in context.lower():
            queries.append("international AI cooperation agreements")
            
        return queries[:3]  # Limit to 3 queries
    
    def _extract_document_queries(self, context: str, last_message: str) -> List[str]:
        """Extract relevant document queries from context"""
        queries = []
        
        # Extract key terms for document search
        if "policy" in context.lower():
            queries.append("AI policy framework")
        if "safety" in last_message.lower():
            queries.append("AI safety standards")
            
        return queries[:2]  # Limit to 2 queries


# Example usage with timeout handling
async def example_with_timeout():
    """Example of using timeouts with async operations"""
    
    async def long_running_operation():
        await asyncio.sleep(10)
        return "Completed"
    
    try:
        # Set a 5-second timeout
        result = await asyncio.wait_for(long_running_operation(), timeout=5.0)
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Operation timed out after 5 seconds")


# Context manager for managing debate session resources
@asynccontextmanager
async def debate_session(agents: List[Any], topic: str):
    """
    Context manager for a complete debate session with proper resource management
    """
    enhancer = AsyncDebateEnhancer()
    
    try:
        # Initialize session
        async with enhancer.api_pool:
            logging.info(f"Starting debate session on topic: {topic}")
            
            # Prepare all agents concurrently
            preparation_results = await enhancer.operations.parallel_agent_preparation(
                agents, f"Prepare for debate on: {topic}"
            )
            
            logging.info(f"Agents prepared: {[r['agent'] for r in preparation_results]}")
            
            yield enhancer
            
    finally:
        # Cleanup
        logging.info("Debate session ended, cleaning up resources")


# Performance monitoring decorator
def async_performance_monitor(func: Callable):
    """Monitor performance of async functions"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            elapsed = time.time() - start_time
            logging.info(f"{func.__name__} completed in {elapsed:.2f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logging.error(f"{func.__name__} failed after {elapsed:.2f}s: {e}")
            raise
            
    return wrapper


# Example of enhanced async agent response
class EnhancedAsyncAgent:
    """Example of how to integrate async enhancements into existing agents"""
    
    def __init__(self, name: str, search_client, document_store):
        self.name = name
        self.search_client = search_client
        self.document_store = document_store
        
    @async_performance_monitor
    @AsyncRetryHandler.with_retry(max_attempts=3)
    async def generate_enhanced_response(self, context: str, last_message: str) -> str:
        """
        Generate response with concurrent search and document retrieval
        """
        # Create concurrent tasks
        tasks = []
        
        # Search task
        if self.search_client:
            search_task = asyncio.create_task(
                self.search_client.search(f"{self.name} {context}")
            )
            tasks.append(('search', search_task))
        
        # Document retrieval task
        if self.document_store:
            doc_task = asyncio.create_task(
                self.document_store.search_documents(
                    query=context,
                    agent_name=self.name,
                    max_results=5
                )
            )
            tasks.append(('documents', doc_task))
        
        # Wait for all tasks with timeout
        results = {}
        for task_name, task in tasks:
            try:
                results[task_name] = await asyncio.wait_for(task, timeout=10.0)
            except asyncio.TimeoutError:
                logging.warning(f"{task_name} timed out for {self.name}")
                results[task_name] = None
        
        # Generate response with gathered information
        return await self._generate_with_context(context, last_message, results)
    
    async def _generate_with_context(self, context: str, last_message: str, 
                                   gathered_info: Dict[str, Any]) -> str:
        """Generate response using gathered information"""
        # This would integrate with the actual LLM call
        prompt = f"Context: {context}\nLast: {last_message}\n"
        
        if gathered_info.get('search'):
            prompt += f"Search results: {gathered_info['search']}\n"
        if gathered_info.get('documents'):
            prompt += f"Documents: {gathered_info['documents']}\n"
            
        # Simulate LLM call
        await asyncio.sleep(0.1)  # Simulate API delay
        return f"{self.name} responds based on gathered information"


if __name__ == "__main__":
    # Example usage
    async def main():
        # Test timeout handling
        await example_with_timeout()
        
        # Test concurrent operations
        async with AsyncAPIPool() as pool:
            operations = ConcurrentDebateOperations(pool)
            
            # Simulate concurrent searches
            async def mock_search(query):
                await asyncio.sleep(1)
                return f"Results for: {query}"
            
            async def mock_doc_search(query):
                await asyncio.sleep(0.5)
                return f"Documents for: {query}"
            
            results = await operations.concurrent_search_and_retrieve(
                search_queries=["AI policy", "AI safety"],
                document_queries=["governance framework"],
                search_func=mock_search,
                doc_func=mock_doc_search
            )
            
            print("Concurrent results:", results)
    
    asyncio.run(main())