@echo off

set WD=%~dp0
cd /d "%~dp0"
".\.venv\Scripts\python" "__convert.py" %*
cd /d "%WD%"

pause