cd /D %~dp0
set PYTHONPATH=%~dp0\hkprofile
start venv\Scripts\pythonw.exe gserver.py >nul
