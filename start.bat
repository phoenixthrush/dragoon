@echo off
title Dragoon
mode con: cols=100 lines=25
cls

title You got stabbed to death and reincarnated as a hero to fight a dragon that later became his new wife.
python src\dragoon\__main__.py

cls
echo Thank you for playing Dragoon!
echo Press any key to exit...
pause >nul