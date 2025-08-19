"""
Check if all required dependencies for the async implementation are installed
"""

import sys
import importlib
from typing import List, Tuple

def check_dependencies() -> List[Tuple[str, bool, str]]:
    """Check all required dependencies and return their status"""
    
    dependencies = {
        # Core async dependencies
        'aiohttp': 'Core async HTTP client/server framework',
        'asyncio': 'Built-in async support (Python 3.4+)',
        
        # Enhanced async dependencies
        'aiofiles': 'Async file operations',
        'aiodns': 'Async DNS resolver for better performance',
        'cchardet': 'Fast character encoding detection',
        'brotli': 'Compression support for aiohttp',
        
        # Testing
        'pytest': 'Testing framework',
        'pytest_asyncio': 'Async test support for pytest',
        
        # Core project dependencies
        'streamlit': 'Web UI framework',
        'dotenv': 'Environment variable management',
        'requests': 'Sync HTTP client',
        'yaml': 'YAML configuration support',
        'pandas': 'Data manipulation',
        
        # AI/ML dependencies
        'sentence_transformers': 'Semantic search (optional)',
        'torch': 'PyTorch for ML models (optional)',
    }
    
    results = []
    
    for module_name, description in dependencies.items():
        try:
            # Handle special cases
            if module_name == 'dotenv':
                importlib.import_module('dotenv')
            elif module_name == 'yaml':
                importlib.import_module('yaml')
            elif module_name == 'pytest_asyncio':
                importlib.import_module('pytest_asyncio')
            else:
                importlib.import_module(module_name)
            
            results.append((module_name, True, description))
        except ImportError:
            results.append((module_name, False, description))
    
    return results

def main():
    """Check and report dependency status"""
    print("=" * 70)
    print("ASYNC IMPLEMENTATION DEPENDENCY CHECK")
    print("=" * 70)
    
    results = check_dependencies()
    
    # Separate into categories
    core_async = ['aiohttp', 'asyncio']
    enhanced_async = ['aiofiles', 'aiodns', 'cchardet', 'brotli']
    testing = ['pytest', 'pytest_asyncio']
    optional = ['sentence_transformers', 'torch']
    
    # Core async dependencies
    print("\n🔧 CORE ASYNC DEPENDENCIES:")
    print("-" * 40)
    for name, installed, desc in results:
        if name in core_async:
            status = "✅" if installed else "❌"
            print(f"{status} {name:<20} - {desc}")
    
    # Enhanced async dependencies
    print("\n🚀 ENHANCED ASYNC DEPENDENCIES:")
    print("-" * 40)
    for name, installed, desc in results:
        if name in enhanced_async:
            status = "✅" if installed else "❌"
            print(f"{status} {name:<20} - {desc}")
    
    # Testing dependencies
    print("\n🧪 TESTING DEPENDENCIES:")
    print("-" * 40)
    for name, installed, desc in results:
        if name in testing:
            status = "✅" if installed else "❌"
            print(f"{status} {name:<20} - {desc}")
    
    # Other required dependencies
    print("\n📦 OTHER REQUIRED DEPENDENCIES:")
    print("-" * 40)
    for name, installed, desc in results:
        if name not in core_async + enhanced_async + testing + optional:
            status = "✅" if installed else "❌"
            print(f"{status} {name:<20} - {desc}")
    
    # Optional dependencies
    print("\n🔮 OPTIONAL DEPENDENCIES:")
    print("-" * 40)
    for name, installed, desc in results:
        if name in optional:
            status = "✅" if installed else "⚠️"
            print(f"{status} {name:<20} - {desc}")
    
    # Summary
    installed_count = sum(1 for _, installed, _ in results if installed)
    total_count = len(results)
    required_count = total_count - len(optional)
    required_installed = sum(1 for name, installed, _ in results 
                           if installed and name not in optional)
    
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print(f"Total dependencies: {installed_count}/{total_count} installed")
    print(f"Required dependencies: {required_installed}/{required_count} installed")
    
    # Check if all required async dependencies are installed
    async_deps = core_async + enhanced_async
    async_installed = all(installed for name, installed, _ in results 
                         if name in async_deps)
    
    if async_installed:
        print("\n✅ All async dependencies are installed!")
        print("   The enhanced async implementation is ready to use.")
    else:
        missing = [name for name, installed, _ in results 
                  if not installed and name in async_deps]
        print(f"\n❌ Missing async dependencies: {', '.join(missing)}")
        print("   Run: pip install " + " ".join(missing))
    
    print("=" * 70)

if __name__ == "__main__":
    main()