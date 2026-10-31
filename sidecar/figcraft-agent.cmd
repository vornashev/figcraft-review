@echo off
rem Opens the FigCraft Agent chat; starts its server when it isn't running (see launch.py).
where py >nul 2>nul
if %errorlevel%==0 (py -3 "%~dp0launch.py" %*) else (python "%~dp0launch.py" %*)
