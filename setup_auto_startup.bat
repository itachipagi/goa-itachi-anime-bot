@echo off
echo Adding Telegram Bot to Windows Startup...

REM Get the current directory
set "SCRIPT_DIR=%~dp0"

REM Create a VBS script to run the bot without a visible window
echo Creating hidden startup script...
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo Dim strArgs
echo strArgs = "cmd /c cd /d ""%SCRIPT_DIR%"" && python run_bot_forever.py"
echo WshShell.Run strArgs, 0, False
) > "%SCRIPT_DIR%\run_bot_hidden.vbs"

REM Create the startup shortcut
echo Creating startup shortcut...
(
echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
echo sLinkFile = oWS.SpecialFolders^("Startup"^) ^& "\TelegramBot.lnk"
echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
echo oLink.TargetPath = "%SCRIPT_DIR%\run_bot_hidden.vbs"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%"
echo oLink.Description = "Telegram Bot Autostart"
echo oLink.Save
) > "%TEMP%\create_shortcut.vbs"

cscript //nologo "%TEMP%\create_shortcut.vbs"
del "%TEMP%\create_shortcut.vbs"

echo.
echo The Telegram Bot has been added to Windows startup.
echo It will automatically start when you log in to Windows.
echo.
echo To run it now without restarting, double-click on:
echo %SCRIPT_DIR%\run_bot_hidden.vbs
echo.
pause 
