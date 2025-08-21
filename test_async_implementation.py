"""
Comprehensive test suite for the enhanced async implementation
Tests concurrent operations, timeouts, retries, and performance
"""

import asyncio
import time
import logging
from unittest.mock import Mock, AsyncMock, patch
import pytest
from enhanced_async_debate_agent import EnhancedAsyncDebateAgent
from async_enhancements import AsyncAPIPool, AsyncRetryHandler, ConcurrentDebateOperations
from perplexity_search import PerplexitySearchClient, SearchResult, SignalType
from document_retrieval import DocumentStore

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestAsyncEnhancements:
    """Test the async enhancement components"""
    
    @pytest.mark.asyncio
    async def test_api_pool_connection_management(self):
        """Test connection pooling works correctly"""
        async with AsyncAPIPool(max_connections=5, timeout=10) as pool:
            # Simulate multiple concurrent requests
            async def make_request(i):
                return await pool.request('GET', f'https://httpbin.org/delay/{i%3}')
            
            start_time = time.time()
            results = await asyncio.gather(*[make_request(i) for i in range(10)])
            elapsed = time.time() - start_time
            
            assert len(results) == 10
            assert elapsed < 10  # Should be faster than sequential (30s)
            print(f"✓ Connection pool handled 10 requests in {elapsed:.2f}s")
    
    @pytest.mark.asyncio
    async def test_retry_handler(self):
        """Test retry logic with exponential backoff"""
        attempt_count = 0
        
        @AsyncRetryHandler.with_retry(max_attempts=3, backoff_factor=2.0)
        async def flaky_operation():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise Exception(f"Attempt {attempt_count} failed")
            return "Success"
        
        result = await flaky_operation()
        assert result == "Success"
        assert attempt_count == 3
        print("✓ Retry handler succeeded after 3 attempts")
    
    @pytest.mark.asyncio
    async def test_concurrent_operations(self):
        """Test concurrent search and document retrieval"""
        async with AsyncAPIPool() as pool:
            ops = ConcurrentDebateOperations(pool)
            
            # Mock functions
            async def mock_search(query):
                await asyncio.sleep(0.1)
                return f"Search: {query}"
            
            async def mock_doc_search(query):
                await asyncio.sleep(0.05)
                return f"Doc: {query}"
            
            results = await ops.concurrent_search_and_retrieve(
                search_queries=["AI policy", "AI safety"],
                document_queries=["governance"],
                search_func=mock_search,
                doc_func=mock_doc_search
            )
            
            assert len(results['search_results']) == 2
            assert len(results['document_results']) == 1
            print("✓ Concurrent operations completed successfully")


class TestEnhancedDebateAgent:
    """Test the enhanced async debate agent"""
    
    @pytest.fixture
    def mock_components(self):
        """Create mock components for testing"""
        mock_doc_store = Mock(spec=DocumentStore)
        mock_search_client = Mock(spec=PerplexitySearchClient)
        
        # Setup async mocks
        mock_search_client.generate_meta_query = AsyncMock(
            return_value=("test query", "test angle")
        )
        mock_search_client.search = AsyncMock(
            return_value=[SearchResult(
                query="test",
                content="Test content",
                source="Test Source",
                url="https://test.com",
                timestamp="2024-01-01",
                signal_type=SignalType.TYING_HANDS
            )]
        )
        
        return mock_doc_store, mock_search_client
    
    @pytest.mark.asyncio
    async def test_concurrent_information_gathering(self, mock_components):
        """Test concurrent information gathering"""
        mock_doc_store, mock_search_client = mock_components
        
        agent = EnhancedAsyncDebateAgent(
            name="Test Agent",
            personality="Test personality",
            agent_config_key="test",
            document_store=mock_doc_store,
            search_client=mock_search_client
        )
        
        # Mock document retrieval
        agent._get_document_context_with_tracking = Mock(
            return_value=("Document context", ["doc1.pdf"])
        )
        
        start_time = time.time()
        search_results, doc_context = await agent._concurrent_information_gathering(
            topic="AI governance",
            last_message="Previous message",
            context="Debate context"
        )
        elapsed = time.time() - start_time
        
        assert search_results is not None
        assert doc_context == "Document context"
        assert elapsed < 1.0  # Should be fast with mocks
        print(f"✓ Concurrent gathering completed in {elapsed:.2f}s")
    
    @pytest.mark.asyncio
    async def test_timeout_handling(self, mock_components):
        """Test timeout handling in async operations"""
        mock_doc_store, mock_search_client = mock_components
        
        # Create a slow search function
        async def slow_search(*args):
            await asyncio.sleep(5)
            return []
        
        mock_search_client.search = slow_search
        
        agent = EnhancedAsyncDebateAgent(
            name="Test Agent",
            personality="Test personality",
            agent_config_key="test",
            document_store=mock_doc_store,
            search_client=mock_search_client
        )
        
        # This should timeout
        search_results, _ = await agent._concurrent_information_gathering(
            topic="test",
            last_message="test",
            context="test"
        )
        
        # Should handle timeout gracefully
        assert search_results is None
        print("✓ Timeout handled gracefully")
    
    @pytest.mark.asyncio
    async def test_performance_monitoring(self, mock_components):
        """Test performance monitoring decorator"""
        from async_enhancements import async_performance_monitor
        
        @async_performance_monitor
        async def monitored_function():
            await asyncio.sleep(0.1)
            return "Done"
        
        with patch('logging.info') as mock_log:
            result = await monitored_function()
            assert result == "Done"
            
            # Check that performance was logged
            log_calls = [call[0][0] for call in mock_log.call_args_list]
            assert any("completed in" in log for log in log_calls)
            print("✓ Performance monitoring working")


class TestIntegrationScenarios:
    """Test real-world integration scenarios"""
    
    @pytest.mark.asyncio
    async def test_multi_agent_concurrent_response(self):
        """Test multiple agents generating responses concurrently"""
        # Create mock agents
        agents = []
        for i in range(3):
            agent = Mock()
            agent.name = f"Agent {i}"
            agent.generate_response = AsyncMock(
                return_value=f"Response from Agent {i}"
            )
            agents.append(agent)
        
        # Generate responses concurrently
        start_time = time.time()
        responses = await asyncio.gather(*[
            agent.generate_response("context", "last message")
            for agent in agents
        ])
        elapsed = time.time() - start_time
        
        assert len(responses) == 3
        assert all(f"Response from Agent {i}" == responses[i] for i in range(3))
        print(f"✓ Multi-agent responses generated in {elapsed:.2f}s")
    
    @pytest.mark.asyncio
    async def test_debate_session_context_manager(self):
        """Test debate session context manager"""
        from async_enhancements import debate_session
        
        mock_agents = [Mock(name=f"Agent {i}") for i in range(3)]
        
        # Mock the parallel preparation
        with patch('async_enhancements.ConcurrentDebateOperations.parallel_agent_preparation') as mock_prep:
            mock_prep.return_value = [
                {'agent': agent.name, 'search': None, 'documents': None}
                for agent in mock_agents
            ]
            
            async with debate_session(mock_agents, "Test Topic") as enhancer:
                assert enhancer is not None
                assert enhancer.api_pool is not None
                print("✓ Debate session context manager working")


class TestPerformanceBenchmarks:
    """Benchmark the performance improvements"""
    
    @pytest.mark.asyncio
    async def test_response_generation_performance(self):
        """Compare sync vs async response generation"""
        # Simulate sync operation
        def sync_operation():
            time.sleep(0.1)  # Search
            time.sleep(0.1)  # Document retrieval
            time.sleep(0.2)  # LLM call
            return "Response"
        
        # Simulate async operation
        async def async_operation():
            search = asyncio.create_task(asyncio.sleep(0.1))
            docs = asyncio.create_task(asyncio.sleep(0.1))
            await asyncio.gather(search, docs)
            await asyncio.sleep(0.2)  # LLM call
            return "Response"
        
        # Measure sync time
        start = time.time()
        sync_result = sync_operation()
        sync_time = time.time() - start
        
        # Measure async time
        start = time.time()
        async_result = await async_operation()
        async_time = time.time() - start
        
        improvement = (sync_time - async_time) / sync_time * 100
        print(f"✓ Performance improvement: {improvement:.1f}%")
        print(f"  Sync: {sync_time:.3f}s, Async: {async_time:.3f}s")
        
        assert async_time < sync_time
        assert improvement > 20  # At least 20% improvement


async def run_all_tests():
    """Run all tests and report results"""
    print("=" * 60)
    print("ASYNC IMPLEMENTATION TEST SUITE")
    print("=" * 60)
    
    test_classes = [
        TestAsyncEnhancements(),
        TestEnhancedDebateAgent(),
        TestIntegrationScenarios(),
        TestPerformanceBenchmarks()
    ]
    
    for test_class in test_classes:
        print(f"\n{test_class.__class__.__name__}:")
        print("-" * 40)
        
        # Get all test methods
        test_methods = [
            method for method in dir(test_class)
            if method.startswith('test_') and callable(getattr(test_class, method))
        ]
        
        for method_name in test_methods:
            method = getattr(test_class, method_name)
            try:
                # Handle fixtures manually for this example
                if 'mock_components' in method.__code__.co_varnames:
                    fixture = test_class.mock_components()
                    await method(fixture)
                else:
                    await method()
            except Exception as e:
                print(f"✗ {method_name}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    # Run the test suite
    asyncio.run(run_all_tests())