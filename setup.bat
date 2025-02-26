@echo off
:: Create Virtual Python-Environment
echo "Creating Virtual Python-Environment..."
python -m venv ".venv"

:: Install Requirements
echo "Installing Requirements..."
"./.venv/Scripts/pip" install -r "requirements.txt"

echo "Done."

:: Remove unnecessary files
del ".gitignore"
del "requirements.txt"
del "README.md"
del "setup.bat"

:: Wait for input, then exit
pause