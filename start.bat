@echo off
echo Starting Cab Fare Comparator...
echo Please wait a moment while the dashboard loads in your browser.
call venv\Scripts\activate
start http://localhost:8501
streamlit run app.py
pause
