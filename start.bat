@echo off
title Dragoon
mode con: cols=80 lines=25
cls

python src\dragoon\__main__.py

cls
echo Thank you for playing Dragoon!
echo Press any key to exit...
pause >nul