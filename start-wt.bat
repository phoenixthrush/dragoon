@echo off

echo Starting up...

REM Use old cmd instead of Windows Terminal to allow resizing the window
set id=Dragoon
title %id%
tasklist /v /fo csv | findstr "%id%" | findstr "cmd.exe"
if %errorlevel% == 1 start conhost "%~f0" & GOTO :EOF

cls

mode con: cols=100 lines=25

title Clayn got stabbed to death and reincarnated as a hero to fight a dragon that later became his new wife.
python src\dragoon\__main__.py

cls
echo Thank you for playing Dragoon!
echo Press any key to exit...
pause >nul