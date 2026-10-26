@echo off
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 goto usepython
py -3 demo_launcher.py
goto finished
:usepython
python demo_launcher.py
:finished
if errorlevel 1 pause
