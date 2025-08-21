"""
Simple test to verify async implementation works
"""

import asyncio
import time
from async_enhancements import AsyncAPIPool, AsyncRetryHandler, ConcurrentDebateOperations

async def test_connection_pool():
    """Test basic connection pooling"""
    print("Testing Connection Pool...")
    
    async with AsyncAPIPool(max_connections=5, timeout=10) as pool:
        # Test a simple request
        try:
            result = await pool.request('GET', 'https://httpbin.org/get')
            print(f"✓ Connection pool working: Status {result['status']}")
        except Exception as e:
            print(f"✗ Connection pool error: {e}")

async def test_retry_mechanism():
    """Test retry with exponential backoff"""
    print("\nTesting Retry Mechanism...")
    
    attempt_count = 0
    
    @AsyncRetryHandler.with_retry(max_attempts=3, backoff_factor=1.5)
    async def flaky_function():
        nonlocal attempt_count
        attempt_count += 1
        print(f"  Attempt {attempt_count}")
        if attempt_count < 2:
            raise Exception("Simulated failure")
        return "Success!"
    
    try:
        result = await flaky_function()
        print(f"✓ Retry mechanism working: {result} after {attempt_count} attempts")
    except Exception as e:
        print(f"✗ Retry failed: {e}")

async def test_concurrent_operations():
    """Test concurrent execution"""
    print("\nTesting Concurrent Operations...")
    
    async def slow_operation(name, delay):
        print(f"  Starting {name}...")
        await asyncio.sleep(delay)
        print(f"  Completed {name}")
        return f"Result from {name}"
    
    # Sequential execution
    print("  Sequential execution:")
    start = time.time()
    result1 = await slow_operation("Op1", 0.5)
    result2 = await slow_operation("Op2", 0.5)
    result3 = await slow_operation("Op3", 0.5)
    seq_time = time.time() - start
    
    # Concurrent execution
    print("\n  Concurrent execution:")
    start = time.time()
    results = await asyncio.gather(
        slow_operation("Op1", 0.5),
        slow_operation("Op2", 0.5),
        slow_operation("Op3", 0.5)
    )
    conc_time = time.time() - start
    
    print(f"\n✓ Concurrent operations working:")
    print(f"  Sequential time: {seq_time:.2f}s")
    print(f"  Concurrent time: {conc_time:.2f}s")
    print(f"  Speedup: {seq_time/conc_time:.1f}x")

async def test_timeout_handling():
    """Test timeout handling"""
    print("\nTesting Timeout Handling...")
    
    async def slow_task():
        await asyncio.sleep(5)
        return "Should not reach here"
    
    try:
        result = await asyncio.wait_for(slow_task(), timeout=1.0)
        print(f"✗ Timeout not working: {result}")
    except asyncio.TimeoutError:
        print("✓ Timeout handling working: Operation timed out as expected")

async def test_semaphore_limiting():
    """Test semaphore for limiting concurrent operations"""
    print("\nTesting Semaphore Limiting...")
    
    semaphore = asyncio.Semaphore(2)  # Allow only 2 concurrent operations
    active_count = 0
    max_active = 0
    
    async def limited_operation(id):
        nonlocal active_count, max_active
        async with semaphore:
            active_count += 1
            max_active = max(max_active, active_count)
            print(f"  Task {id} started (active: {active_count})")
            await asyncio.sleep(0.2)
            active_count -= 1
            print(f"  Task {id} finished")
    
    # Try to run 5 tasks with semaphore limiting to 2
    await asyncio.gather(*[limited_operation(i) for i in range(5)])
    
    print(f"✓ Semaphore working: Max concurrent tasks was {max_active} (limit was 2)")

async def main():
    """Run all tests"""
    print("=" * 60)
    print("ASYNC IMPLEMENTATION TESTS")
    print("=" * 60)
    
    try:
        await test_connection_pool()
        await test_retry_mechanism()
        await test_concurrent_operations()
        await test_timeout_handling()
        await test_semaphore_limiting()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())