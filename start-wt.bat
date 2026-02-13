@echo off

echo Starting up...

REM Use old cmd instead of Windows Terminal to allow resizing the window
set id=Dragoon
title %id%
tasklist /v /fo csv | findstr "%id%" | findstr "cmd.exe"
if %errorlevel% == 1 start conhost "%~f0" & GOTO :EOF

cls

mode con: cols=80 lines=25

python src\dragoon\__main__.py

cls
echo Thank you for playing Dragoon!
echo Press any key to exit...
pause >nul