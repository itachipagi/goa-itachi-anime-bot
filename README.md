# Telegram Channel Filter Bot

This bot helps manage Telegram channels by providing auto-responses for specific keywords or phrases. When users ask for specific anime or content, the bot provides a button with a direct channel link.

## Features

- Responds to exact multi-word filters only
- Provides clickable buttons with channel links
- Supports 40+ anime/manga channels
- Auto-restart if crashed
- 24/7 operation options

## Running the Bot 24/7

There are three ways to keep the bot running 24/7, even when you close your computer or restart it:

### Option 1: Use the Simple Runner (Easiest)

1. Double-click `run_bot_forever.py` to start the bot
2. This will keep the bot running and automatically restart it if it crashes
3. A console window will remain open while it runs

**Note:** This option requires the console window to stay open.

### Option 2: Add to Windows Startup (Recommended)

1. Run `setup_auto_startup.bat` by double-clicking it
2. This will create scripts to automatically start the bot when you log in to Windows
3. The bot will run invisibly in the background
4. To start the bot now without restarting, use the `run_bot_hidden.vbs` script

**Note:** This option doesn't require administrator privileges.

### Option 3: Install as Windows Service (Advanced)

1. Right-click on `install_service.bat` and select "Run as administrator"
2. This will install the bot as a Windows service that starts automatically with Windows
3. The bot will run even if no user is logged in

**Note:** This option requires administrator privileges.

## Managing the Bot

- To stop the Windows service: `python bot_service.py stop`
- To restart the Windows service: `python bot_service.py restart`
- To remove the Windows service: `python bot_service.py remove`

## Available Filters

Type "anime list" in a group with the bot to see all available anime/manga channels.

Main filters:
- "channels" - See all channels
- "attack on titan"
- "tokyo 24th ward"
- "naruto shippuden"
- "married" or "girl i hate"
- "wolf king"
- "solo leveling"
- and many more!

## Logs

- `bot.log` - Main bot log
- `bot_runner.log` - Log for the simple runner
- `bot_service.log` - Log for the Windows service

## Requirements

- Python 3.7+
- python-telegram-bot
- pywin32 (for Windows service option)
- python-dotenv 
