#!/usr/bin/env python3
"""
Ultra-fast launcher for maximum performance Streamlit debate app
"""

import subprocess
import sys

def main():
    print("=== ULTRA-FAST AI GOVERNANCE DEBATE ===")
    print("Maximum performance version - minimal processing")
    print()
    
    print("🔧 PERFORMANCE OPTIMIZATIONS:")
    print("✅ No search integration (saves 3-5s per response)")
    print("✅ No document processing (saves 2-3s per response)")
    print("✅ No theoretical analysis (saves 4-6s per response)")
    print("✅ Short responses (200 tokens max)")
    print("✅ 10 second API timeout")
    print("✅ Minimal session state")
    print("✅ Simplified UI")
    print()
    
    print("⚡ EXPECTED PERFORMANCE:")
    print("- Response time: 2-4 seconds per round")
    print("- No heavy analysis or search delays")
    print("- Direct LLM responses only")
    print()
    
    input("Press Enter to launch ultra-fast debate app...")
    
    try:
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "debatepy_ultra_fast.py",
            "--server.port=8502"  # Different port
        ]
        
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Ultra-fast app stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error launching app: {e}")

if __name__ == "__main__":
    main()
