# Telegram Bot Deployment Guide

This guide will help you deploy your Telegram bot to run continuously 24/7, even when your computer is turned off.

## Option 1: Using a VPS (Virtual Private Server)

A VPS is the most reliable way to deploy your bot for 24/7 operation.

### Step 1: Choose a VPS Provider

Popular affordable options include:
- [DigitalOcean](https://www.digitalocean.com/) ($5/month droplet is sufficient)
- [Linode](https://www.linode.com/) (Basic plans start at $5/month)
- [Oracle Cloud](https://www.oracle.com/cloud/) (Has a free tier)
- [AWS EC2](https://aws.amazon.com/ec2/) (Has a free tier)

### Step 2: Set Up Your VPS

1. Create an account and set up a basic Ubuntu/Debian server
2. Connect to your server via SSH
3. Update your system:
   ```
   sudo apt update && sudo apt upgrade -y
   ```
4. Install Python and pip:
   ```
   sudo apt install python3 python3-pip git screen -y
   ```

### Step 3: Upload Your Bot Code

1. Clone your repository or upload your bot files using SCP or SFTP
2. If using Git:
   ```
   git clone https://your-repository-url.git
   cd your-repository-folder
   ```

### Step 4: Install Dependencies

```
pip3 install python-telegram-bot --upgrade
pip3 install -r requirements.txt  # If you have this file
```

### Step 5: Run Your Bot 24/7 Using Screen

1. Create a new screen session:
   ```
   screen -S telegram_bot
   ```

2. Run your bot:
   ```
   python3 bot.py
   ```

3. Detach from the screen session by pressing `Ctrl+A` followed by `D`

4. To reattach to the session later:
   ```
   screen -r telegram_bot
   ```

## Option 2: Using a Windows Server/Computer

If you prefer to run the bot on a Windows server or computer that stays on 24/7:

### Step 1: Install Python

1. Download and install Python from [python.org](https://www.python.org/downloads/)
2. Make sure to add Python to PATH during installation

### Step 2: Set Up the Bot as a Windows Service

1. Install NSSM (Non-Sucking Service Manager):
   - Download from [nssm.cc](https://nssm.cc/download)
   - Extract the files
   - Open Command Prompt as Administrator
   - Navigate to the extracted folder (nssm-2.24\win64)

2. Create a service:
   ```
   nssm install TelegramBot
   ```

3. In the GUI that appears:
   - Application Path: Browse to your Python executable (e.g., C:\Python311\python.exe)
   - Startup Directory: Your bot's directory (e.g., C:\bots\telegram_bot)
   - Arguments: bot.py
   - Click "Install service"

4. Start the service:
   ```
   nssm start TelegramBot
   ```

## Option 3: Using the Existing bot_service.py Script (Windows)

The `bot_service.py` script included in this project sets up a Windows service:

1. Install required packages:
   ```
   pip install pywin32
   ```

2. Install the service:
   ```
   python bot_service.py install
   ```

3. Start the service:
   ```
   python bot_service.py start
   ```

4. Check service status:
   ```
   python bot_service.py status
   ```

5. To stop and remove the service:
   ```
   python bot_service.py stop
   python bot_service.py remove
   ```

## Option 4: Using a Hosting Service

Several platforms specifically host Telegram bots:

1. [PythonAnywhere](https://www.pythonanywhere.com/) - Has a free tier
2. [Heroku](https://www.heroku.com/) - Free tier available but requires card
3. [Railway](https://railway.app/) - Good for small projects

### PythonAnywhere Quick Setup:

1. Create a PythonAnywhere account
2. Go to Dashboard → Files and upload your bot files
3. Open a Console and install dependencies:
   ```
   pip3 install python-telegram-bot --upgrade
   ```
4. Go to "Tasks" and set up an "Always-on task":
   - Command: python3 /home/yourusername/your_project_folder/bot.py

## Maintaining Your Bot

Regardless of where you host your bot:

1. Set up logging to monitor issues
2. Create a simple health check that pings your bot periodically
3. Consider using a service like UptimeRobot to monitor your bot's server
4. Keep your dependencies updated

## Troubleshooting

- If your bot stops responding, check logs for errors
- Ensure your TOKEN is correct and kept secure
- For VPS hosting, make sure your server has sufficient resources
- If using the service option, check the Windows Event Viewer for service errors 
