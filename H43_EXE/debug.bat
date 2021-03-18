@echo OFF

reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT

if %OS%==64BIT ("H43 BOT".exe) else ("H43 BOT (32 bits)".exe)

PAUSE