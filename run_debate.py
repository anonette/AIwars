import subprocess
import sys
import os

def main():
    try:
        # Attempt to import necessary modules to ensure they are installed.
        # The user is expected to have installed these via requirements.txt
        import streamlit
        import asyncio
        import pandas
        from dotenv import load_dotenv

        # Check if the debate file exists
        debate_file = "debatepy.py"
        if not os.path.exists(debate_file):
            print(f"Error: {debate_file} not found. Please ensure the file exists in the current directory.")
            sys.exit(1)
        
        # Run the debate app - use sys.executable to ensure we use the correct Python interpreter
        print(f"Starting AI Futures Deliberation using {debate_file}...")
        print("Opening Streamlit app... (This will open in your browser)")
        
        # Use the same Python executable that's running this script
        cmd = [sys.executable, "-m", "streamlit", "run", debate_file]
        subprocess.run(cmd)
        
    except ImportError as e:
        print(f"Error: A required Python package is missing: {e}")
        print("Please ensure you have installed all dependencies from requirements.txt by running:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error running debate application: {e}")
        print("\nAlternatively, you can run the app directly with:")
        print("streamlit run debatepy.py")
        sys.exit(1)

if __name__ == "__main__":
    main()