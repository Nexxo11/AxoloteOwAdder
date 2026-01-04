@echo off
echo Starting AxoloteOwAdder debug mode...
python main.py
if %errorlevel% neq 0 (
    echo.
    echo An error occurred. Please check the output above or error.log.
)
pause
