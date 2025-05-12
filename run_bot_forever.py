"""
Alternative to Windows service - runs the bot continuously
and restarts it if it crashes. This version doesn't require
administrator privileges but will show a console window.
"""

import os
import sys
import time
import subprocess
import logging
import signal

# Set up logging
logging.basicConfig(
    filename='bot_runner.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables
bot_process = None
is_running = True

def signal_handler(sig, frame):
    """Handle Ctrl+C and other termination signals"""
    global is_running, bot_process
    print("\nStopping bot...")
    logger.info("Received termination signal, shutting down")
    is_running = False
    
    if bot_process:
        try:
            bot_process.terminate()
        except:
            pass

def main():
    global bot_process, is_running
    
    # Set up signal handlers for clean shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bot_script = os.path.join(script_dir, 'bot.py')
    
    print(f"Starting Telegram bot from: {bot_script}")
    print("Bot will run continuously and restart if it crashes")
    print("Press Ctrl+C to stop")
    logger.info(f"Starting bot from: {bot_script}")
    
    # Keep restarting the bot if it crashes
    while is_running:
        try:
            # Start the bot process
            python_exec = sys.executable
            bot_process = subprocess.Popen(
                [python_exec, bot_script],
                cwd=script_dir
            )
            
            print(f"Bot process started with PID: {bot_process.pid}")
            logger.info(f"Bot process started with PID: {bot_process.pid}")
            
            # Wait for the process to end
            bot_process.wait()
            
            # If we get here, the process has ended
            if is_running:
                print("Bot process has stopped unexpectedly, restarting in 10 seconds...")
                logger.warning("Bot process has stopped unexpectedly")
                time.sleep(10)
            
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            print(f"Error: {e}")
            if is_running:
                print("Waiting 60 seconds before retrying...")
                time.sleep(60)
    
    print("Bot runner stopped")
    logger.info("Bot runner stopped")

if __name__ == "__main__":
    main() 
