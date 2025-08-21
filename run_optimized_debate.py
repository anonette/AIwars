#!/usr/bin/env python3
"""
Launch script for the optimized Streamlit debate app
"""

import subprocess
import sys
import os
import time

def check_environment():
    """Check if virtual environment is activated"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
        return True
    else:
        print("⚠️  Virtual environment not detected")
        print("   Consider running: python -m venv venv && venv\\Scripts\\activate")
        return False

def check_dependencies():
    """Check key dependencies"""
    try:
        import streamlit
        import yaml
        print(f"✅ Streamlit {streamlit.__version__} available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("   Run: pip install -r requirements.txt")
        return False

def launch_app():
    """Launch the optimized Streamlit app"""
    print("\n🚀 Starting optimized AI Governance Debate app...\n")
    
    # Performance tips
    print("PERFORMANCE TIPS:")
    print("1. Toggle 'Fast Mode' in sidebar for faster responses")
    print("2. Use smaller round counts (5-10) for testing") 
    print("3. Check 'Show performance stats' to monitor timing")
    print("4. Document store and search client are cached for speed")
    print()
    
    try:
        # Launch with optimized settings
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "debatepy_optimized.py",
            "--server.maxUploadSize=50",  # 50MB limit
            "--server.enableCORS=true",
            "--server.enableXsrfProtection=false",
            "--theme.primaryColor=#FF4B4B"
        ]
        
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error launching app: {e}")
        print("\nTry running manually:")
        print("streamlit run debatepy_optimized.py")

def main():
    print("=== OPTIMIZED AI GOVERNANCE DEBATE ===")
    print("Performance-optimized version of the Streamlit app\n")
    
    # Check environment
    env_ok = check_environment()
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n❌ Cannot start - missing dependencies")
        return
    
    if not env_ok:
        print("\n⚠️  Environment warning - continuing anyway...")
    
    # Show optimization summary
    print("\n🔧 OPTIMIZATIONS ACTIVE:")
    print("✅ Cached configuration loading")
    print("✅ Cached document store initialization") 
    print("✅ Cached search client setup")
    print("✅ Fast mode toggle for reduced analysis")
    print("✅ Simplified session state management")
    print("✅ Message truncation and display limits")
    print("✅ Performance timing display")
    
    input("\nPress Enter to launch the app...")
    launch_app()

if __name__ == "__main__":
    main()
