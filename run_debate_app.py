"""
Wrapper script to run the debate app with proper environment setup
"""
import os
import sys
import subprocess

# Set environment variables to avoid PyTorch/Streamlit conflicts
os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'
os.environ['STREAMLIT_SERVER_RUN_ON_SAVE'] = 'false'

# Ensure we're using the virtual environment
if sys.platform == "win32":
    activate_script = os.path.join("venv", "Scripts", "activate.bat")
else:
    activate_script = os.path.join("venv", "bin", "activate")

# Run streamlit
try:
    print("Starting AI Wars Debate System...")
    print("Configuration:")
    print("- File watcher disabled (to avoid PyTorch conflicts)")
    print("- Search integration enabled")
    print("\nAccess the app at: http://localhost:8503")
    
    # Run streamlit with the main app
    subprocess.run([sys.executable, "-m", "streamlit", "run", "debatepy.py", "--server.port", "8503"])
    
except KeyboardInterrupt:
    print("\nShutting down...")
except Exception as e:
    print(f"Error: {e}")