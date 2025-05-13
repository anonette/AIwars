import streamlit as st
import subprocess
import sys
import os

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "asyncio", "python-dotenv", "pandas"])
        print("Required packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        sys.exit(1)

def main():
    try:
        # Check if required packages are installed
        try:
            import streamlit
            import asyncio
            import pandas
            from dotenv import load_dotenv
        except ImportError as e:
            print(f"Missing dependency: {e}")
            install_requirements()
        
        # Check if the debate file exists
        debate_file = "debatepy.py"
        if not os.path.exists(debate_file):
            print(f"Error: {debate_file} not found.")
            fallback_file = "debate_app.py"
            if os.path.exists(fallback_file):
                print(f"Using fallback file: {fallback_file}")
                debate_file = fallback_file
            else:
                print("No debate application file found.")
                sys.exit(1)
        
        # Run the debate app
        print(f"Starting debate app using {debate_file}...")
        subprocess.run(["streamlit", "run", debate_file])
    except Exception as e:
        print(f"Error running debate application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()