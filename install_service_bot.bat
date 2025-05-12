@echo off
echo Installing the Telegram Bot Windows Service...

REM Check for admin privileges
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo This script requires administrator privileges.
    echo Please right-click on this file and select "Run as administrator"
    pause
    exit /b 1
)

REM Install required Python packages
echo Installing required Python packages...
pip install pywin32 python-telegram-bot python-dotenv

REM Install the service
echo Installing the Windows service...
python bot_service.py install

REM Start the service
echo Starting the service...
python bot_service.py start

echo.
echo The Telegram Bot service has been installed and started.
echo It will now run in the background even when you close this window.
echo.
echo To manage the service:
echo - To stop: python bot_service.py stop
echo - To restart: python bot_service.py restart
echo - To remove: python bot_service.py remove
echo.
echo You can also manage the service through Windows Services:
echo 1. Press Win+R, type "services.msc" and press Enter
echo 2. Look for "Telegram Bot Service" in the list
echo.
pause 

