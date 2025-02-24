@echo off
set WD=%cd%
cd "%~dp0"
set args=
:loop
if "%1"=="" goto execute
set args=%args% "%1"
shift
goto loop
:execute
".\.venv\Scripts\python" "__convert.py"%args%
cd %WD%
pause
