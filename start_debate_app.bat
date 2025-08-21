@echo off
echo Starting AI Wars Debate System...
echo.
echo Configuration:
echo - PyTorch file watcher conflicts resolved
echo - Search integration enabled
echo - Running on port 8503
echo.

REM Set environment variables to avoid conflicts
set STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
set STREAMLIT_SERVER_RUN_ON_SAVE=false

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the app
echo Access the app at: http://localhost:8503
echo.
streamlit run debatepy.py --server.port 8503 --server.fileWatcherType none

pause